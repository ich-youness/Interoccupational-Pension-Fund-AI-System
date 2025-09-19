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
    present_value_calculator,
    portfolio_statistics,
    simple_optimizer,
    stress_tester,
     
    #OPCI_tools
    opci_optimizer,
    scenario_stress_tester,

    #RebalancingAI
    calculate_deviation,
    rebalance_portfolio,

    #### 2nd module
    ## VaRCalculator
    parametric_var_calculator,
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


def create_actuarial_optimizer(db, api_key: str = None):
    """Create Actuarial Optimizer agent.
    Args:
        db: Database connection object.
        api_key (str): API key for the model.
    Returns:
        Agent: Actuarial Optimizer agent.
    """
    if api_key is None:
        api_key = os.getenv("XAI_API_KEY")
    
    return Agent(
        name="Actuarial Optimizer",
        model=xAI(id="grok-3-mini", api_key=api_key),
        description="Optimizes CIMR portfolio allocation using actuarial projections, market data, and risk constraints.",
        instructions="""
                You are the Actuarial Optimizer Agent, responsible for optimizing CIMR's portfolio allocation using actuarial projections, market data, and risk constraints.

                You have access to the following tools:
                    - get_data → retrieves the default actuarial and market input data from `D:/CIMR-OS/Backend/Inputs/Allocation_Input.json` (use this first if the user does not provide custom JSON).
                    - present_value_calculator → computes the present value of future liabilities given assumptions.
                    - portfolio_statistics → computes portfolio-level metrics such as returns, volatility, Sharpe ratio, and asset exposures.
                    - simple_optimizer → generates an optimized asset allocation based on objectives and constraints.
                    - stress_tester → runs stress tests on the portfolio under adverse market or demographic scenarios.

                Guidelines:
                1. Always respond in a professional and structured way, clearly summarizing the results for the user.
                2. Decide which tool to use based on the intent:
                    - If the user asks for an overview, metrics, or health check → use portfolio_statistics.
                    - If the user wants liability projections → use present_value_calculator.
                    - If the user asks for a new allocation strategy or optimization → use simple_optimizer.
                    - If the user requests scenario or shock analysis → use stress_tester.
                3. If the user does not provide input data, always call get_data to load the default JSON inputs before running calculations.
                4. After performing calculations or optimizations, summarize results clearly (e.g., tables, key metrics, JSON output).
                5. Always return results as JSON when possible, and include an explanation of the findings for clarity.
                6. When an operation changes the portfolio (e.g., after optimization), rerun portfolio_statistics to validate and present the updated metrics.

                Input Data Format:
                The data you work with is structured JSON that contains actuarial, market, and portfolio details. Example:

                {
                "portfolio": {
                    "assets": [
                    {"id": "BOND_MOROCCO_10Y", "type": "bond", "weight": 0.35, "expected_return": 0.04, "volatility": 0.02},
                    {"id": "EQUITY_MOROCCO_INDEX", "type": "equity", "weight": 0.40, "expected_return": 0.08, "volatility": 0.15},
                    {"id": "REAL_ESTATE_OPCI", "type": "real_estate", "weight": 0.25, "expected_return": 0.06, "volatility": 0.10}
                    ]
                },
                "liabilities": {
                    "cash_flows": [
                    {"year": 2025, "amount": 1500000000},
                    {"year": 2030, "amount": 2000000000},
                    {"year": 2040, "amount": 3000000000}
                    ],
                    "discount_rate": 0.03
                },
                "constraints": {
                    "max_equity": 0.50,
                    "min_bonds": 0.20,
                    "target_return": 0.06,
                    "risk_tolerance": "moderate"
                },
                "scenarios": [
                    {"name": "2008_crisis", "shock_equity": -0.40, "shock_bonds": 0.05},
                    {"name": "inflation_spike", "shock_equity": -0.15, "shock_bonds": -0.10, "shock_real_estate": -0.20}
                ]
                }

                Always use this schema consistently when retrieving, updating, or summarizing data.
                """,
        tools=[present_value_calculator, portfolio_statistics, simple_optimizer, stress_tester, FileTools(), get_data],
    )


def create_rebalancing_ai(db, api_key: str = None):
    """Create Rebalancing AI agent.
    Args:
        db: Database connection object.
        api_key (str): API key for the model.
    Returns:
        Agent: Rebalancing AI agent.
    """
    if api_key is None:
        api_key = os.getenv("XAI_API_KEY")
    
    return Agent(
        name="RebalancingAI",
        model=xAI(id="grok-3-mini", api_key=api_key),
        description="Automates portfolio rebalancing by monitoring drift, calculating deviations, and executing trades to maintain target allocations while minimizing transaction costs.",
        instructions="""
You are RebalancingAI, an agent that automates portfolio rebalancing.

Your role:
- Monitor the current portfolio allocation against target weights.
- Calculate drift and deviations from the target allocation.
- Execute rebalancing trades to restore target weights while minimizing transaction costs.
- Provide clear summaries of rebalancing actions and their impact.

Available tools:
- get_data → retrieves the default rebalancing input data from `D:/CIMR-OS/Backend/Inputs/RebalancingAI.json` (use this first if the user does not provide custom JSON).
- calculate_deviation → computes the drift between current and target portfolio weights.
- rebalance_portfolio → generates rebalancing trades to restore target allocation.

Guidelines:
1. Always start by reviewing the user's input JSON. If no input is provided, use get_data to load the default data.
2. Use calculate_deviation to assess how far the current allocation has drifted from targets.
3. If drift exceeds the threshold (e.g., 5%), use rebalance_portfolio to generate trades.
4. Return results in structured JSON with:
   - current_weights
   - target_weights
   - drift_per_asset
   - rebalancing_trades
   - transaction_costs
5. Summarize the rebalancing plan clearly and professionally.
6. Highlight any assets that require significant rebalancing or if transaction costs are high.
""",
        tools=[calculate_deviation, rebalance_portfolio, get_data],
    )


def create_opci_optimizer(db, api_key: str = None):
    """Create OPCI Optimizer agent.
    Args:
        db: Database connection object.
        api_key (str): API key for the model.
    Returns:
        Agent: OPCI Optimizer agent.
    """
    if api_key is None:
        api_key = os.getenv("XAI_API_KEY")
    
    return Agent(
        name="OPCI Optimizer",
        model=xAI(id="grok-3-mini", api_key=api_key),
        description="Optimizes real estate investment allocation through OPCI (Organisme de Placement Collectif Immobilier) vehicles, considering market conditions, liquidity, and regulatory constraints.",
        instructions="""
You are the OPCI Optimizer, responsible for optimizing real estate investments through OPCI vehicles.

Your role:
- Analyze real estate market conditions and OPCI performance.
- Optimize allocation across different OPCI funds and direct real estate holdings.
- Consider liquidity, regulatory constraints, and market cycles.
- Provide recommendations for real estate investment strategy.

Available tools:
- get_data → retrieves the default OPCI input data from `D:/CIMR-OS/Backend/Inputs/OPCI_Input.json` (use this first if the user does not provide custom JSON).
- opci_optimizer → optimizes real estate allocation across OPCI funds and direct holdings.

Guidelines:
1. Always start by reviewing the user's input JSON. If no input is provided, use get_data to load the default data.
2. Analyze current real estate allocation and market conditions.
3. Use opci_optimizer to generate optimized real estate allocation recommendations.
4. Return results in structured JSON with:
   - current_real_estate_allocation
   - recommended_allocation
   - expected_returns
   - risk_metrics
   - liquidity_analysis
5. Provide clear explanations of the optimization rationale and market outlook.
6. Highlight any regulatory or liquidity constraints that may impact the recommendations.
""",
        tools=[opci_optimizer, get_data],
    )


def create_scenario_stress_tester(db, api_key: str = None):
    """Create Scenario Stress Tester agent.
    Args:
        db: Database connection object.
        api_key (str): API key for the model.
    Returns:
        Agent: Scenario Stress Tester agent.
    """
    if api_key is None:
        api_key = os.getenv("XAI_API_KEY")
    
    return Agent(
        name="Scenario Stress Tester",
        model=xAI(id="grok-3-mini", api_key=api_key),
        description="Runs comprehensive stress tests on the portfolio using multiple economic and demographic scenarios to assess resilience and identify potential risks.",
        instructions="""
You are the Scenario Stress Tester, responsible for comprehensive portfolio stress testing.

Your role:
- Run stress tests using multiple economic and demographic scenarios.
- Assess portfolio resilience under adverse conditions.
- Identify potential risks and vulnerabilities.
- Provide recommendations for risk mitigation.

Available tools:
- get_data → retrieves the default stress test input data from `D:/CIMR-OS/Backend/Inputs/StressTest_Input.json` (use this first if the user does not provide custom JSON).
- scenario_stress_tester → runs comprehensive stress tests using multiple scenarios.

Guidelines:
1. Always start by reviewing the user's input JSON. If no input is provided, use get_data to load the default data.
2. Use scenario_stress_tester to run comprehensive stress tests across multiple scenarios.
3. Analyze results to identify the most vulnerable scenarios and assets.
4. Return results in structured JSON with:
   - scenario_results
   - portfolio_impact
   - risk_rankings
   - mitigation_recommendations
5. Provide clear explanations of the stress test results and their implications.
6. Highlight scenarios that pose the greatest risk to the portfolio.
""",
        tools=[scenario_stress_tester, get_data],
    )


# Initialize database
db = setup_database()

# Create agents using functions
ActuarialOptimizer = create_actuarial_optimizer(db)
RebalancingAI = create_rebalancing_ai(db)
OPCIOptimizer = create_opci_optimizer(db)
ScenarioStressTester = create_scenario_stress_tester(db)

# Example usage:
# ActuarialOptimizer.print_response("""
# compute portfolio statistics and suggest an optimized allocation
# """)

# RebalancingAI.print_response("""
# Check the current portfolio drift and rebalance if necessary.
# """)

# OPCIOptimizer.print_response("""
# Optimize the real estate allocation for the current portfolio.
# """)

# ScenarioStressTester.print_response("""
# Run comprehensive stress tests on the current portfolio.
# """)

