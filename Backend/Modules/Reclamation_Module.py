from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.models.xai import xAI
from agno.models.google import Gemini
from agno.tools.file import FileTools
from agno.tools.exa import ExaTools
from agno.tools.yfinance import YFinanceTools
from agno.knowledge.knowledge import Knowledge #V2 knowledge base
from agno.tools.reasoning import ReasoningTools
from agno.knowledge.embedder.google import GeminiEmbedder

from agno.vectordb.lancedb import LanceDb



# Import reclamation tools for Airtable integration
# from .Tools.Reclamation_tools import *

from dotenv import load_dotenv
import os
import sys
import json
import uuid
from datetime import datetime


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

load_dotenv()

from Backend.Tools.Reclamation_tools import *
    #2nd agent


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
        # model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
         model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY_2")),
        description="Classifies incoming CIMR claims from text or images and stores them in database",
        instructions="""
      You are a CIMR claim classifier. Follow these steps EXACTLY:

      1. Read the claim text
      2. Classify it into one of these categories:
         - pension_payment (issues with pension payments)
         - missing_contribution (employer didn't pay contributions)
         - survivor_pension (death benefits)
         - disability_pension (disability benefits)
         - retirement_initiation (starting retirement)
         - correction_of_records (fixing member records)
         - general_info (other questions)

      3. Extract key information like dates, employer names, amounts
      4. Generate a member_id (like M001, M002, etc.)
      5. Give a confidence score (0.0 to 1.0)
      6. Determine next_action: "eligibility_check" if confidence >= 0.8, otherwise "clarification_required"

      7. IMPORTANT: Create a complete dictionary with ALL required fields, then call create_claim_record:

      For the text "Mon employeur ABC SARL n'a pas déclaré mes cotisations pour la période 2019-2021. Je réclame ces cotisations manquantes."

      You should call:
      create_claim_record({
      
      "member_id": "M001", 
      "claim_type": "missing_contribution",
      "confidence": 0.9,
      "entities": {"employer": "ABC SARL", "period": "2019-2021"},
      "next_action": "eligibility_check"
      }, "Mon employeur ABC SARL n'a pas déclaré mes cotisations pour la période 2019-2021. Je réclame ces cotisations manquantes.")

      DO NOT call create_claim_record with empty data. Always create the complete dictionary first.

      as a response, return the claim_id, and message saying Claim created successfully
        """,
        tools=[create_claim_record, ReasoningTools()],  # Add the database storage tool
        stream=True,
    )

# Create agent instances
claim_classifier_agent = create_claim_classifier()

# # Test functions
# def test_claim_classification():
#     """Test the claim classification workflow"""
#     test_claim = "Mon employeur ABC SARL n'a pas déclaré mes cotisations pour la période 2019-2021. Je réclame ces cotisations manquantes."
#     print("Testing claim classification...")
#     claim_classifier_agent.print_response(test_claim, stream=True)

# def test_eligibility_check():
#     """Test the eligibility check workflow"""
#     print("Testing eligibility check...")
#     eligibility_agent.run("Please check the eligibility of the latest claim", stream=True)

# Uncomment to test
# test_claim_classification()
# test_eligibility_check()


### 2nd agent

# 1. Configure the Vector Database
# This example uses LanceDB, a simple, file-based vector database



# Agent_test=Agent(
#    name="knowledge_base_test",
#    model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
#    description="A test agent to test the knowledge base",
#    instructions="""
#    You are a test agent to test the knowledge base",
#    you only get your response from the knowledge base, you cannot use any other tools
#    """,
#    knowledge=knowledge_base,
#    # use_tools=True,
#    stream=True,
# )

# Agent_test.print_response("ou ce trouve la Caisse Interprofessionnelle Marocaine de Retraite?", stream=True)


def create_eligibility_rules_agent():
    """
    Creates an AI agent to validate CIMR claims against rules and member profiles.
    """
    # Configure the Knowledge Base (lazy initialization)
    vector_db = LanceDb(
        table_name="my_markdown_knowledge",  # Name for your knowledge base table
        uri="tmp/agno_lancedb",  # Path where the database will be stored locally
        embedder=GeminiEmbedder(),
    )
    
    knowledge_base = Knowledge(vector_db=vector_db)
    # Note: add_content will be called when the agent is first used
    # This avoids the async error during module import
    
    return Agent(
        name="EligibilityRulesAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
      #   model=Gemini(id="gemini-1.5-flash", api_key="AIzaSyDlD0tDvunUrWCeqQGg-SQ1zr7twgR4hBA"),
        description="Validates CIMR claims against member profile and CIMR rules, returns eligibility decision, and updates the database",
        instructions="""
      You are an AI agent responsible for evaluating CIMR retirement fund claims for eligibility.

      Follow these EXACT steps in order:

      1. **Get the specific claim** using get_claim_record(claim_id) with the provided claim ID
      2. **Load CIMR rules** using load_cimr_rules() to access the knowledge base
      3. **Get member profile** using get_member_profile(member_id) from the claim data
      4. **Check the claim against CIMR rules** using the knowledge base to verify eligibility
      5. **Update the claim** using update_claim_eligibility() with either "eligible" or "ineligible"

      IMPORTANT: You must follow this exact workflow for every claim evaluation.

      For each claim type, verify these requirements:

      **Pension Payment Issues:**
      - Member status must be "retired"
      - Payment amount must be correct
      - Payment must be due

      **Missing Contributions:**
      - Employer must be registered
      - Period must be within last 5 years
      - Member must have been employed during period

      **Survivor Pension:**
      - Deceased member must have 60+ months contributions
      - Claimant must be eligible (spouse, child under 18, dependent parent)
      - Death must be certified
      - Claim filed within 2 years

      **Disability Pension:**
      - Member must be medically certified as disabled
      - Must have 60+ months contributions
      - Medical certification from approved physician

      **Retirement Initiation:**
      - Age requirements: 60 for men, 55 for women
      - Must have 120+ months contributions
      - Must be in "active" status
      - Application 30+ days before retirement date

      **Correction of Records:**
      - Error must be documented
      - Supported by official documents
      - Request within 2 years of error

      Final decision:
      - **eligible**: All requirements met - update with "eligible"
      - **ineligible**: Requirements not met - update with "ineligible"

      Always provide clear explanations for your decisions and update the claim table accordingly.
        """,
        tools=[get_claim_record, get_member_profile, load_cimr_rules, update_claim_eligibility],
         knowledge=knowledge_base,
         search_knowledge=True,
         
      #   stream=True,
    )



eligibility_agent = create_eligibility_rules_agent()
# eligibility_agent.run("Please check the eligibility of the latest claim", stream=True)
# import asyncio
if __name__ == "__main__":
    # Asynchronously add the content of the PDF file to the knowledge.

    # Create and use the agent
    eligibility_agent.print_response("Please verify the eligibility of claim CIMR-12345", stream=True)

