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

# agent 1
CIMRChatbot = Agent(
    name="DemographicAI",
    db=db,
    model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
    description=""" """,
    instructions="""""",
    add_history_to_context=True,


)