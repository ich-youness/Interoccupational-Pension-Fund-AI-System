# CIMR-OS FastAPI Server

A comprehensive FastAPI server that provides AI-powered pension fund management capabilities through modular agents.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd Backend
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python run_server.py
```

Or directly:
```bash
python Server.py
```

### 3. Access the API
- **Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📋 API Endpoints

### General Endpoints

#### `GET /`
Root endpoint with basic information
```json
{
  "message": "CIMR-OS API is running",
  "version": "1.0.0",
  "available_modules": ["acaps_compliance", "member_relations", "financial_risk", "actuarial_projections", "allocation_optimization"]
}
```

#### `GET /health`
Health check endpoint
```json
{
  "status": "healthy",
  "message": "All systems operational"
}
```

#### `GET /modules`
Get all available modules and agents
```json
{
  "modules": {
    "acaps_compliance": ["acaps_reporter", "compliance_monitor", "audit_tracker", "regulation_watcher"],
    "member_relations": ["cimr_chatbot", "pension_simulator", "fraud_detector", "retirement_planner"],
    "financial_risk": ["var_calculator", "stress_tester", "credit_monitor", "actuarial_risk_bot"],
    "actuarial_projections": ["demographic_ai", "pension_calculator", "reserve_optimizer", "scenario_planner"],
    "allocation_optimization": ["actuarial_optimizer", "rebalancing_ai", "opci_optimizer", "scenario_stress_tester"]
  }
}
```

### ACAPS Compliance Module

#### `POST /acaps/reporter`
Generate ACAPS regulatory reports
```json
{
  "query": "Generate the ACAPS regulatory report for the current portfolio",
  "custom_data": {}
}
```

#### `POST /acaps/compliance`
Monitor compliance violations
```json
{
  "query": "Check the current portfolio for compliance violations",
  "custom_data": {}
}
```

#### `POST /acaps/audit`
Generate audit trails
```json
{
  "query": "Generate a complete audit trail for all operations",
  "custom_data": {}
}
```

#### `POST /acaps/regulation`
Monitor regulatory changes
```json
{
  "query": "Check for new regulatory changes affecting pension funds",
  "custom_data": {}
}
```

### Member Relations Module

#### `POST /member/chatbot`
CIMR member chatbot
```json
{
  "query": "How do I check my pension projection?",
  "custom_data": {}
}
```

#### `POST /member/pension-simulator`
Pension simulation
```json
{
  "query": "Simulate my pension at different retirement ages",
  "custom_data": {
    "member_id": "CIMR123456",
    "current_age": 45,
    "retirement_ages": [60, 62, 65]
  }
}
```

#### `POST /member/fraud-detector`
Fraud detection
```json
{
  "query": "Check for suspicious activity in member accounts",
  "custom_data": {}
}
```

#### `POST /member/retirement-planner`
Retirement planning
```json
{
  "query": "Create a personalized retirement plan",
  "custom_data": {}
}
```

### Financial Risk Management Module

#### `POST /financial/var-calculator`
Value at Risk calculation
```json
{
  "query": "Calculate 1-day 95% VaR for the current portfolio",
  "custom_data": {}
}
```

#### `POST /financial/stress-tester`
Stress testing
```json
{
  "query": "Run stress tests on the portfolio under market crash scenarios",
  "custom_data": {}
}
```

#### `POST /financial/credit-monitor`
Credit monitoring
```json
{
  "query": "Monitor credit risk for bond issuers in the portfolio",
  "custom_data": {}
}
```

#### `POST /financial/actuarial-risk`
Actuarial risk assessment
```json
{
  "query": "Assess longevity and mortality risks",
  "custom_data": {}
}
```

### Actuarial Projections Module

#### `POST /actuarial/demographic`
Demographic projections
```json
{
  "query": "Project Moroccan population structure up to 2100",
  "custom_data": {}
}
```

#### `POST /actuarial/pension-calculator`
Pension calculations
```json
{
  "query": "Calculate pension entitlements for a member",
  "custom_data": {}
}
```

#### `POST /actuarial/reserve-optimizer`
Reserve optimization
```json
{
  "query": "Optimize the provident reserve to maintain 40+ billion DH",
  "custom_data": {}
}
```

#### `POST /actuarial/scenario-planner`
Scenario planning
```json
{
  "query": "Create strategic adaptation plans for different scenarios",
  "custom_data": {}
}
```

### Allocation Optimization Module

#### `POST /allocation/optimizer`
Portfolio optimization
```json
{
  "query": "Optimize portfolio allocation using actuarial projections",
  "custom_data": {}
}
```

#### `POST /allocation/rebalancing`
Portfolio rebalancing
```json
{
  "query": "Check portfolio drift and suggest rebalancing trades",
  "custom_data": {}
}
```

#### `POST /allocation/opci`
OPCI optimization
```json
{
  "query": "Optimize real estate allocation through OPCI vehicles",
  "custom_data": {}
}
```

#### `POST /allocation/scenario-stress`
Scenario stress testing
```json
{
  "query": "Run comprehensive stress tests on the portfolio",
  "custom_data": {}
}
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the Backend directory:
```env
XAI_API_KEY=your_xai_api_key_here
```

### CORS Configuration
The server is configured to accept requests from `http://localhost:8080`. To modify this, update the `allow_origins` list in `Server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000"],  # Add more origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 Response Format

All endpoints return responses in the following format:

```json
{
  "success": true,
  "response": "Agent response text here",
  "module": "module_name",
  "agent": "agent_name",
  "error": null
}
```

## 🚨 Error Handling

The API includes comprehensive error handling:
- **400 Bad Request**: Invalid module or agent names
- **500 Internal Server Error**: Agent execution errors
- **422 Unprocessable Entity**: Invalid request format

## 🔍 Testing the API

### Using curl
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test ACAPS reporter
curl -X POST "http://localhost:8000/acaps/reporter" \
  -H "Content-Type: application/json" \
  -d '{"query": "Generate ACAPS report", "custom_data": {}}'

# Test member chatbot
curl -X POST "http://localhost:8000/member/chatbot" \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I check my pension?", "custom_data": {}}'
```

### Using the Interactive Documentation
Visit http://localhost:8000/docs to use the built-in Swagger UI for testing all endpoints.

## 🏗️ Architecture

The server follows a modular architecture:
- **FastAPI**: Web framework
- **Pydantic**: Data validation
- **CORS Middleware**: Cross-origin requests
- **Modular Agents**: Each module contains specialized AI agents
- **Database Separation**: Each module uses its own SQLite database

## 📝 Notes

- All agents are initialized at startup for optimal performance
- Each module uses a separate database file for data isolation
- The server supports both specific endpoints and a generic `/query` endpoint
- All responses are JSON-formatted for easy frontend integration
