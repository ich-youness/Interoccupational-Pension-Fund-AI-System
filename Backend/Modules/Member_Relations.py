from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.models.xai import xAI
from agno.tools.file import FileTools
from agno.tools.exa import ExaTools
from agno.tools.yfinance import YFinanceTools


from dotenv import load_dotenv
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

load_dotenv()

# from Backend.Tools.Allocation_tools import (
#     #2nd agent
# )

def get_data(path: str):
    """Tool to read JSON data from a file.
    Args:
        path (str): Path to the JSON file.
    Returns:
        str: Contents of the JSON file as a string.
    """
    with open(path, "r") as f:
        return f.read()


def setup_database(db_file: str = "tmp/agno.db"):
    """Setup database connection.
    Args:
        db_file (str): Path to database file.
    Returns:
        SqliteDb: Database connection object.
    """
    return SqliteDb(db_file=db_file)


def create_cimr_chatbot(db, api_key: str = None):
    """Create CIMR Chatbot agent.
    Args:
        db: Database connection object.
        api_key (str): API key for the model.
    Returns:
        Agent: CIMR Chatbot agent.
    """
    if api_key is None:
        api_key = os.getenv("XAI_API_KEY")
    
    return Agent(
        name="CIMR Chatbot",
        db=db,
        model=xAI(id="grok-3-mini", api_key=api_key),
        description="""
    A 24/7 virtual assistant for CIMR members that automatically handles the majority of inquiries.
    It provides accurate, professional answers regarding membership, pensions, contributions, regulations, forms, and general fund information.
    Escalates only complex or unusual cases to human agents.
    """,
        instructions="""
    You are CIMRChatbot, a virtual assistant for CIMR members.

    Your role:
    - Answer inquiries related to personal membership, pension projections, contributions, rules, forms, and general fund information.
    - Provide concise, professional, and accurate responses.
    - Escalate only when the inquiry cannot be resolved automatically.


    Guidelines:
    0. use get_data to  get the data you can use to answer the member's inquiry, here is the path for that file `D:/CIMR-OS/Backend/Inputs/CIMRChatbot_Input.json`.
    1. Always start by reviewing the member's input JSON, which includes personal info, account info, retirement info, rules, forms, general information, and the inquiry text.
    2. Use the provided data to generate responses. Do not guess member-specific data outside of the JSON input.
    3. For inquiries about:
    - Account or membership → provide balance, status, or info from account_info and personal_info.
    - Pension or retirement → calculate or summarize based on retirement_info.
    - Contributions → summarize payments, pending contributions, or schedule.
    - Rules & regulations → provide guidance based on rules_and_regulations.
    - Forms → provide instructions or list relevant forms.
    - General info → summarize fund performance, investment overview, FAQs.
    4. Always respond in a professional way and provide summaries, tables, or step-by-step guidance when relevant.
    5. If the inquiry cannot be answered with the data provided, politely indicate this and suggest the member contact a human agent.
    6. Maintain context across conversations to provide coherent multi-turn interactions.
    """,
        add_history_to_context=True,
        tools=[get_data]
    )


def create_pension_simulator(db, api_key: str = None):
    """Create Pension Simulator agent.
    Args:
        db: Database connection object.
        api_key (str): API key for the model.
    Returns:
        Agent: Pension Simulator agent.
    """
    if api_key is None:
        api_key = os.getenv("XAI_API_KEY")
    
    return Agent(
        name="Pension Simulator",
        db=db,
        model=xAI(id="grok-3-mini", api_key=api_key),
        description="""
A real-time, personalized retirement projection agent for CIMR members.
Calculates projected pensions at different retirement ages, considers early/late retirement, partial retirement, contributions, salary history, and economic assumptions.
Provides detailed and structured outputs for decision making.
""",
        instructions="""
You are PensionSimulator, an AI agent that provides personalized retirement projections.

Guidelines:
1. Always start by reviewing the member's JSON input, which includes personal_info, account_info, retirement_info, and economic_assumptions.
2. Compute projected monthly and annual pensions based on:
   - Current contributions and reserves
   - Salary history and growth
   - Expected investment returns (equities, bonds)
   - Inflation
   - Retirement age options (early, normal, late)
   - Partial retirement options if available
3. Provide results as structured JSON including:
   - projected_monthly_pension
   - projected_annual_pension
   - early_retirement_projection (if applicable)
   - late_retirement_projection (if applicable)
4. Summarize projections clearly in tables or bullet points for the user.
5. If requested, simulate alternative economic scenarios and show their impact on pension amounts.
6. Always respond professionally, and never guess member-specific data outside the input JSON.
""",
        add_history_to_context=True,
    )


def create_fraud_detector(db, api_key: str = None):
    """Create Fraud Detector agent.
    Args:
        db: Database connection object.
        api_key (str): API key for the model.
    Returns:
        Agent: Fraud Detector agent.
    """
    if api_key is None:
        api_key = os.getenv("XAI_API_KEY")
    
    return Agent(
        name="Pension Fraud Detector",
        db=db,
        model=xAI(id="grok-3-mini", api_key=api_key),
        description="""
An AI agent that detects suspicious or fraudulent pension activity for CIMR members.
It identifies anomalies in contributions, pension payments, early/partial retirements, duplicate records, and rule violations, providing actionable alerts to prevent financial losses.
""",
        instructions="""
You are FraudDetector, an AI agent that identifies potential pension fraud.

Guidelines:
1. Review the member's JSON input, including personal_info, account_info, retirement_info, transaction_history, and rules_and_constraints.
2. Analyze the data to detect anomalies or suspicious activity, such as:
   - Duplicate claims or multiple entries for the same member
   - Inconsistent contribution or payment history
   - Early/partial retirement claims violating rules
   - Excessive or unusual pension projections
   - Rule violations (e.g., minimum contribution years, maximum pension limits)
3. Return results as structured JSON:
   - fraud_detected: true/false
   - fraud_type: string (e.g., duplicate_claim, overpayment, invalid_member_data, rule_violation)
   - alert_message: explanation of the anomaly
   - recommended_action: suggested next steps (manual review, suspension, notification)
4. Always provide a professional explanation and actionable recommendations.
5. Escalate only if fraud_detected is true.
""",
        add_history_to_context=True,
    )


def create_retirement_planner(db, api_key: str = None):
    """Create Retirement Planner agent.
    Args:
        db: Database connection object.
        api_key (str): API key for the model.
    Returns:
        Agent: Retirement Planner agent.
    """
    if api_key is None:
        api_key = os.getenv("XAI_API_KEY")
    
    return Agent(
        name="Retirement Planner",
        db=db,
        model=xAI(id="grok-3-mini", api_key=api_key),
        description="""
An AI agent that provides personalized retirement advice and tailored savings plans for CIMR members.
It evaluates member data, pension projections, and economic assumptions to recommend actionable retirement strategies.
""",
        instructions="""
You are RetirementPlanner, an AI agent that offers personalized retirement guidance.

Available Tools:
    - get_data → retrieves default retirement planning input data from `D:/CIMR-OS/Backend/Inputs/RetirementPlanner_Input.json` 
      (use this first if the user does not provide custom JSON).

Guidelines:
1. Always start by using get_data to read the member's input data if no custom JSON is provided.
2. Evaluate personal_info, account_info, retirement_info, economic_assumptions, and user_goals.
3. Provide retirement advice, including:
   - Recommended contribution plan to meet goals
   - Suggested adjustments to investment profile
   - Projections of monthly and annual pensions
   - Partial or early retirement options
4. Return results as structured JSON:
   - advice_summary
   - recommended_savings_plan
   - pension_projection
   - risk_warnings
5. Summarize results professionally and clearly for the member.
6. Always provide actionable recommendations and flag potential risks.
""",
        tools=[get_data],
        add_history_to_context=True,
    )


# Initialize database
db = setup_database()

# Create agents using functions
CIMRChatbot = create_cimr_chatbot(db)


# CIMRChatbot.print_response("How do I check my pension projection?")

PensionSimulator = create_pension_simulator(db)


# PensionSimulator.print_response("""
# {
#   "member_id": "CIMR123456",
#   "personal_info": {
#     "first_name": "Mohamed",
#     "last_name": "Elhaj",
#     "date_of_birth": "1970-05-15",
#     "membership_status": "active",
#     "years_of_service": 30,
#     "average_salary": 240000
#   },
#   "account_info": {
#     "current_reserve": 4500000,
#     "contributions_paid": 900000
#   },
#   "retirement_info": {
#     "desired_retirement_age": 62,
#     "early_retirement_age": 60,
#     "late_retirement_age": 65,
#     "partial_retirement_options": true
#   },
#   "economic_assumptions": {
#     "expected_equity_return": 0.07,
#     "expected_bond_return": 0.03,
#     "inflation_rate": 0.025,
#     "salary_growth_rate": 0.03
#   }
# }
# """)

FraudDetector = create_fraud_detector(db)

# FraudDetector.print_response("""
# {
#   "member_id": "CIMR123456",
#   "personal_info": {
#     "first_name": "Mohamed",
#     "last_name": "Elhaj",
#     "date_of_birth": "1970-05-15",
#     "membership_status": "active"
#   },
#   "account_info": {
#     "current_reserve": 4500000,
#     "contributions_paid": 900000,
#     "last_contribution_date": "2025-08-31",
#     "pending_contributions": 0
#   },
#   "retirement_info": {
#     "projected_retirement_age": 62,
#     "projected_pension": 12000,
#     "early_retirement_options": {"available": true, "penalty_rate": 0.15},
#     "partial_retirement_options": {"available": true, "minimum_age": 60}
#   },
#   "transaction_history": [
#     {"type": "pension_payment", "amount": 12000, "date": "2025-09-01"},
#     {"type": "pension_payment", "amount": 12000, "date": "2025-09-01"},
#     {"type": "contribution", "amount": 5000, "date": "2025-08-31"}
#   ],
#   "flags_and_alerts": [],
#   "rules_and_constraints": {
#     "maximum_early_retirement_penalty": 0.15,
#     "minimum_contribution_years": 10,
#     "maximum_monthly_pension": 15000
#   }
# }
# """)



RetirementPlanner = create_retirement_planner(db)

# RetirementPlanner.print_response("""
# Please provide a personalized retirement plan for the member.

# Summarize the recommended savings plan, projected pension, and any potential risks.
# """)
