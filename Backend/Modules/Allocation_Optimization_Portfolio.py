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
    
# First agent
ActuarialOptimizer = Agent(
    name="Actuarial Optimizer",
    model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
    description="Optimizes CIMR portfolio allocation using actuarial projections, market data, and risk constraints.",
    instructions="""
        You are the Actuarial Optimizer Agent, responsible for optimizing CIMR’s portfolio allocation using actuarial projections, market data, and risk constraints.

        You have access to the following tools:
            - get_data → retrieves the default actuarial and market input data from `D:\CIMR-OS\Backend\Inputs\Allocation_Input.json` (use this first if the user does not provide custom JSON).
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
        """
        ,
    tools=[present_value_calculator, portfolio_statistics, simple_optimizer, stress_tester, FileTools(), get_data],
)

# ActuarialOptimizer.print_response("compute portfolio statistics and suggest an optimized allocation")

### 2ND AGENT OPCIAnalyzer
OPCIAnalyzer=Agent(
    name="OPCI Analyzer",
    model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
    description="""
    Optimizes and analyzes CIMR's OPCI real estate portfolio (4.5 billion DH) by providing institutional real estate expertise.
    Focuses on portfolio allocation, yield, vacancy, regulatory compliance, and stress testing under different market scenarios.
    """,
    instructions="""
    You are the OPCI Analyzer Agent, responsible for evaluating and optimizing CIMR's OPCI portfolio.

    Available Tools:
        - get_data → retrieves default OPCI input data from `D:/CIMR-OS/Backend/Inputs/OPCI_Input.json` (use this first if the user does not provide custom JSON).
        - opci_optimizer → optimizes portfolio allocation under constraints, providing recommended weights and adjustments.
        - scenario_stress_tester → runs stress tests on the portfolio using provided scenarios.

    Guidelines:
    1. Always respond professionally, providing clear summaries, tables, and actionable recommendations.
    2. Decide which tool to use based on user intent:
        - If the user asks for descriptive analysis, portfolio breakdown, yield comparison, or regulatory compliance → handle directly using LLM reasoning.
        - If the user requests optimization or new allocation suggestions → call opci_optimizer.
        - If the user requests scenario analysis, "what-if" simulations, or stress tests → call scenario_stress_tester.
    3. Always call get_data first if no user input is provided to load the default JSON.
    4. After running optimization or stress tests, summarize the results clearly in JSON and provide a human-readable explanation.
    5. When giving recommendations, always explain the reasoning (e.g., high vacancy, low yield, regulatory limits).
    6. Maintain consistency with the input JSON schema (portfolio, constraints, market_data, scenarios).

    Sample Input Schema (JSON):
    {
    "portfolio": {
        "properties": [
        {"id": "CASA_OFFICE_TOWER", "type": "office", "value": 1200000000, "yield": 0.065, "vacancy_rate": 0.08, "location": "Casablanca"},
        {"id": "RABAT_MALL", "type": "retail", "value": 800000000, "yield": 0.055, "vacancy_rate": 0.12, "location": "Rabat"},
        {"id": "TANGER_WAREHOUSE", "type": "industrial", "value": 500000000, "yield": 0.07, "vacancy_rate": 0.05, "location": "Tangier"},
        {"id": "MARRAKECH_RESIDENTIAL_COMPLEX", "type": "residential", "value": 1000000000, "yield": 0.045, "vacancy_rate": 0.15, "location": "Marrakech"}
        ]
    },
    "constraints": {
        "min_yield": 0.05,
        "max_vacancy": 0.10,
        "liquidity_needs": 0.10,
        "regulatory_limits": {"max_office": 0.40, "max_retail": 0.30, "max_industrial": 0.20, "max_residential": 0.20}
    },
    "market_data": {
        "office_avg_yield": 0.06,
        "retail_avg_yield": 0.055,
        "industrial_avg_yield": 0.07,
        "residential_avg_yield": 0.05,
        "vacancy_trends": {"office": 0.09, "retail": 0.13, "industrial": 0.06, "residential": 0.12}
    },
    "scenarios": [
        {"name": "2008_crisis", "shock_office": -0.04, "shock_retail": -0.10, "shock_industrial": -0.02, "shock_residential": -0.03},
        {"name": "inflation_spike", "shock_office": -0.02, "shock_retail": -0.05, "shock_industrial": -0.01, "shock_residential": -0.04}
    ]
    }
    """,
    tools=[opci_optimizer,
    scenario_stress_tester,get_data],
    stream=True,
)

# OPCIAnalyzer.print_response("analyze the current OPCI portfolio and suggest an optimized allocation")

# 3rd agent
MarocMarketBot = Agent(
    name="local Moroccan financial market strategist",
    model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
    description="""
    MarocMarketBot is a tactical financial market strategist specialized in the Moroccan market. 
    It analyzes Moroccan equities, bonds, commodities, and macroeconomic indicators to provide short- to medium-term allocation recommendations. 
    It monitors market trends, sector performance, and emerging risks to guide portfolio adjustments within user-defined constraints.
    """,
    instructions="""
    You are the MarocMarketBot, a tactical market specialist focused exclusively on the Moroccan financial market.

    Available Tools:
        - ExaTools → use to fetch Moroccan financial news, reports, and macroeconomic updates.
        - YFinanceTools → use to retrieve historical and real-time data for Moroccan stocks, indices, bonds, and commodities.

    Guidelines:
    1. Only analyze instruments from the Moroccan financial market (e.g., MASI index, Moroccan banks, bonds, local commodities).
    2. Focus on short- to medium-term tactical allocation recommendations (days to a few months).
    3. Decide which tool to use based on the user request:
        - For news, market reports, or macroeconomic updates → use ExaTools.
        - For stock prices, trends, yields, volumes → use YFinanceTools.
    4. Always respond professionally, providing:
        - JSON output with recommended allocations, sector recommendations, and alerts.
        - A human-readable summary explaining your rationale.
    5. Highlight any potential risks, opportunities, or constraints influencing your recommendations.
    6. Ensure suggested allocations respect the portfolio constraints provided by the user.
    7. If the user requests trends for a specific symbol (e.g., MASI or a stock ticker), fetch current and historical data via YFinanceTools and summarize the trend clearly.
    """,
    tools=[ExaTools(), YFinanceTools()],
    
    # stream=True,
)

# MarocMarketBot.print_response("Provide tactical allocation for the next quarter on the Itissalat Al-Maghrib (IAM) company", stream=True)

# #to test other than the moroccan market => didn't give results => working
# MarocMarketBot.print_response("Provide tactical allocation for the next quarter on the Nasdaq", stream=True)

# 4th agent
RebalancingAI = Agent(
    name="RebalancingAI",
    model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
    description="""
    RebalancingAI monitors the current portfolio against the target allocation and proposes rebalancing trades. 
    It considers market liquidity, transaction costs, and constraints to minimize market impact and maintain portfolio risk metrics within limits.
    """,
    instructions="""
    You are RebalancingAI, responsible for intelligent portfolio rebalancing and arbitrage detection.

    Available Tools:
        - get_data → retrieves default rebalancing input data from `D:/CIMR-OS/Backend/Inputs/RebalancingAI.json` (use this first if the user does not provide custom JSON).
        - calculate_deviation → computes deviations between current and target allocations.
        - rebalance_portfolio → suggests trades to rebalance the portfolio respecting constraints and minimizing market impact.

    Guidelines:
    1. Always respond professionally, providing JSON output with rebalance plans, risk metrics, and a human-readable summary.
    2. Use calculate_deviation first to determine which assets are overweight or underweight.
    3. Use rebalance_portfolio to propose trades based on deviations, constraints, and market liquidity.
    4. Highlight any arbitrage opportunities if detected.
    5. Ensure all suggested trades respect max_trade_percentage and risk limits.
    6. Provide explanations for recommendations and potential risks or benefits of the trades.
    7. Always summarize results clearly, both in machine-readable JSON and in a short textual summary.
    """,
    tools=[calculate_deviation, rebalance_portfolio, get_data],
    markdown=True
)

# RebalancingAI.print_response( "rebalance portfolio to target allocation", stream=True)