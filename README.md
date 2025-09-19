# CIMR-OS: AI-Powered Pension Fund Management System

![CIMR-OS Logo](https://img.shields.io/badge/CIMR--OS-AI%20Pension%20Management-blue?style=for-the-badge&logo=shield)

A comprehensive AI-powered pension fund management system designed for the Caisse Interprofessionnelle Marocaine de Retraite (CIMR). This system provides intelligent automation, compliance monitoring, risk management, and member services through specialized AI agents.

## 🎯 Overview

CIMR-OS is a full-stack application that combines modern web technologies with AI-powered agents to streamline pension fund operations. The system is built with a modular architecture, featuring specialized AI agents for different aspects of pension fund management.

### Key Features

- **🤖 AI-Powered Agents**: 20 specialized AI agents across 5 modules
- **📊 Real-time Analytics**: Comprehensive dashboards and reporting
- **🛡️ Compliance Monitoring**: Automated ACAPS regulatory compliance
- **💰 Risk Management**: Advanced financial risk assessment tools
- **👥 Member Services**: Interactive chatbot and pension planning tools
- **📈 Portfolio Optimization**: AI-driven allocation and rebalancing
- **🔍 Fraud Detection**: Automated suspicious activity monitoring

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **FastAPI Server**: High-performance API with automatic documentation
- **Modular Design**: 5 specialized modules with independent databases
- **AI Integration**: XAI API integration for intelligent responses
- **Database**: SQLite databases for each module (ACAPS, Member Relations, etc.)

### Frontend (React/TypeScript)
- **React 18**: Modern React with TypeScript
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **Shadcn/ui**: Beautiful, accessible UI components
- **React Router**: Client-side routing

## 📁 Project Structure

```
CIMR-OS/
├── Backend/                    # Python FastAPI Backend
│   ├── Modules/               # AI Agent Modules
│   │   ├── ACAPS_Compliance.py
│   │   ├── Member_Relations.py
│   │   ├── Financial_Risk_Management.py
│   │   ├── Actuarial_Projections.py
│   │   └── Allocation_Optimization_Portfolio.py
│   ├── Inputs/               # JSON Input Templates
│   ├── Tools/                # Utility Tools
│   ├── Server.py             # Main FastAPI Application
│   ├── run_server.py         # Server Startup Script
│   └── API_README.md         # Backend Documentation
├── Frontend/                  # React TypeScript Frontend
│   ├── src/
│   │   ├── components/       # Reusable UI Components
│   │   ├── pages/           # Application Pages
│   │   ├── data/            # Data Models and Types
│   │   └── lib/             # Utility Functions
│   ├── public/              # Static Assets
│   └── package.json         # Frontend Dependencies
└── README.md                # This File
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **XAI API Key** (for AI functionality)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd CIMR-OS
```

### 2. Backend Setup

```bash
cd Backend

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
echo "XAI_API_KEY=your_xai_api_key_here" > .env

# Start the server
python run_server.py
```

The backend will be available at:
- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 3. Frontend Setup

```bash
cd Frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at http://localhost:5173

## 🤖 AI Modules & Agents

### 1. ACAPS Compliance Module
**Purpose**: Regulatory compliance and reporting for ACAPS standards

| Agent | Function | Description |
|-------|----------|-------------|
| ACAPS Reporter | Report Generation | Generates regulatory reports and documentation |
| Compliance Monitor | Violation Detection | Monitors portfolio for compliance violations |
| Audit Tracker | Audit Management | Tracks and manages audit trails |
| Regulation Watcher | Regulatory Updates | Monitors regulatory changes and updates |

### 2. Member Relations Module
**Purpose**: Member services and pension planning

| Agent | Function | Description |
|-------|----------|-------------|
| CIMR Chatbot | Member Support | Interactive chatbot for member queries |
| Pension Simulator | Pension Modeling | Simulates pension scenarios and projections |
| Fraud Detector | Security | Detects suspicious member account activity |
| Retirement Planner | Planning | Creates personalized retirement plans |

### 3. Financial Risk Management Module
**Purpose**: Risk assessment and financial analysis

| Agent | Function | Description |
|-------|----------|-------------|
| VaR Calculator | Risk Metrics | Calculates Value at Risk metrics |
| Stress Tester | Scenario Analysis | Tests portfolio under stress scenarios |
| Credit Monitor | Credit Risk | Monitors credit risk for bond issuers |
| Actuarial Risk Bot | Longevity Risk | Assesses mortality and longevity risks |

### 4. Actuarial Projections Module
**Purpose**: Demographic analysis and actuarial calculations

| Agent | Function | Description |
|-------|----------|-------------|
| Demographic AI | Population Analysis | Projects demographic trends and structure |
| Pension Calculator | Benefit Calculation | Calculates pension entitlements |
| Reserve Optimizer | Reserve Management | Optimizes provident reserve levels |
| Scenario Planner | Strategic Planning | Creates strategic adaptation plans |

### 5. Allocation Optimization Module
**Purpose**: Portfolio optimization and asset allocation

| Agent | Function | Description |
|-------|----------|-------------|
| Actuarial Optimizer | Portfolio Optimization | Optimizes allocation using actuarial data |
| Rebalancing AI | Portfolio Rebalancing | Manages portfolio drift and rebalancing |
| OPCI Optimizer | Real Estate Allocation | Optimizes real estate through OPCI vehicles |
| Scenario Stress Tester | Comprehensive Testing | Runs comprehensive stress tests |

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the Backend directory:

```env
XAI_API_KEY=your_xai_api_key_here
```

### CORS Configuration

The backend is configured to accept requests from `http://localhost:5173` (Vite default). To modify this, update the CORS settings in `Backend/Server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 API Usage

### Generic Query Endpoint

All agents can be accessed through the generic `/query` endpoint:

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Your question here",
    "module": "acaps_compliance",
    "agent": "acaps_reporter",
    "custom_data": {}
  }'
```

### Module-Specific Endpoints

Each module has dedicated endpoints:

```bash
# ACAPS Compliance
curl -X POST "http://localhost:8000/acaps/reporter" \
  -H "Content-Type: application/json" \
  -d '{"query": "Generate ACAPS report", "custom_data": {}}'

# Member Relations
curl -X POST "http://localhost:8000/member/chatbot" \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I check my pension?", "custom_data": {}}'

# Financial Risk
curl -X POST "http://localhost:8000/financial/var-calculator" \
  -H "Content-Type: application/json" \
  -d '{"query": "Calculate 1-day 95% VaR", "custom_data": {}}'
```

## 🎨 Frontend Features

### Modern UI Components
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Dark/Light Mode**: Theme switching capability
- **Accessible Components**: Built with accessibility in mind
- **Interactive Charts**: Real-time data visualization with Recharts

### Key Pages
- **Landing Page**: Module overview and navigation
- **Agent Chat**: Interactive chat interface with AI agents
- **SubTeam Pages**: Detailed module and agent information
- **Dashboard**: Real-time analytics and monitoring

## 🧪 Testing

### Backend Testing
```bash
cd Backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd Frontend
npm run test
```

### API Testing
Use the interactive documentation at http://localhost:8000/docs or test with curl commands.

## 📈 Performance

- **Backend**: FastAPI with async support for high performance
- **Frontend**: Vite for fast development and optimized builds
- **Database**: SQLite with module-specific databases for data isolation
- **Caching**: Built-in response caching for improved performance

## 🔒 Security

- **CORS Protection**: Configured for specific origins
- **Input Validation**: Pydantic models for request validation
- **Error Handling**: Comprehensive error handling and logging
- **Database Isolation**: Separate databases for each module

## 🚀 Deployment

### Development
```bash
# Backend
cd Backend && python run_server.py

# Frontend
cd Frontend && npm run dev
```

### Production
```bash
# Build frontend
cd Frontend && npm run build

# Serve with production server
cd Backend && uvicorn Server:app --host 0.0.0.0 --port 8000
```

## 📝 Documentation

- **Backend API**: [Backend/API_README.md](Backend/API_README.md)
- **Module Architecture**: [Backend/Modules/README.md](Backend/Modules/README.md)
- **Frontend Updates**: [Frontend/FRONTEND_UPDATE_SUMMARY.md](Frontend/FRONTEND_UPDATE_SUMMARY.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at http://localhost:8000/docs
- Review the module-specific documentation

## 🔮 Roadmap

- [ ] Advanced analytics dashboard
- [ ] Mobile application
- [ ] Integration with external pension systems
- [ ] Machine learning model improvements
- [ ] Multi-language support
- [ ] Advanced reporting features

---

**CIMR-OS** - Empowering pension fund management with AI technology 🚀
