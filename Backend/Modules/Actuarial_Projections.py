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

from Backend.Tools.Allocation_tools import (
    #2nd agent
    pension_benefit_calculator,
    present_value_annuity,



)

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


def create_demographic_ai(db, api_key: str = None):
    """Create Demographic AI agent.
    Args:
        db: Database connection object.
        api_key (str): API key for the model.
    Returns:
        Agent: Demographic AI agent.
    """
    if api_key is None:
        api_key = os.getenv("XAI_API_KEY")
    
    return Agent(
        name="DemographicAI",
        model=xAI(id="grok-3-mini", api_key=api_key),
        description="""An AI specialized in demographic and actuarial projections. 
    It generates long-term population and affiliate forecasts up to the year 2100, 
    considering age structures, fertility, mortality, and longevity risks.""",
        instructions="""Always produce structured demographic forecasts with clear breakdowns 
    (e.g., by age groups, dependency ratios). Focus on Morocco and international 
    benchmarks when useful. Provide both narrative explanations and data tables 
    when projecting. For uncertainty, present at least a baseline and one alternative 
    scenario (e.g., high longevity, low fertility).""",
        markdown=True,
    )


def create_pension_calculator(db, api_key: str = None):
    """Create Pension Calculator agent.
    Args:
        db: Database connection object.
        api_key (str): API key for the model.
    Returns:
        Agent: Pension Calculator agent.
    """
    if api_key is None:
        api_key = os.getenv("XAI_API_KEY")
    
    return Agent(
        name="Pension Calculator",
        model=xAI(id="grok-3-mini", api_key=api_key),
        description="""
    Automates pension benefit calculations for instant settlements.
    It computes monthly and annual pension entitlements, applies early retirement penalties,
    checks pension caps, and determines the present value of lifetime annuities
    based on demographic and financial assumptions.
    """,
        instructions="""
    You have access to tools for calculating pensions and present value of annuities.

    Available tools:
        - get_data → retrieves default individual participant data and plan parameters input data from `D:/CIMR-OS/Backend/Inputs/PensionCalculator_Input.json` (use this first if the user does not provide custom JSON).
        - pension_benefit_calculator → Calculates annual and monthly pension entitlements 
          based on service years, salary, accrual rate, retirement age, and caps/penalties.
        - present_value_annuity → Computes the present value of lifetime annuities 
          using discount rates and mortality assumptions.

    Guidelines:
    1. Always begin by checking if the user provided pension input data in JSON format.
       - If no input is provided, request the required fields explicitly.
    2. Use pension_benefit_calculator first to compute the annual and monthly pension.
    3. Pass the annual pension result to present_value_annuity to compute the settlement value.
    4. Return results in structured JSON with fields:
       { "monthly_pension", "annual_pension", "present_value" }.
    5. Summarize results clearly and professionally, explaining how values were derived.
    6. If results exceed pension caps or violate rules, flag the issue with an "alert".
    """,
        tools=[pension_benefit_calculator, present_value_annuity, get_data],
    )


def create_reserve_optimizer(db, api_key: str = None):
    """Create Reserve Optimizer agent.
    Args:
        db: Database connection object.
        api_key (str): API key for the model.
    Returns:
        Agent: Reserve Optimizer agent.
    """
    if api_key is None:
        api_key = os.getenv("XAI_API_KEY")
    
    return Agent(
        name="Reserve Optimizer",
        model=xAI(id="grok-3-mini", api_key=api_key),
        description="Manages and optimizes CIMR's provident reserve to maintain an optimal level of 40+ billion DH while balancing liabilities, returns, and risk.",
        instructions="""
    You are the Reserve Optimizer for CIMR.

    Your role:
    - Maintain the provident reserve at or above 40 billion DH.  
    - Evaluate reserve sustainability given expected inflows (contributions), outflows (benefits), liabilities, and investment returns.  
    - Provide both short-term (1–3 years) and long-term (10–20 years) projections.  
    - Recommend allocation adjustments if the reserve drifts too low or grows excessively.  

    Guidelines:
    1. Always start by reviewing the input JSON, if no input json was given by the user, then us the get_data function to retrieve the input from the file `D:/CIMR-OS/Backend/Inputs/ReserveOptimizer_Input.json`. It should contain at least:  
    - current_reserve (float, DH)  
    - annual_inflows (float, DH)  
    - annual_outflows (float, DH)  
    - expected_return_rate (float, %)  
    - liabilities (float, DH, optional)  
    - projection_horizon (int, years, optional, default=20)  

    2. If no input is provided, assume current_reserve = 40e9, inflows = 3e9, outflows = 2.5e9, return_rate = 4%.  

    3. Perform step-by-step calculations:
    - Reserve_next_year = Reserve_current × (1 + return_rate) + inflows – outflows  
    - Repeat over the projection horizon.  
    - Compare projected reserves against the 40B threshold.  

    4. Provide output in **two formats**:  
    - JSON with projections (per year) and risk flags.  
    - A human-readable executive summary with recommendations.  

    5. Recommendations should include:
    - If reserves fall < 40B → suggest reducing equity exposure, increase contributions, or cut benefits.  
    - If reserves are stable but < 45B → suggest cautious monitoring.  
    - If reserves grow well above 50B → suggest rebalancing into higher-yield investments.  

    Always respond professionally, with both numbers and strategic advice.
    """,
        tools=[get_data],
    )


def create_scenario_planner(db, api_key: str = None):
    """Create Scenario Planner agent.
    Args:
        db: Database connection object.
        api_key (str): API key for the model.
    Returns:
        Agent: Scenario Planner agent.
    """
    if api_key is None:
        api_key = os.getenv("XAI_API_KEY")
    
    return Agent(
        name="Scenario Planner",
        model=xAI(id="grok-3-mini", api_key=api_key),
        description="""
    Generates strategic adaptation plans for the pension scheme by simulating multiple economic,
    demographic, and policy scenarios. Provides actionable recommendations to maintain fund resilience
    and meet regulatory and policy objectives.
    """,
        instructions="""
You are the Scenario Planner for CIMR's pension scheme.

Your role:
- Simulate the pension fund's performance under multiple scenarios (economic, demographic, policy).  
- Assess impacts on reserves, contributions, and pension payouts.  
- Provide adaptation recommendations to maintain fund sustainability.

Available inputs:
- current_reserve (float, DH)
- portfolio_allocation (equity, bonds, real_estate)
- demographics (active_members, retirees, mortality rates)
- economic_forecasts (equity_return, bond_return, inflation)
- policy_constraints (min_reserve, max_equity_allocation, contribution limits)
- scenario_requests (list of scenarios like market_crash, longevity_risk, inflation_spike)

Guidelines:
1. Always review the user's input JSON first. If any key data is missing, ask for it explicitly.
2. For each requested scenario, simulate its impact on reserves, contributions, and pension payouts over the projection horizon.
3. Highlight risks using alerts if reserves fall below the minimum or if policy constraints are violated.
4. Provide recommendations for each scenario:
   - Adjust contributions or benefits
   - Change asset allocation
   - Implement risk mitigation strategies
5. Return output in two formats:
   - JSON with per-scenario projections, alerts, and recommended actions
   - Professional executive summary highlighting key risks and suggested adaptations
6. Present results clearly and concisely for decision-makers.
"""
    )


# Initialize database
db = setup_database()

# Create agents using functions
DemographicAI = create_demographic_ai(db)


# DemographicAI.print_response( "Project the Moroccan population structure up to 2100,     showing age groups 0-14, 15-64, and 65+. Include a baseline and high-longevity scenario.")

PensionCalculator = create_pension_calculator(db)

# PensionCalculator.print_response(
#     """
#     Calculate the pension entitlement and settlement value for the following case:
#      {
#         "service_years": 32,
#         "final_avg_salary": 240000,
#         "accrual_rate": 0.02,
#         "retirement_age": 62,
#         "early_retirement_penalty": 0.03,
#         "pension_cap": 180000,
#         "discount_rate": 0.04,
#         "mortality_table": {
#             "age_62": 0.98,
#             "age_63": 0.97,
#             "age_64": 0.96,
#             "age_65": 0.95,
#             "age_70": 0.90,
#             "age_80": 0.70,
#             "age_90": 0.40
#         }
#     }
   
#     """
# )

ReserveOptimizer = create_reserve_optimizer(db)

# ReserveOptimizer.print_response("""
# Evaluate the reserve sustainability with the following input:
# {
#   "current_reserve": 42000000000,
#   "annual_inflows": 3200000000,
#   "annual_outflows": 2800000000,
#   "expected_return_rate": 0.04,
#   "projection_horizon": 15
# }
# Provide both JSON projections and a clear recommendation.
# """)

from agno.agent import Agent
from agno.models.xai import xAI
import os

ScenarioPlanner = create_scenario_planner(db)

# ScenarioPlanner.print_response("""
# Simulate the following scenarios for the pension fund:

# {
#   "current_reserve": 42000000000,
#   "portfolio_allocation": {
#     "equity": 0.45,
#     "bonds": 0.35,
#     "real_estate": 0.2
#   },
#   "demographics": {
#     "active_members": 120000,
#     "retirees": 40000,
#     "mortality_growth_rate": 0.01
#   },
#   "economic_forecasts": {
#     "equity_return": 0.07,
#     "bond_return": 0.03,
#     "inflation": 0.025
#   },
#   "policy_constraints": {
#     "min_reserve": 40000000000,
#     "max_equity_allocation": 0.5
#   },
#   "scenario_requests": [
#     "market_crash",
#     "longevity_risk",
#     "inflation_spike"
#   ]
# }
# """)

