import os
from pyairtable import Api
from dotenv import load_dotenv
import json
import uuid
from datetime import datetime

load_dotenv()

AIRTABLE_TOKEN = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

# Initialize the Airtable API
api = Api(AIRTABLE_TOKEN)
claims_table = api.table(BASE_ID, "claims_data")
member_profiles_table = api.table(BASE_ID, "member_profiles")

def get_claim_record(claim_id: str):
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
# result = get_patient_record("CIMR-0001")
# print(result)
#here is the printed stuff:
# {'id': 'recA1Q2a7QL5joYUm', 'createdTime': '2025-09-24T16:43:14.000Z', 'fields': {'claim_id': 'CIMR-0001', 'member_id': 'M001', 'claim_type': 'pension_payment', 'entities': '{"month": "January 2025", "issue": "incorrect_amount"}', 'raw_text': "Je n'ai pas reçu ma pension de janvier 2025, le montant est 
# incorrect. Merci de corriger.", 'status': 'classified', 'confidence': 0.95, 
# 'next_action': 'eligibility_check'}}
def create_claim_record(claim_data: dict, raw_text: str = ""):
    """
    Creates a new claim record in Airtable.
    
    Args:
        claim_data (dict): Structured claim data with keys: claim_id, member_id, claim_type, confidence, entities, next_action
        raw_text (str): Original raw text of the claim
        
    Returns:
        dict: Created record data or None if failed
    """
    try:
        # Check if claim_data is a dictionary
        if not isinstance(claim_data, dict):
            print(f"ERROR: claim_data is not a dictionary, it's: {type(claim_data)}")
            return None
        
        # Generate unique claim ID if not provided
        if 'claim_id' not in claim_data or not claim_data['claim_id']:
            claim_data['claim_id'] = f"CIMR-{str(uuid.uuid4())[:8].upper()}"
        
        # Check for required fields
        required_fields = ['claim_type', 'confidence', 'next_action']
        missing_fields = [field for field in required_fields if field not in claim_data]
        if missing_fields:
            print(f"ERROR: Missing required fields: {missing_fields}")
            return None
        
        # Prepare record data for Airtable
        record_data = {
            'claim_id': claim_data['claim_id'],
            'member_id': claim_data.get('member_id', 'M000'),  # Default member ID if not provided
            'claim_type': claim_data['claim_type'],
            'entities': json.dumps(claim_data.get('entities', {})),
            'raw_text': raw_text,
            'status': 'classified',
            'confidence': claim_data['confidence'],
            'next_action': claim_data['next_action']
        }
        
        # Create record in Airtable
        created_record = claims_table.create(record_data)
        print(f"✅ Successfully created claim record: {claim_data['claim_id']}")
        return created_record
        
    except Exception as e:
        print(f"❌ Error creating claim record: {str(e)}")
        return None


def get_latest_claim():
    """Get the most recent claim from the database."""
    try:
        # Get all records sorted by created time (most recent first)
        records = claims_table.all(sort=["-createdTime"])
        if records:
            return records[0]
        return None
    except Exception as e:
        print(f"Error getting latest claim: {str(e)}")
        return None


def get_member_profile(member_id: str):
    """Get a member profile by member ID."""
    try:
        # Try to find by member_id field
        records = member_profiles_table.all(formula=f"{{member_id}}='{member_id}'")
        if records:
            return records[0]
        return None
    except Exception as e:
        print(f"Error getting member profile {member_id}: {str(e)}")
        return None


def update_claim_eligibility(claim_id: str, eligibility_status: str, explanation: str):
    """Update the eligibility status of a claim."""
    try:
        # First find the claim by claim_id
        records = claims_table.all(formula=f"{{claim_id}}='{claim_id}'")
        if not records:
            print(f"Claim {claim_id} not found")
            return None
        
        claim_record = records[0]
        record_id = claim_record['id']
        
        # Update the record
        updated_record = claims_table.update(record_id, {
            'eligibility_status': eligibility_status,
            'explanation': explanation,
            # 'processed_at': datetime.now().isoformat()
        })
        
        print(f"✅ Updated claim {claim_id} eligibility status to: {eligibility_status}")
        return updated_record
        
    except Exception as e:
        print(f"❌ Error updating claim eligibility: {str(e)}")
        return None


def load_cimr_rules(file_path: str = "Backend/Inputs/CIMR_Rules.md"):
    """Load CIMR rules and regulations from markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"❌ CIMR rules file not found at {file_path}")
        return None
    except Exception as e:
        print(f"❌ Error loading CIMR rules: {str(e)}")
        return None

