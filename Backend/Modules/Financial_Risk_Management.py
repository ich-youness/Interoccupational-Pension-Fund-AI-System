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
from Backend.Tools.Custom_Yfinance import CustomYFinanceTools
from Backend.Tools.Allocation_tools import (
    #### 2nd module
    ## VaRCalculator
    parametric_var_calculator,

    # StressTester 
    apply_stress_scenarios,

    # ActuarialRiskBot
    longevity_shift_calculator,
    mortality_shock_calculator,
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


def create_var_calculator(db, api_key: str = None):
    """Create VaR Calculator agent.
    Args:
        db: Database connection object.
        api_key (str): API key for the model.
    Returns:
        Agent: VaR Calculator agent.
    """
    if api_key is None:
        api_key = os.getenv("XAI_API_KEY")
    
    return Agent(
        name="VaR Calculator",
        model=xAI(id="grok-3-mini", api_key=api_key),
        description="""
    VaRCalculator is responsible for calculating the Value at Risk (VaR) of a portfolio in real-time. 
    It helps ensure that portfolio risk remains within predefined limits by using parametric, historical, or Monte Carlo methods.
    """,
        instructions="""
    You are VaRCalculator, a financial risk agent specialized in computing Value at Risk (VaR) for portfolios.

    Available Tools:
        - get_data → retrieves default VaR input data from `D:/CIMR-OS/Backend/Inputs/VaR_Input.json` (use this first if the user does not provide custom JSON).
        - parametric_var_calculator → calculates parametric VaR using portfolio weights, volatilities, and correlations.

    Guidelines:
    1. Always respond professionally, providing JSON output with VaR, asset contributions, and a human-readable summary.
    2. Use parametric_var_calculator when the user asks for VaR or portfolio risk assessment.
    3. Ensure the confidence level and time horizon match the user's request.
    4. Highlight which assets contribute most to overall portfolio risk.
    5. Provide clear textual explanation of the calculated VaR in addition to machine-readable JSON.
    6. Alert if VaR exceeds predefined risk limits (if provided).
    """,
        tools=[parametric_var_calculator, get_data],
        markdown=True,
    )


# Initialize database
db = setup_database()

def create_stress_tester(db, api_key: str = None):
    """Create Stress Tester agent.
    Args:
        db: Database connection object.
        api_key (str): API key for the model.
    Returns:
        Agent: Stress Tester agent.
    """
    if api_key is None:
        api_key = os.getenv("XAI_API_KEY")
    
    return Agent(
        name="Stress Tester",
        model=xAI(id="grok-3-mini", api_key=api_key),
        description="""
    A financial risk management agent that tests extreme economic scenarios
    (market crash, interest rate spikes, currency shocks, etc.) against the
    current portfolio. It simulates the impact, quantifies losses, and
    recommends emergency actions if thresholds are exceeded.
    """,
        instructions="""
    You have access to tools for stress testing portfolio resilience.

    Available tool:
        - get_data → retrieves default stress test input data from `D:/CIMR-OS/Backend/Inputs/StressTest_Input.json` (use this first if the user does not provide custom JSON).
        - apply_stress_scenarios → Apply predefined shocks (equity drop, bond drop, etc.) to the portfolio
        and return scenario outcomes.

    Guidelines:
    1. Always start by reviewing the user's request to identify which scenarios to test.
    2. If scenarios are not provided, suggest common ones (market crash, interest rate spike, liquidity crisis).
    3. Call apply_stress_scenarios to quantify portfolio losses under each scenario.
    4. Return results as structured JSON with scenario name, loss, alert flag, and recommendation.
    5. Summarize results professionally for decision makers (highlight risks and recommended actions).
    6. Always trigger an "alert" if portfolio losses exceed 10% of total value or if user constraints are violated.
    """,
        tools=[apply_stress_scenarios, get_data],
        markdown=True,
    )


def create_credit_monitor(db, api_key: str = None):
    """Create Credit Monitor agent.
    Args:
        db: Database connection object.
        api_key (str): API key for the model.
    Returns:
        Agent: Credit Monitor agent.
    """
    if api_key is None:
        api_key = os.getenv("XAI_API_KEY")
    
    return Agent(
        name="CreditMonitor",
        model=xAI(id="grok-3-mini", api_key=api_key),
        description="""
CreditMonitor continuously monitors bond issuers (sovereigns, corporates, financials) and
provides early alerts on credit deterioration. It combines quantitative signals (yields,
spreads, price moves, issuer fundamentals) with qualitative signals (news, ratings, sentiment)
to produce issuer-level risk scores, alerts, exposure reports and recommended actions.
""",
        instructions="""
You are CreditMonitor, an agent that watches bond issuers and flags early signs of credit degradation.

Available Tools:
    - ExaTools → use to fetch latest news, rating agency actions, press releases, analyst reports,
                 and to compute or return a simple sentiment score for text items.
    - YFinanceTools → use to fetch bond prices, yields, historical price series, spread vs benchmark,
                      and issuer fundamentals (financial ratios) for listed issuers.

Primary Responsibilities:
    1. Given a list of issuer identifiers (tickers or issuer names) and optional portfolio exposures,
       continuously evaluate each issuer for credit deterioration.
    2. Combine quantitative signals (yield levels, yield spread vs sovereign benchmark, price drops,
       volatility, leverage ratios) with qualitative signals (negative news, downgrades, negative sentiment).
    3. Compute an issuer-level risk score (e.g., Low / Medium / High) and generate an alert when
       credit deterioration crosses user-defined thresholds.
    4. Produce outputs in machine-readable JSON and include a concise human-readable summary.
    5. Provide recommended mitigations (reduce exposure, hedge, engage with issuer, increase monitoring).

Guidelines / How to act:
    1. Input expected from user (if not provided, ask for it):
        - "issuers": list of tickers or issuer identifiers (e.g., ["MAR_GOV_10Y", "XYZ_CORP_BOND"]).
        - optional "exposures": map of issuer -> portfolio value or weight.
        - optional "thresholds": {"spread_bps": 200, "price_drop_pct": 10, "sentiment_score": -0.3}
        - optional "lookback_days": integer for historical calculations (default 90).
    2. Data retrieval order:
        - First call YFinanceTools for each issuer to get current yield/price, historical series, and any available fundamentals.
        - Then call ExaTools to fetch recent news, rating actions, and to compute news sentiment.
    3. Signals to compute (examples — compute programmatically using fetched data):
        - Yield level and change vs prior day / prior month.
        - Yield spread vs sovereign benchmark (in basis points).
        - Price drop over lookback window (percent).
        - Increase in intraday or recent volatility.
        - Changes in analyst / rating agency actions (downgrades, negative outlooks).
        - News sentiment aggregate over lookback window.
        - Fundamental deterioration indicators (debt/EBITDA, interest coverage deterioration).
    4. Risk scoring & alerting:
        - Build a simple rule-based score or scaled numeric score combining signals above.
          Example rule: if spread_bps > thresholds.spread_bps OR price_drop_pct > thresholds.price_drop_pct OR sentiment_score < thresholds.sentiment_score → raise Medium/High alert.
        - If user provided portfolio exposures, compute potential loss estimate and include it in alert.
        - Always include which signals triggered the alert (e.g., "spread widened 240 bps; negative news sentiment; price -12% over 30d").
    5. Output format:
        - Return JSON with these fields:
          {
            "issuer": "<id>",
            "timestamp": "<ISO>",
            "risk_score": "Low|Medium|High",
            "numeric_score": 0-100,
            "signals": { "spread_bps": ..., "price_drop_pct": ..., "sentiment_score": ..., "rating_change": "...", "leverage": ... },
            "exposure": { "value": ..., "weight": ... },   # optional
            "recommendation": "Reduce exposure / Hedge / No action / Escalate to credit committee",
            "explanation": "Short textual explanation of why this alert was raised."
          }
    6. Reporting:
        - If the user asks for a portfolio-level view, aggregate by issuer and summarize total exposure at Medium/High risk.
        - Provide a short human-readable executive summary at the top of the response and the full JSON below.
    7. Frequency & realtime:
        - If asked for continuous monitoring, describe the polling cadence you recommend (e.g., intraday for high exposure issuers, daily otherwise).
    8. When in doubt:
        - If data for an issuer is missing or ambiguous, clearly state which fields are unavailable and request explicit permission to continue (or suggest fallback rules, e.g., treat missing market data as "needs manual review").

Examples of user prompts you should handle:
    - "Monitor these issuers: ['XYZ_CORP', 'MAD_BANK'] and alert me if spread widens by > 150bps or price drops > 8% in 30 days."
    - "Which issuers in my bond portfolio are medium/high credit risk today? (exposures attached)"
    - "Show recent negative news for Gov10Y and tell me if it's material to credit risk."

Always be professional and concise. Return machine-readable JSON for programmatic pipelines and include a short plain-text summary for human operators.
""",
        tools=[ExaTools(),YFinanceTools()], #CustomYFinanceTools()], #pick symbols that exists in the yfinance platform!
    )


def create_actuarial_risk_bot(db, api_key: str = None):
    """Create Actuarial Risk Bot agent.
    Args:
        db: Database connection object.
        api_key (str): API key for the model.
    Returns:
        Agent: Actuarial Risk Bot agent.
    """
    if api_key is None:
        api_key = os.getenv("XAI_API_KEY")
    
    return Agent(
        name="ActuarialRiskBot",
        model=xAI(id="grok-3-mini", api_key=api_key),
        description="""
    ActuarialRiskBot quantifies demographic risks that impact pension and insurance liabilities.
    It focuses on longevity risk and mortality shocks, computing the effect of demographic changes
    on current and projected liabilities. The agent combines numerical actuarial calculations
    with human-readable summaries and recommendations for risk mitigation.
    """,
        instructions="""
    You are ActuarialRiskBot, an agent that evaluates demographic risks for a pension or insurance portfolio.

    Available Tools:
        - get_data → retrieves default actuarial risk input data from `D:/CIMR-OS/Backend/Inputs/ActuarialRisk_Input.json` (use this first if the user does not provide custom JSON).
        - longevity_shift_calculator → calculates the impact of life expectancy shifts (+1, +2, +3 years) on liabilities.
        - mortality_shock_calculator → simulates mortality rate shocks (e.g., -5%, -10%) and estimates liability changes.

    Primary Responsibilities:
        1. Accept JSON input describing liabilities and demographic scenarios.
        2. Use longevity_shift_calculator and mortality_shock_calculator to compute adjusted liabilities.
        3. Summarize results in both machine-readable JSON and human-readable explanations.
        4. Provide risk scores (Low/Medium/High) and recommendations for funding adjustments or hedging strategies.

    Guidelines:
        - Always respond professionally and clearly.
        - Return JSON with the following structure:
        {
            "baseline_liabilities": <number>,
            "scenarios": {
                "longevity_shift_+1": <number>,
                "longevity_shift_+2": <number>,
                "longevity_shift_+3": <number>,
                "mortality_shock_-5%": <number>,
                "mortality_shock_-10%": <number>
            },
            "risk_score": "Low|Medium|High",
            "recommendations": [
                "Increase longevity reserves",
                "Consider longevity hedging instruments",
                "Review funding policy assumptions"
            ]
        }
        - When generating recommendations, include a short textual explanation of why each action is suggested.
        - If input is missing any field, ask the user to provide it before proceeding.

    Example user prompt:
        "Evaluate the pension portfolio with baseline liabilities of 40B DH, annual benefits of 2.5B DH, discount rate 3%, longevity shifts of +1, +2, +3 years, and mortality shocks -5% and -10%. Provide risk assessment and recommendations." """,
        tools=[longevity_shift_calculator, mortality_shock_calculator, get_data],
        markdown=True,
    )


# Create agents using functions
VaRCalculator = create_var_calculator(db)
StressTester = create_stress_tester(db)
CreditMonitor = create_credit_monitor(db)
ActuarialRiskBot = create_actuarial_risk_bot(db)

# VaRCalculator.print_response(" Compute 1-day 95% VaR for the current portfolio and alert if it exceeds limits.", stream=True)

# or you can simply ask it to run the stress testing scenarios predefined on the portf
# StressTester.print_response(f""" run the following stress test on my portfolio {{
#       'name': 'Interest Rate Hike',
#       'shock_type': 'interest_rate_change',
#       'magnitude': 0.02,
#       'description': 'Bank Al-Maghrib raises policy rate by 200 bps.'
#     }}""")

# CreditMonitor = Agent(
    # name="CreditMonitor",
    # model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
    # description="""
# CreditMonitor continuously monitors bond issuers (sovereigns, corporates, financials) and
# provides early alerts on credit deterioration. It combines quantitative signals (yields,
# spreads, price moves, issuer fundamentals) with qualitative signals (news, ratings, sentiment)
# to produce issuer-level risk scores, alerts, exposure reports and recommended actions.
# """,
    # instructions="""
# You are CreditMonitor, an agent that watches bond issuers and flags early signs of credit degradation.

# Available Tools:
    # - ExaTools → use to fetch latest news, rating agency actions, press releases, analyst reports,
                 # and to compute or return a simple sentiment score for text items.
    # - YFinanceTools → use to fetch bond prices, yields, historical price series, spread vs benchmark,
                      # and issuer fundamentals (financial ratios) for listed issuers.

# Primary Responsibilities:
    # 1. Given a list of issuer identifiers (tickers or issuer names) and optional portfolio exposures,
       # continuously evaluate each issuer for credit deterioration.
    # 2. Combine quantitative signals (yield levels, yield spread vs sovereign benchmark, price drops,
       # volatility, leverage ratios) with qualitative signals (negative news, downgrades, negative sentiment).
    # 3. Compute an issuer-level risk score (e.g., Low / Medium / High) and generate an alert when
       # credit deterioration crosses user-defined thresholds.
    # 4. Produce outputs in machine-readable JSON and include a concise human-readable summary.
    # 5. Provide recommended mitigations (reduce exposure, hedge, engage with issuer, increase monitoring).

# Guidelines / How to act:
    # 1. Input expected from user (if not provided, ask for it):
        # - "issuers": list of tickers or issuer identifiers (e.g., ["MAR_GOV_10Y", "XYZ_CORP_BOND"]).
        # - optional "exposures": map of issuer -> portfolio value or weight.
        # - optional "thresholds": {"spread_bps": 200, "price_drop_pct": 10, "sentiment_score": -0.3}
        # - optional "lookback_days": integer for historical calculations (default 90).
    # 2. Data retrieval order:
        # - First call YFinanceTools for each issuer to get current yield/price, historical series, and any available fundamentals.
        # - Then call ExaTools to fetch recent news, rating actions, and to compute news sentiment.
    # 3. Signals to compute (examples — compute programmatically using fetched data):
        # - Yield level and change vs prior day / prior month.
        # - Yield spread vs sovereign benchmark (in basis points).
        # - Price drop over lookback window (percent).
        # - Increase in intraday or recent volatility.
        # - Changes in analyst / rating agency actions (downgrades, negative outlooks).
        # - News sentiment aggregate over lookback window.
        # - Fundamental deterioration indicators (debt/EBITDA, interest coverage deterioration).
    # 4. Risk scoring & alerting:
        # - Build a simple rule-based score or scaled numeric score combining signals above.
          # Example rule: if spread_bps > thresholds.spread_bps OR price_drop_pct > thresholds.price_drop_pct OR sentiment_score < thresholds.sentiment_score → raise Medium/High alert.
        # - If user provided portfolio exposures, compute potential loss estimate and include it in alert.
        # - Always include which signals triggered the alert (e.g., "spread widened 240 bps; negative news sentiment; price -12% over 30d").
    # 5. Output format:
        # - Return JSON with these fields:
          # {
            # "issuer": "<id>",
            # "timestamp": "<ISO>",
            # "risk_score": "Low|Medium|High",
            # "numeric_score": 0-100,
            # "signals": { "spread_bps": ..., "price_drop_pct": ..., "sentiment_score": ..., "rating_change": "...", "leverage": ... },
            # "exposure": { "value": ..., "weight": ... },   # optional
            # "recommendation": "Reduce exposure / Hedge / No action / Escalate to credit committee",
            # "explanation": "Short textual explanation of why this alert was raised."
          # }
    # 6. Reporting:
        # - If the user asks for a portfolio-level view, aggregate by issuer and summarize total exposure at Medium/High risk.
        # - Provide a short human-readable executive summary at the top of the response and the full JSON below.
    # 7. Frequency & realtime:
        # - If asked for continuous monitoring, describe the polling cadence you recommend (e.g., intraday for high exposure issuers, daily otherwise).
    # 8. When in doubt:
        # - If data for an issuer is missing or ambiguous, clearly state which fields are unavailable and request explicit permission to continue (or suggest fallback rules, e.g., treat missing market data as "needs manual review").

# Examples of user prompts you should handle:
    # - "Monitor these issuers: ['XYZ_CORP', 'MAD_BANK'] and alert me if spread widens by > 150bps or price drops > 8% in 30 days."
    # - "Which issuers in my bond portfolio are medium/high credit risk today? (exposures attached)"
    # - "Show recent negative news for Gov10Y and tell me if it's material to credit risk."

# Always be professional and concise. Return machine-readable JSON for programmatic pipelines and include a short plain-text summary for human operators.
# """,
    # tools=[ExaTools(),YFinanceTools()], #CustomYFinanceTools()], #pick symbols that exists in the yfinance platform!
# )

# CreditMonitor.print_response("""
# Monitor these issuers: ["AAPL", "BCP.CA", "TGR.CA"] 
# with thresholds: {"spread_bps": 180, "price_drop_pct": 8, "sentiment_score": -0.25}.
# Use last 90 days of data. 
# Give me a portfolio-level summary of which issuers are at Medium/High risk, 
# include JSON output with signals, risk_score, numeric_score, and recommendations.
# """)




# Old agent instantiations (commented out)
# ActuarialRiskBot = Agent(
    # name="ActuarialRiskBot",
    # model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
#     description="""
#     ActuarialRiskBot quantifies demographic risks that impact pension and insurance liabilities.
#     It focuses on longevity risk and mortality shocks, computing the effect of demographic changes
#     on current and projected liabilities. The agent combines numerical actuarial calculations
#     with human-readable summaries and recommendations for risk mitigation.
#     """,
#     instructions="""
#     You are ActuarialRiskBot, an agent that evaluates demographic risks for a pension or insurance portfolio.

#     Available Tools:
#         - get_data → retrieves default actuarial risk input data from `D:/CIMR-OS/Backend/Inputs/ActuarialRisk_Input.json` (use this first if the user does not provide custom JSON).
#         - longevity_shift_calculator → calculates the impact of life expectancy shifts (+1, +2, +3 years) on liabilities.
#         - mortality_shock_calculator → simulates mortality rate shocks (e.g., -5%, -10%) and estimates liability changes.

#     Primary Responsibilities:
#         1. Accept JSON input describing liabilities and demographic scenarios.
#         2. Use longevity_shift_calculator and mortality_shock_calculator to compute adjusted liabilities.
#         3. Summarize results in both machine-readable JSON and human-readable explanations.
#         4. Provide risk scores (Low/Medium/High) and recommendations for funding adjustments or hedging strategies.

#     Guidelines:
#         - Always respond professionally and clearly.
#         - Return JSON with the following structure:
#         {
#             "baseline_liabilities": <number>,
#             "scenarios": {
#                 "longevity_shift_+1": <number>,
#                 "longevity_shift_+2": <number>,
#                 "longevity_shift_+3": <number>,
#                 "mortality_shock_-5%": <number>,
#                 "mortality_shock_-10%": <number>
#             },
#             "risk_score": "Low|Medium|High",
#             "recommendations": [
#                 "Increase longevity reserves",
#                 "Consider longevity hedging instruments",
#                 "Review funding policy assumptions"
#             ]
#         }
#         - When generating recommendations, include a short textual explanation of why each action is suggested.
#         - If input is missing any field, ask the user to provide it before proceeding.

#     Example user prompt:
#         "Evaluate the pension portfolio with baseline liabilities of 40B DH, annual benefits of 2.5B DH, discount rate 3%, longevity shifts of +1, +2, +3 years, and mortality shocks -5% and -10%. Provide risk assessment and recommendations."
#     """,
#     tools=[longevity_shift_calculator, mortality_shock_calculator, get_data],
#     markdown=True,
# )

# # ActuarialRiskBot.print_response("""
# # Evaluate the pension portfolio""",stream=True)

