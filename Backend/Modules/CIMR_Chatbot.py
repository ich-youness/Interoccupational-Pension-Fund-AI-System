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
from agno.vectordb.lancedb import LanceDb
from agno.tools.exa import ExaTools




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


def setup_database(db_file: str = "tmp/agno.db"):
    """Setup database connection.
    Args:
        db_file (str): Path to database file.
    Returns:
        SqliteDb: Database connection object.
    """
    return SqliteDb(db_file=db_file)




vector_db = LanceDb(
    table_name="my_markdown_knowledge",  # Name for your knowledge base table
    uri="tmp/agno_lancedb",  # Path where the database will be stored locally
    embedder=GeminiEmbedder(),

)
# 2. Configure the Knowledge Base with your Markdown file
knowledge_base = Knowledge(
    vector_db=vector_db,

)
knowledge_base.add_content(
    path="D:/CIMR-OS/Backend/Inputs/CIMR_Rules.md",   
)

# Add all markdown files from the markdown_output directory
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/Brochure_Questions-reponses_AGO_2018_-.md")
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/Brochure_réponses_aux_questions_des_adérents_AGO__2016.md")
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/Brochure_réponses_aux_questions_des_adhérents_AGO_2021.md")
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/Brochure_réponses_aux_questions_des_adhérents_AGM_2024.md")
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/Brochure_réponses_aux_questions_des_adhérents_2010.md")
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/Brochure_réponses_aux_questions_des_adhérents_2012.md")
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/Brochure_réponses_aux_questions_des_adhérents_2013.md")
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/Brochure_réponses_aux_questions_des_adhérents_2014.md")
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/Brochure_réponses_aux_questions_des_adhérents__AGO_2023.md")
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/Brochure_réponses_questions_adhérents_AGO.md")
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/Brochure_réponses_questions_adhérents_AGO_1.md")
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/Charte_de_Communication_Responsable.md")
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/Charte_des_Engagements_Client_CIMR_2024.md")
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/Offre_Al_Mounassib.md")
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/Questions-reponses_AGO_2017.md")
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/questions_aux_reponses.md")
knowledge_base.add_content(path="D:/CIMR-OS/Backend/Knowledge/markdown_output/Réponses_aux_questions_des_adhérents_AGM2022.md")



test_agent = Agent(
    name="test_agent",
    model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
    description="A test agent to test the knowledge base",
    instructions="""
    You are a chatbot that can answer questions based on the knowledge base and only the knowledge base, you cannot use any other tools.
    except when the user is asking about some things about CIMR that don't exist in the Knowledge base, then you can check the official documentation of CIMR on this link using the tool ExaTools https://www.cimr.ma/a-propos-cimr/espace-documentation/

    Important: Always provide in the end of the response give me the source of the information, either a link or the article number or name of the file in the knowledge base.
    """,
    knowledge=knowledge_base,
    search_knowledge=True,
    tools=[ExaTools("cimr.ma")],
    stream=True,
    markdown=True,
)

# test_agent.print_response("je veux savoir les les dates limites pour le règlement des contributions à la CIMR ", stream=True)
test_agent.print_response("c'est quoi La Formule de calcul des intérêts de retard", stream=True)