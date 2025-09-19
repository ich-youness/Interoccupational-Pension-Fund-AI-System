# Example usage in server.py
from Backend.Modules.ACAPS_Compliance import create_acaps_reporter, setup_database

# Initialize database
db = setup_database()

# Create agents
acaps_reporter = create_acaps_reporter(db)
# compliance_monitor = create_compliance_monitor(db)

# Use agents
response = acaps_reporter.print_response("give me the ACAPS report")