from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.models.xai import xAI
from agno.tools.file import FileTools
from agno.tools.exa import ExaTools
from agno.tools.yfinance import YFinanceTools
from agno.knowledge.knowledge import Knowledge


from dotenv import load_dotenv
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

load_dotenv()

def setup_database(db_file: str = "tmp/agno.db"):
    """Setup database connection.
    Args:
        db_file (str): Path to database file.
    Returns:
        SqliteDb: Database connection object.
    """
    return SqliteDb(db_file=db_file)


def create_claim_classifier():
    """
    Creates an LLM-powered agent to classify CIMR claims.
    """
    return Agent(
        name="ClaimClassifierAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="Classifies incoming CIMR claims from text or images and stores them in database",
        instructions="""
You are an AI agent responsible for classifying CIMR retirement fund claims. 
You will receive **cleaned textual content** extracted from claims (text or OCR-processed images). 

Your tasks are:

1. **Classify the claim** into one of the following types:
   - pension_payment
   - missing_contribution
   - survivor_pension
   - disability_pension
   - retirement_initiation
   - correction_of_records
   - general_info / other

2. **Extract key entities** relevant to the claim:
   - dates / periods (e.g., contribution period)
   - employer name
   - member identifiers (if present)
   - any other relevant numeric/financial info

3. **Assign a confidence score** (0.0 to 1.0) representing how certain you are of the classification.

4. **Determine next action** based on confidence:
   - If confidence >= 0.8 → next_action = "eligibility_check"
   - If confidence < 0.8 → next_action = "clarification_required"

5. **Output** a structured JSON object in this exact format:
{
  "claim_id": "<unique_claim_id>",
  "claim_type": "<classified_type>",
  "sub_type": "<optional_sub_type>",
  "confidence": <float>,
  "entities": { ... },
  "next_action": "<eligibility_check or clarification_required>"
}

6. **Do not attempt eligibility checks** yourself. Just classify and extract information.
7. Be concise, factual, and avoid assumptions not present in the text.
8. Store the output in the claims database with status = "classified" and await the Eligibility & Rules Agent.
        """,
        tools=[],  # OCR should be performed before passing text to this agent
    )

agent= create_claim_classifier()

# agent.print_response("Mon employeur ABC SARL n’a pas déclaré mes cotisations pour la période 2019-2021. Je réclame ces cotisations manquantes.")

### 2nd agent


def _load_cimr_knowledge(self) -> Knowledge:
        """Load CIMR regulations and rules"""
        return Knowledge(
            documents=[
             #include documents
            ]
        )

def create_eligibility_rules_agent():## include that we have to follow strictly the rules of the knowledge base to vaidate the claims
    """
    Creates an AI agent to validate CIMR claims against rules and member profiles.
    """
    return Agent(
        name="EligibilityRulesAgent",
        description="Validates CIMR claims against member profile and CIMR rules, returns eligibility decision, and updates the database",
        instructions="""
You are an AI agent responsible for evaluating CIMR retirement fund claims for eligibility.

Your tasks are:

1. **Fetch the claim** from the database using claim_id provided in the input.
2. **Retrieve member profile data** including:
   - Date of birth
   - Employment history
   - Contribution records (months/years paid)
   - Membership status (active, retired, disabled, deceased)

3. **Check claim against CIMR rules**:
   - Use the CIMR rules knowledge base to determine eligibility for the given claim_type.
   - Rules include: minimum contribution months, age requirements, disability status, survivor eligibility, etc.

4. **Determine eligibility_status**:
   - "eligible" → claim meets all conditions
   - "ineligible" → claim does not meet rules
   - "incomplete" → missing data or documents required to make a decision

5. **Provide reasoning / explanations** for your decision:
   - Example: "Member has 140 months of contributions and is 62 years old, which meets retirement pension conditions."

6. **Update the database** with:
   - eligibility_status
   - explanation
   - timestamp

7. **Trigger next actions** based on the result:
   - eligible → set next_action = "approve_claim" and optionally notify employee
   - ineligible → set next_action = "reject_claim" and notify employee
   - incomplete → set next_action = "request_documents" and notify employee

8. **Output** a structured JSON object in this format:
{
  "claim_id": "<claim_id>",
  "eligibility_status": "<eligible/ineligible/incomplete>",
  "rules_checked": [
    {"rule": "<rule_name>", "result": true/false}
  ],
  "missing_data": ["field1", "field2"],
  "explanations": "<text explanation>",
  "next_action": "<approve_claim/reject_claim/request_documents>"
}

9. Ensure all decisions are auditable, factual, and based strictly on the member's profile and CIMR rules.
        """,
        tools=[],  # Can integrate with DB access tool if available
    )


