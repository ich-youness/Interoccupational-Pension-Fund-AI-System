from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Import all module functions
from Modules.ACAPS_Compliance import (
    create_acaps_reporter, 
    create_compliance_monitor, 
    create_audit_tracker, 
    create_regulation_watcher,
    setup_database as setup_acaps_db
)

from Modules.Member_Relations import (
    create_cimr_chatbot,
    create_pension_simulator,
    create_fraud_detector,
    create_retirement_planner,
    setup_database as setup_member_db
)

from Modules.Financial_Risk_Management import (
    create_var_calculator,
    create_stress_tester,
    create_credit_monitor,
    create_actuarial_risk_bot,
    setup_database as setup_financial_db
)

from Modules.Actuarial_Projections import (
    create_demographic_ai,
    create_pension_calculator,
    create_reserve_optimizer,
    create_scenario_planner,
    setup_database as setup_actuarial_db
)

from Modules.Allocation_Optimization_Portfolio import (
    create_actuarial_optimizer,
    create_rebalancing_ai,
    create_opci_optimizer,
    create_scenario_stress_tester,
    setup_database as setup_allocation_db
)

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cimr_os.log'),
        logging.StreamHandler()
    ]
)

# Create logger for agent calls
agent_logger = logging.getLogger('cimr_os.agents')
api_logger = logging.getLogger('cimr_os.api')

# Initialize FastAPI app
app = FastAPI(
    title="CIMR-OS API",
    description="AI-powered pension fund management system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str
    module: str
    agent: str
    custom_data: Optional[Dict[str, Any]] = None

class ResponseModel(BaseModel):
    success: bool
    response: str
    module: str
    agent: str
    error: Optional[str] = None

# Initialize databases and agents
api_logger.info("Initializing CIMR-OS modules...")

# ACAPS Compliance Module
api_logger.info("Setting up ACAPS Compliance Module...")
acaps_db = setup_acaps_db("tmp/acaps.db")
agent_logger.info("Creating ACAPS Reporter agent...")
acaps_reporter = create_acaps_reporter(acaps_db)
agent_logger.info("Creating Compliance Monitor agent...")
compliance_monitor = create_compliance_monitor(acaps_db)
agent_logger.info("Creating Audit Tracker agent...")
audit_tracker = create_audit_tracker(acaps_db)
agent_logger.info("Creating Regulation Watcher agent...")
regulation_watcher = create_regulation_watcher(acaps_db)

# Member Relations Module
api_logger.info("Setting up Member Relations Module...")
member_db = setup_member_db("tmp/member.db")
agent_logger.info("Creating CIMR Chatbot agent...")
cimr_chatbot = create_cimr_chatbot(member_db)
agent_logger.info("Creating Pension Simulator agent...")
pension_simulator = create_pension_simulator(member_db)
agent_logger.info("Creating Fraud Detector agent...")
fraud_detector = create_fraud_detector(member_db)
agent_logger.info("Creating Retirement Planner agent...")
retirement_planner = create_retirement_planner(member_db)

# Financial Risk Management Module
api_logger.info("Setting up Financial Risk Management Module...")
financial_db = setup_financial_db("tmp/financial.db")
agent_logger.info("Creating VaR Calculator agent...")
var_calculator = create_var_calculator(financial_db)
agent_logger.info("Creating Stress Tester agent...")
stress_tester = create_stress_tester(financial_db)
agent_logger.info("Creating Credit Monitor agent...")
credit_monitor = create_credit_monitor(financial_db)
agent_logger.info("Creating Actuarial Risk Bot agent...")
actuarial_risk_bot = create_actuarial_risk_bot(financial_db)

# Actuarial Projections Module
api_logger.info("Setting up Actuarial Projections Module...")
actuarial_db = setup_actuarial_db("tmp/actuarial.db")
agent_logger.info("Creating Demographic AI agent...")
demographic_ai = create_demographic_ai(actuarial_db)
agent_logger.info("Creating Pension Calculator agent...")
pension_calculator = create_pension_calculator(actuarial_db)
agent_logger.info("Creating Reserve Optimizer agent...")
reserve_optimizer = create_reserve_optimizer(actuarial_db)
agent_logger.info("Creating Scenario Planner agent...")
scenario_planner = create_scenario_planner(actuarial_db)

# Allocation Optimization Module
api_logger.info("Setting up Allocation Optimization Module...")
allocation_db = setup_allocation_db("tmp/allocation.db")
agent_logger.info("Creating Actuarial Optimizer agent...")
actuarial_optimizer = create_actuarial_optimizer(allocation_db)
agent_logger.info("Creating Rebalancing AI agent...")
rebalancing_ai = create_rebalancing_ai(allocation_db)
agent_logger.info("Creating OPCI Optimizer agent...")
opci_optimizer = create_opci_optimizer(allocation_db)
agent_logger.info("Creating Scenario Stress Tester agent...")
scenario_stress_tester = create_scenario_stress_tester(allocation_db)

api_logger.info("All modules initialized successfully!")

# Agent mapping for easy access
AGENTS = {
    "acaps_compliance": {
        "acaps_reporter": acaps_reporter,
        "compliance_monitor": compliance_monitor,
        "audit_tracker": audit_tracker,
        "regulation_watcher": regulation_watcher
    },
    "member_relations": {
        "cimr_chatbot": cimr_chatbot,
        "pension_simulator": pension_simulator,
        "fraud_detector": fraud_detector,
        "retirement_planner": retirement_planner
    },
    "financial_risk": {
        "var_calculator": var_calculator,
        "stress_tester": stress_tester,
        "credit_monitor": credit_monitor,
        "actuarial_risk_bot": actuarial_risk_bot
    },
    "actuarial_projections": {
        "demographic_ai": demographic_ai,
        "pension_calculator": pension_calculator,
        "reserve_optimizer": reserve_optimizer,
        "scenario_planner": scenario_planner
    },
    "allocation_optimization": {
        "actuarial_optimizer": actuarial_optimizer,
        "rebalancing_ai": rebalancing_ai,
        "opci_optimizer": opci_optimizer,
        "scenario_stress_tester": scenario_stress_tester
    }
}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "CIMR-OS API is running",
        "version": "1.0.0",
        "available_modules": list(AGENTS.keys())
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "All systems operational"}

# Get available modules and agents
@app.get("/modules")
async def get_modules():
    return {
        "modules": {
            module_name: list(agents.keys()) 
            for module_name, agents in AGENTS.items()
        }
    }

# Main query endpoint
@app.post("/query", response_model=ResponseModel)
async def query_agent(request: QueryRequest):
    start_time = datetime.now()
    request_id = f"{request.module}_{request.agent}_{start_time.strftime('%Y%m%d_%H%M%S')}"
    
    api_logger.info(f"[{request_id}] Received query request - Module: {request.module}, Agent: {request.agent}")
    agent_logger.info(f"[{request_id}] Query: {request.query[:100]}{'...' if len(request.query) > 100 else ''}")
    
    try:
        # Validate module and agent
        if request.module not in AGENTS:
            error_msg = f"Module '{request.module}' not found. Available modules: {list(AGENTS.keys())}"
            api_logger.error(f"[{request_id}] {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        if request.agent not in AGENTS[request.module]:
            error_msg = f"Agent '{request.agent}' not found in module '{request.module}'. Available agents: {list(AGENTS[request.module].keys())}"
            api_logger.error(f"[{request_id}] {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Get the agent
        agent = AGENTS[request.module][request.agent]
        agent_logger.info(f"[{request_id}] Agent retrieved successfully: {agent.name}")
        
        # Execute the query
        agent_logger.info(f"[{request_id}] Executing agent query...")
        execution_start = datetime.now()
        
        response = agent.run(request.query, stream=False)
        response_content = response.content
        
        execution_time = (datetime.now() - execution_start).total_seconds()
        agent_logger.info(f"[{request_id}] Agent execution completed in {execution_time:.2f} seconds")
        agent_logger.info(f"[{request_id}] Response length: {len(response_content)} characters")
        
        total_time = (datetime.now() - start_time).total_seconds()
        api_logger.info(f"[{request_id}] Query completed successfully in {total_time:.2f} seconds")
        
        return ResponseModel(
            success=True,
            response=response_content,
            module=request.module,
            agent=request.agent
        )
        
    except HTTPException as e:
        total_time = (datetime.now() - start_time).total_seconds()
        api_logger.error(f"[{request_id}] HTTP error after {total_time:.2f} seconds: {e.detail}")
        return ResponseModel(
            success=False,
            response="",
            module=request.module,
            agent=request.agent,
            error=e.detail
        )
        
    except Exception as e:
        total_time = (datetime.now() - start_time).total_seconds()
        error_msg = str(e)
        api_logger.error(f"[{request_id}] Unexpected error after {total_time:.2f} seconds: {error_msg}")
        agent_logger.error(f"[{request_id}] Error details: {type(e).__name__}: {error_msg}")
        
        return ResponseModel(
            success=False,
            response="",
            module=request.module,
            agent=request.agent,
            error=error_msg
        )

# ACAPS Compliance endpoints
@app.post("/acaps/reporter")
async def acaps_reporter_query(request: QueryRequest):
    api_logger.info(f"ACAPS Reporter endpoint called - Query: {request.query[:50]}...")
    request.module = "acaps_compliance"
    request.agent = "acaps_reporter"
    return await query_agent(request)

@app.post("/acaps/compliance")
async def compliance_monitor_query(request: QueryRequest):
    api_logger.info(f"Compliance Monitor endpoint called - Query: {request.query[:50]}...")
    request.module = "acaps_compliance"
    request.agent = "compliance_monitor"
    return await query_agent(request)

@app.post("/acaps/audit")
async def audit_tracker_query(request: QueryRequest):
    api_logger.info(f"Audit Tracker endpoint called - Query: {request.query[:50]}...")
    request.module = "acaps_compliance"
    request.agent = "audit_tracker"
    return await query_agent(request)

@app.post("/acaps/regulation")
async def regulation_watcher_query(request: QueryRequest):
    api_logger.info(f"Regulation Watcher endpoint called - Query: {request.query[:50]}...")
    request.module = "acaps_compliance"
    request.agent = "regulation_watcher"
    return await query_agent(request)

# Member Relations endpoints
@app.post("/member/chatbot")
async def cimr_chatbot_query(request: QueryRequest):
    api_logger.info(f"CIMR Chatbot endpoint called - Query: {request.query[:50]}...")
    request.module = "member_relations"
    request.agent = "cimr_chatbot"
    return await query_agent(request)

@app.post("/member/pension-simulator")
async def pension_simulator_query(request: QueryRequest):
    api_logger.info(f"Pension Simulator endpoint called - Query: {request.query[:50]}...")
    request.module = "member_relations"
    request.agent = "pension_simulator"
    return await query_agent(request)

@app.post("/member/fraud-detector")
async def fraud_detector_query(request: QueryRequest):
    api_logger.info(f"Fraud Detector endpoint called - Query: {request.query[:50]}...")
    request.module = "member_relations"
    request.agent = "fraud_detector"
    return await query_agent(request)

@app.post("/member/retirement-planner")
async def retirement_planner_query(request: QueryRequest):
    api_logger.info(f"Retirement Planner endpoint called - Query: {request.query[:50]}...")
    request.module = "member_relations"
    request.agent = "retirement_planner"
    return await query_agent(request)

# Financial Risk Management endpoints
@app.post("/financial/var-calculator")
async def var_calculator_query(request: QueryRequest):
    api_logger.info(f"VaR Calculator endpoint called - Query: {request.query[:50]}...")
    request.module = "financial_risk"
    request.agent = "var_calculator"
    return await query_agent(request)

@app.post("/financial/stress-tester")
async def stress_tester_query(request: QueryRequest):
    api_logger.info(f"Stress Tester endpoint called - Query: {request.query[:50]}...")
    request.module = "financial_risk"
    request.agent = "stress_tester"
    return await query_agent(request)

@app.post("/financial/credit-monitor")
async def credit_monitor_query(request: QueryRequest):
    api_logger.info(f"Credit Monitor endpoint called - Query: {request.query[:50]}...")
    request.module = "financial_risk"
    request.agent = "credit_monitor"
    return await query_agent(request)

@app.post("/financial/actuarial-risk")
async def actuarial_risk_bot_query(request: QueryRequest):
    api_logger.info(f"Actuarial Risk Bot endpoint called - Query: {request.query[:50]}...")
    request.module = "financial_risk"
    request.agent = "actuarial_risk_bot"
    return await query_agent(request)

# Actuarial Projections endpoints
@app.post("/actuarial/demographic")
async def demographic_ai_query(request: QueryRequest):
    api_logger.info(f"Demographic AI endpoint called - Query: {request.query[:50]}...")
    request.module = "actuarial_projections"
    request.agent = "demographic_ai"
    return await query_agent(request)

@app.post("/actuarial/pension-calculator")
async def pension_calculator_query(request: QueryRequest):
    api_logger.info(f"Pension Calculator endpoint called - Query: {request.query[:50]}...")
    request.module = "actuarial_projections"
    request.agent = "pension_calculator"
    return await query_agent(request)

@app.post("/actuarial/reserve-optimizer")
async def reserve_optimizer_query(request: QueryRequest):
    api_logger.info(f"Reserve Optimizer endpoint called - Query: {request.query[:50]}...")
    request.module = "actuarial_projections"
    request.agent = "reserve_optimizer"
    return await query_agent(request)

@app.post("/actuarial/scenario-planner")
async def scenario_planner_query(request: QueryRequest):
    api_logger.info(f"Scenario Planner endpoint called - Query: {request.query[:50]}...")
    request.module = "actuarial_projections"
    request.agent = "scenario_planner"
    return await query_agent(request)

# Allocation Optimization endpoints
@app.post("/allocation/optimizer")
async def actuarial_optimizer_query(request: QueryRequest):
    api_logger.info(f"Actuarial Optimizer endpoint called - Query: {request.query[:50]}...")
    request.module = "allocation_optimization"
    request.agent = "actuarial_optimizer"
    return await query_agent(request)

@app.post("/allocation/rebalancing")
async def rebalancing_ai_query(request: QueryRequest):
    api_logger.info(f"Rebalancing AI endpoint called - Query: {request.query[:50]}...")
    request.module = "allocation_optimization"
    request.agent = "rebalancing_ai"
    return await query_agent(request)

@app.post("/allocation/opci")
async def opci_optimizer_query(request: QueryRequest):
    api_logger.info(f"OPCI Optimizer endpoint called - Query: {request.query[:50]}...")
    request.module = "allocation_optimization"
    request.agent = "opci_optimizer"
    return await query_agent(request)

@app.post("/allocation/scenario-stress")
async def scenario_stress_tester_query(request: QueryRequest):
    api_logger.info(f"Scenario Stress Tester endpoint called - Query: {request.query[:50]}...")
    request.module = "allocation_optimization"
    request.agent = "scenario_stress_tester"
    return await query_agent(request)

# Run the server
if __name__ == "__main__":
    api_logger.info("Starting CIMR-OS FastAPI Server...")
    api_logger.info("Server will be available at: http://localhost:8000")
    api_logger.info("API Documentation: http://localhost:8000/docs")
    api_logger.info("Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "Server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )