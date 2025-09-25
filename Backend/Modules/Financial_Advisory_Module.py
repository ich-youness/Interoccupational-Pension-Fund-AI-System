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
from agno.tools.calculator import CalculatorTools
from agno.vectordb.lancedb import LanceDb
import matplotlib.pyplot as plt



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

# from Backend.Tools. import *
    #2nd agent


def setup_database(db_file: str = "tmp/agno.db"):
    """Setup database connection.
    Args:
        db_file (str): Path to database file.
    Returns:
        SqliteDb: Database connection object.
    """
    return SqliteDb(db_file=db_file)


def create_projection_agent():
    """
    Creates an AI agent to run pension benefit projections based on user profile and assumptions.
    """
    return Agent(
        name="ProjectionAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="Calculates pension projections based on age, salary, contribution years, and retirement age.",
        instructions="""
        You are a pension projection agent. Your task is to calculate and present pension estimates clearly.  

        Steps you MUST follow:

        1. Read the input data provided in the prompt:
        - current_age
        - retirement_age
        - salary (current or average reference)
        - contribution_years
        - contribution_rate (% of salary contributed)
        - salary_growth (optional, default 2%)
        - inflation_rate (optional, default 2%)

        2. Apply a simple projection formula (baseline example):
        - Future Salary = salary × (1 + salary_growth)^(retirement_age - current_age)
        - Accrued Pension = contribution_years × accrual_rate × reference_salary
        - Monthly Pension ≈ Accrued Pension / 12
        - Adjust using inflation_rate for real value

        Assume accrual_rate = contribution_rate / 2. Example: if contribution_rate=10%, accrual_rate=5%.

        3. Output:
        - A summary table with:
            * Retirement Age
            * Projected Final Salary
            * Accrued Pension (annual & monthly)
            * Assumptions used

        4. Present results in a clear, structured way (markdown table).
        """,
        tools=[CalculatorTools()],
        markdown=True,
    )

# --- Example test run ---

projection_agent = create_projection_agent()
test_prompt = """
Run a pension projection with the following data:
current_age: 40
retirement_age: 60
salary: 15000 MAD
contribution_years: 20
contribution_rate: 10%
salary_growth: 3%
inflation_rate: 2%
"""
# projection_agent.print_response(test_prompt, stream=True)


def create_scenario_comparison_agent():
    """
    Creates an AI agent to compare multiple pension projection scenarios.
    """
    return Agent(
        name="ScenarioComparisonAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="Compares multiple pension projection scenarios and highlights differences.",
        instructions="""
    You are a pension scenario comparison agent.  
    Your task is to analyze **two or more projection results** and present the differences clearly.  

    Steps to follow:

    1. Read the scenarios provided in the prompt. Each scenario will include:
    - Retirement age
    - Projected final salary
    - Accrued pension (annual & monthly)
    - Contribution years
    - Assumptions (growth, inflation, rate)

    2. Build a comparison table:
    - Columns = scenarios (Retire at 55, 60, 65…)
    - Rows = metrics (Final Salary, Accrued Pension, Monthly Pension, etc.)

    3. Highlight differences:
    - Compute percentage increase/decrease between scenarios.
    - Example: “Retiring at 60 instead of 55 increases your monthly pension by 25%.”

    4. Provide a clear summary:
    - Which scenario gives the **highest pension**
    - Which gives the **lowest pension**
    - Trade-offs (e.g., more years contributing vs. higher payout)

    5. Output format:
    - Markdown table for comparisons
    - Bullet point summary of key insights
        """,
        tools=[CalculatorTools()],
        markdown=True,
    )

# --- Example test run ---if __name__ == "__main__":
scenario_agent = create_scenario_comparison_agent()
test_prompt = """
Compare these two pension projection scenarios:

Scenario A:
- Retirement age: 55
- Final salary: 18,000 MAD
- Accrued pension: 900,000 MAD
- Monthly pension: 7,500 MAD

Scenario B:
- Retirement age: 60
- Final salary: 21,000 MAD
- Accrued pension: 1,260,000 MAD
- Monthly pension: 10,500 MAD
"""
# scenario_agent.print_response(test_prompt, stream=True)


# --- Configure the Knowledge Base ---
vector_db = LanceDb(
    table_name="cimr_rules_financial",   # dedicated table for financial rules
    uri="tmp/agno_lancedb", 
    embedder=GeminiEmbedder(),
)

knowledge_base = Knowledge(vector_db=vector_db)
knowledge_base.add_content(
    path="D:/CIMR-OS/Backend/Inputs/CIMR_Rules.md",  # your official CIMR rules
)

def create_regulation_integration_agent():
    """
    Creates an AI agent that validates pension projections
    against CIMR official rules and regulations.
    """
    return Agent(
        name="RegulationIntegrationAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="Ensures pension projections comply with CIMR regulations and policies.",
        instructions="""
    You are a CIMR regulation integration agent.  
    Your role is to validate financial projections and scenarios against official CIMR rules.  

    **Workflow:**
    1. Read the input projection or scenario (retirement age, contribution years, salary, etc.).
    2. Query the CIMR rules knowledge base to extract the **regulatory requirements**.
    - Legal retirement ages
    - Minimum contribution months required
    - Conditions for disability/survivor pensions
    - Calculation formulas or caps
    3. Validate the projection against these rules:
    - If compliant → Mark as **valid**, explain why.
    - If not compliant → Mark as **invalid**, and list the broken rules.
    4. Suggest corrections if possible (e.g., “You need 120 months of contributions instead of 100”).

    **Output format:**
    - Compliance status: ✅ Valid / ❌ Invalid
    - Rules checked: (list the exact CIMR rules from the knowledge base)
    - Explanations in plain language
    - Suggestions (if invalid)
        """,
        knowledge=knowledge_base,
        search_knowledge=True,
    )

# --- Example test run ---
# if __name__ == "__main__":
reg_agent = create_regulation_integration_agent()
test_prompt = """
Validate this projection: 
- Retirement age: 55
- Contribution years: 100 months
- Final salary: 20,000 MAD
- Requested pension: 8,000 MAD
"""
# reg_agent.print_response(test_prompt, stream=True)




def create_financial_advisory_agent():
    """
    Creates an AI agent that provides actionable pension advisory insights.
    """
    return Agent(
        name="FinancialAdvisoryAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="Provides personalized pension advice based on projections, comparisons, and user goals.",
        instructions="""
    You are a CIMR financial advisory agent.  
    Your job is to turn pension projections and scenario comparisons into **clear, actionable advice**.

    **Workflow:**
    1. Read the provided projection/comparison data:
    - Contribution levels
    - Retirement ages
    - Expected monthly/annual pension
    - Compliance status (if available)

    2. Identify gaps:
    - Compare current trajectory vs. target income
    - Highlight whether contributions are sufficient or insufficient
    - Spot early/late retirement trade-offs

    3. Generate recommendations:
    - How much to increase contributions for better pension
    - How retiring later/earlier impacts payouts
    - What adjustments (contribution % or years) optimize the outcome

    4. Communicate clearly in **plain language**:
    - Avoid jargon
    - Use concrete numbers when available
    - Provide 2–3 key strategies

    **Output format:**
    - ✅ Key recommendations (bulleted)
    - 📊 Trade-off analysis (retirement age vs. pension amount)
    - 💡 Strategic advice (what to do next)

    Always be practical, concise, and user-focused.
        """,
        markdown=True,
    )

# --- Example test run ---
# if __name__ == "__main__":
#     advisory_agent = create_financial_advisory_agent()
#     test_prompt = """
#     Projection Summary:
#     - Retirement age: 60
#     - Contributions: 30 years at 6% of salary
#     - Final salary: 20,000 MAD
#     - Expected monthly pension: 9,500 MAD
#     - Target pension: 12,000 MAD

#     Please provide financial advice.
#     """
#     advisory_agent.print_response(test_prompt, stream=True)






def create_visualization_agent():
    """
    Creates an AI agent that turns pension projections, scenarios, 
    and advisory outputs into charts and reports.
    """
    return Agent(
        name="VisualizationAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="Transforms pension projections and advisory results into visual outputs (charts, graphs, reports).",
        instructions="""
You are a visualization agent.  
Your job is to take structured pension data (projections, scenarios, recommendations) and output it in a **visual form**.

**Workflow:**
1. Input types:
   - Projection results: {year, contributions, pension}
   - Scenario comparisons: {scenario_name, pension_value}
   - Advisory summary: text recommendations

2. Tasks:
   - Generate a **line chart** for pension growth over years.
   - Generate a **bar chart** comparing scenarios.
   - (Optional) Combine visuals + recommendations into a PDF report.

3. Output requirements:
   - Charts should be clear and labeled (axes, title).
   - Advisory insights should be included as annotations or report text.
   - If user asks for a downloadable report → generate PDF with charts + summary.

4. Always provide a short text summary alongside visuals.
        """,
        markdown=True,
    )


# --- Example test run (chart generation outside LLM) ---
def example_chart():
    years = list(range(2025, 2045))
    contributions = [5000 + i*200 for i in range(20)]
    pension = [0 if i < 10 else (i-9)*1000 for i in range(20)]

    plt.figure(figsize=(8,5))
    plt.plot(years, contributions, label="Contributions", marker="o")
    plt.plot(years, pension, label="Projected Pension", marker="s")
    plt.title("Projection of Contributions vs Pension")
    plt.xlabel("Year")
    plt.ylabel("Amount (MAD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"images/projection_chart{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    plt.close()

# if __name__ == "__main__":
#     vis_agent = create_visualization_agent()
#     vis_agent.print_response("Generate a visualization for pension projections from 2025 to 2045.", stream=True)
#     example_chart()
#     print("✅ Chart saved as projection_chart.png")
