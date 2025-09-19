from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import os
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
print("Initializing CIMR-OS modules...")

# ACAPS Compliance Module
acaps_db = setup_acaps_db("tmp/acaps.db")
acaps_reporter = create_acaps_reporter(acaps_db)
compliance_monitor = create_compliance_monitor(acaps_db)
audit_tracker = create_audit_tracker(acaps_db)
regulation_watcher = create_regulation_watcher(acaps_db)

# Member Relations Module
member_db = setup_member_db("tmp/member.db")
cimr_chatbot = create_cimr_chatbot(member_db)
pension_simulator = create_pension_simulator(member_db)
fraud_detector = create_fraud_detector(member_db)
retirement_planner = create_retirement_planner(member_db)

# Financial Risk Management Module
financial_db = setup_financial_db("tmp/financial.db")
var_calculator = create_var_calculator(financial_db)
stress_tester = create_stress_tester(financial_db)
credit_monitor = create_credit_monitor(financial_db)
actuarial_risk_bot = create_actuarial_risk_bot(financial_db)

# Actuarial Projections Module
actuarial_db = setup_actuarial_db("tmp/actuarial.db")
demographic_ai = create_demographic_ai(actuarial_db)
pension_calculator = create_pension_calculator(actuarial_db)
reserve_optimizer = create_reserve_optimizer(actuarial_db)
scenario_planner = create_scenario_planner(actuarial_db)

# Allocation Optimization Module
allocation_db = setup_allocation_db("tmp/allocation.db")
actuarial_optimizer = create_actuarial_optimizer(allocation_db)
rebalancing_ai = create_rebalancing_ai(allocation_db)
opci_optimizer = create_opci_optimizer(allocation_db)
scenario_stress_tester = create_scenario_stress_tester(allocation_db)

print("All modules initialized successfully!")

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
    try:
        # Validate module and agent
        if request.module not in AGENTS:
            raise HTTPException(
                status_code=400, 
                detail=f"Module '{request.module}' not found. Available modules: {list(AGENTS.keys())}"
            )
        
        if request.agent not in AGENTS[request.module]:
            raise HTTPException(
                status_code=400, 
                detail=f"Agent '{request.agent}' not found in module '{request.module}'. Available agents: {list(AGENTS[request.module].keys())}"
            )
        
        # Get the agent
        agent = AGENTS[request.module][request.agent]
        
        # Execute the query
        response = agent.print_response(request.query, stream=False)
        
        return ResponseModel(
            success=True,
            response=response,
            module=request.module,
            agent=request.agent
        )
        
    except Exception as e:
        return ResponseModel(
            success=False,
            response="",
            module=request.module,
            agent=request.agent,
            error=str(e)
        )

# ACAPS Compliance endpoints
@app.post("/acaps/reporter")
async def acaps_reporter_query(request: QueryRequest):
    request.module = "acaps_compliance"
    request.agent = "acaps_reporter"
    return await query_agent(request)

@app.post("/acaps/compliance")
async def compliance_monitor_query(request: QueryRequest):
    request.module = "acaps_compliance"
    request.agent = "compliance_monitor"
    return await query_agent(request)

@app.post("/acaps/audit")
async def audit_tracker_query(request: QueryRequest):
    request.module = "acaps_compliance"
    request.agent = "audit_tracker"
    return await query_agent(request)

@app.post("/acaps/regulation")
async def regulation_watcher_query(request: QueryRequest):
    request.module = "acaps_compliance"
    request.agent = "regulation_watcher"
    return await query_agent(request)

# Member Relations endpoints
@app.post("/member/chatbot")
async def cimr_chatbot_query(request: QueryRequest):
    request.module = "member_relations"
    request.agent = "cimr_chatbot"
    return await query_agent(request)

@app.post("/member/pension-simulator")
async def pension_simulator_query(request: QueryRequest):
    request.module = "member_relations"
    request.agent = "pension_simulator"
    return await query_agent(request)

@app.post("/member/fraud-detector")
async def fraud_detector_query(request: QueryRequest):
    request.module = "member_relations"
    request.agent = "fraud_detector"
    return await query_agent(request)

@app.post("/member/retirement-planner")
async def retirement_planner_query(request: QueryRequest):
    request.module = "member_relations"
    request.agent = "retirement_planner"
    return await query_agent(request)

# Financial Risk Management endpoints
@app.post("/financial/var-calculator")
async def var_calculator_query(request: QueryRequest):
    request.module = "financial_risk"
    request.agent = "var_calculator"
    return await query_agent(request)

@app.post("/financial/stress-tester")
async def stress_tester_query(request: QueryRequest):
    request.module = "financial_risk"
    request.agent = "stress_tester"
    return await query_agent(request)

@app.post("/financial/credit-monitor")
async def credit_monitor_query(request: QueryRequest):
    request.module = "financial_risk"
    request.agent = "credit_monitor"
    return await query_agent(request)

@app.post("/financial/actuarial-risk")
async def actuarial_risk_bot_query(request: QueryRequest):
    request.module = "financial_risk"
    request.agent = "actuarial_risk_bot"
    return await query_agent(request)

# Actuarial Projections endpoints
@app.post("/actuarial/demographic")
async def demographic_ai_query(request: QueryRequest):
    request.module = "actuarial_projections"
    request.agent = "demographic_ai"
    return await query_agent(request)

@app.post("/actuarial/pension-calculator")
async def pension_calculator_query(request: QueryRequest):
    request.module = "actuarial_projections"
    request.agent = "pension_calculator"
    return await query_agent(request)

@app.post("/actuarial/reserve-optimizer")
async def reserve_optimizer_query(request: QueryRequest):
    request.module = "actuarial_projections"
    request.agent = "reserve_optimizer"
    return await query_agent(request)

@app.post("/actuarial/scenario-planner")
async def scenario_planner_query(request: QueryRequest):
    request.module = "actuarial_projections"
    request.agent = "scenario_planner"
    return await query_agent(request)

# Allocation Optimization endpoints
@app.post("/allocation/optimizer")
async def actuarial_optimizer_query(request: QueryRequest):
    request.module = "allocation_optimization"
    request.agent = "actuarial_optimizer"
    return await query_agent(request)

@app.post("/allocation/rebalancing")
async def rebalancing_ai_query(request: QueryRequest):
    request.module = "allocation_optimization"
    request.agent = "rebalancing_ai"
    return await query_agent(request)

@app.post("/allocation/opci")
async def opci_optimizer_query(request: QueryRequest):
    request.module = "allocation_optimization"
    request.agent = "opci_optimizer"
    return await query_agent(request)

@app.post("/allocation/scenario-stress")
async def scenario_stress_tester_query(request: QueryRequest):
    request.module = "allocation_optimization"
    request.agent = "scenario_stress_tester"
    return await query_agent(request)

# Run the server
if __name__ == "__main__":
    uvicorn.run(
        "Server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )