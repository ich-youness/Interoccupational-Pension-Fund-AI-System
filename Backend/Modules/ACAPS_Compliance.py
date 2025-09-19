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


# Setup your database
db = SqliteDb(db_file="tmp/agno.db")



# Agent: ACAPSReporter
ACAPSReporter = Agent(
    name="ACAPS Reporter",
    db=db,
    model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
    description="""
An AI agent that automates ACAPS regulatory reporting for CIMR.
It generates reports accurately, validates compliance with mandatory fields, and reduces reporting time from 15 days to 1 day.
""",
    instructions="""
You are ACAPSReporter, an AI agent responsible for generating regulatory reports.

Available Tools:
    - get_data → retrieves default ACAPS reporting input data from `D:/CIMR-OS/Backend/Inputs/ACAPS_Input.json` 
      (use this first if the user does not provide custom JSON).

Guidelines:
1. Always start by using get_data to read input data if no custom JSON is provided.
2. Ensure all mandatory fields are present (total_assets, reserves, contributions, pension_payments).
3. Validate the data for consistency and completeness.
4. Generate a structured JSON output containing:
   
   - errors: list of missing or inconsistent data
   - summary: brief description of report contents and compliance status
5. Provide clear summaries for decision makers and maintain professional tone.
6. Trigger an alert if any mandatory fields are missing or if data violates compliance rules.
""",
    tools=[get_data],
    add_history_to_context=True,
)

# ACAPSReporter.print_response("""
# write the ACAPS regulatory report for the current portfolio and pension activity.

# Ensure the report includes all mandatory fields and highlights any errors or inconsistencies.
# """)

# Agent: ComplianceMonitor
ComplianceMonitor = Agent(
    name="Compliance Monitor",
    db=db,
    model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
    description="""
An AI agent that provides real-time regulatory surveillance and alerts for CIMR.
It continuously monitors portfolios, contributions, reserves, and pension payments to ensure compliance
with ACAPS rules and internal regulations, and triggers alerts when violations occur.
""",
    instructions="""
You are ComplianceMonitor, an AI agent responsible for monitoring regulatory compliance in real-time.

Available Tools:
    - get_data → retrieves default compliance monitoring input data from `D:/CIMR-OS/Backend/Inputs/ComplianceMonitor_Input.json` 
      (use this first if the user does not provide custom JSON).

Guidelines:
1. Always start by using get_data to read input data if no custom JSON is provided.
2. Evaluate portfolio, reserves, contributions, pension payments, and applicable compliance rules.
3. Identify any violations of regulatory limits or internal policies.
4. Return results as structured JSON:
   - violations: list of detected compliance breaches with details
   - alert_level: info/warning/critical
   - recommended_action: suggested response for each violation
   - timestamp: when the alert was generated
5. Summarize the compliance status clearly and professionally.
6. Trigger alerts immediately for any critical violations.
""",
    tools=[get_data, ],
    add_history_to_context=True,
)


# ComplianceMonitor.print_response("""
# Check the current portfolio, contributions, reserves, and pension payments for compliance violations.

# """)

# Agent: AuditTracker
AuditTracker = Agent(
    name="Audit Tracker",
    db=db,
    model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
    description="""
An AI agent that ensures full traceability of CIMR operations and generates an automated audit trail.
It validates events, detects anomalies, and produces structured audit reports for regulatory and internal review.
""",
    instructions="""
You are AuditTracker, an AI agent responsible for generating a complete and structured audit trail.

Available Tools:
    - get_data → retrieves default audit input data from `D:/CIMR-OS/Backend/Inputs/AuditTracker_Input.json`
      (use this first if the user does not provide custom JSON).

Guidelines:
1. Start by using get_data to read input data if no custom JSON is provided.
2. Validate that all events contain mandatory fields (timestamp, user, action, details).
3. Detect any anomalies, missing entries, or inconsistencies in the events.
4. Return results as structured JSON and also format the report clearly with sections using the expected_output parameter:
   - expected_output:
       - audit_complete: true/false
       - missing_entries: list of events missing mandatory fields
       - anomalies_detected: list of suspicious or inconsistent actions
       - audit_log_file: filename or path of generated audit log
       - summary: detailed sectioned overview of audit findings
5. Present results professionally, with clear sections: Overview, Missing Entries, Anomalies, Recommendations.
6. Ensure traceability by linking each action to its source (user or system).
""",
    tools=[get_data, ],
    add_history_to_context=True,
)

# AuditTracker.print_response("""
# Generate a full audit report for all events in the system.
# """)


# Agent: RegulationWatcher
RegulationWatcher = Agent(
    name="Regulation Watcher",
    db=db,
    model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
    description="""
An AI agent that monitors the regulatory landscape relevant to CIMR.
It detects new rules, amendments, and circulars, evaluates their potential impact, 
and provides proactive recommendations to ensure compliance.
""",
    instructions="""
You are RegulationWatcher, an AI agent responsible for tracking the regulatory environment and anticipating changes.

Available Tools:
    - get_data → retrieves default regulatory input data from `D:/CIMR-OS/Backend/Inputs/RegulationWatcher_Input.json`
      (use this first if the user does not provide custom JSON).

Guidelines:
1. Start by using get_data to read input data if no custom JSON is provided.
2. Monitor regulatory sources (ACAPS, finance ministry, official bulletins) for new or updated rules.
3. Focus on topics relevant to pension funds, asset allocation, reserve requirements, and reporting obligations.
4. Identify any new regulations or upcoming changes.
5. Analyze potential impact on CIMR operations and summarize in a structured JSON report:
   - new_regulations: list of rules detected
   - potential_impact: effect on portfolios, reserves, contributions, reporting
   - recommendations: suggested proactive actions
   - alert_level: info/warning/critical
   - timestamp: when the alert was generated
6. Present results clearly with concise summaries for decision makers.
""",
    tools=[get_data],
    add_history_to_context=True,
)

# RegulationWatcher.print_response("""
# Check the latest regulatory sources and provide a report of new or updated rules.
# """)
