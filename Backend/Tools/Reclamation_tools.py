import os
from pyairtable import Api
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_TOKEN = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

# Initialize the Airtable API
api = Api(AIRTABLE_TOKEN)
claims_table = api.table(BASE_ID, "claims_data")

def get_patient_record(claim_id: str):
    """Get a claim record by ID."""
    try:
        # First try to find by claim_id field
        records = claims_table.all(formula=f"{{claim_id}}='{claim_id}'")
        if records:
            return records[0]
        
        # If not found by claim_id field, try by Airtable record ID
        try:
            record = claims_table.get(claim_id)
            return record
        except Exception as e:
            print(f"Error getting record by Airtable ID: {str(e)}")
        
        return None
    except Exception as e:
        print(f"Error getting claim record {claim_id}: {str(e)}")
        return None

# Test the function
result = get_patient_record("CIMR-0001")
print(result)