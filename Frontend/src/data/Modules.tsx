import { 
  BarChart3, 
  Shield, 
  TrendingUp, 
  Users, 
  Calculator, 
  FileText, 
  Target,
  Database,
  AlertTriangle,
  CheckCircle,
  Settings,
  PieChart,
  Brain,
  Zap,
  Eye,
  Building2,
  Activity,
  Layers,
  Workflow,
  Scale,
  Heart,
  DollarSign,
  ChartBar,
  UserCheck,
  AlertCircle,
  TrendingDown,
  PieChart as PieChartIcon,
  Target as TargetIcon
} from "lucide-react";

export interface Agent {
  id: string;
  name: string;
  description: string;
  icon: any;
  outputs: string[];
}

export interface SubTeam {
  id: string;
  name: string;
  description: string;
  mode: string;
  icon: any;
  agents: Agent[];
}

export interface Team {
  id: string;
  name: string;
  description: string;
  icon: any;
  subTeams: SubTeam[];
}

// ACAPS Compliance Module
export const acapsComplianceTeam: Team = {
  id: "acaps_compliance",
  name: "ACAPS Compliance Module",
  description: "AI-powered regulatory compliance and reporting for pension fund management",
  icon: Shield,
  subTeams: [
    {
      id: "regulatory-reporting",
      name: "Regulatory Reporting",
      description: "Automated ACAPS regulatory reporting and compliance monitoring",
      mode: "Coordinate",
      icon: FileText,
      agents: [
        {
          id: "acaps_reporter",
          name: "ACAPS Reporter",
          description: "AI agent that automates ACAPS regulatory reporting for CIMR. Generates reports accurately, validates compliance with mandatory fields, and reduces reporting time from 15 days to 1 day.",
          icon: FileText,
          outputs: [
            "ACAPS Regulatory Reports",
            "Compliance Validation Results",
            "Mandatory Field Verification",
            "Report Quality Assessment",
            "Automated Documentation"
          ]
        },
        {
          id: "compliance_monitor",
          name: "Compliance Monitor",
          description: "Real-time compliance monitoring agent that tracks regulatory adherence and identifies potential violations before they occur.",
          icon: AlertCircle,
          outputs: [
            "Compliance Status Reports",
            "Violation Alerts",
            "Risk Assessment",
            "Regulatory Updates",
            "Compliance Recommendations"
          ]
        }
      ]
    },
    {
      id: "audit-tracking",
      name: "Audit & Tracking",
      description: "Audit trail management and regulatory change monitoring",
      mode: "Coordinate",
      icon: Eye,
      agents: [
        {
          id: "audit_tracker",
          name: "Audit Tracker",
          description: "Comprehensive audit trail management agent that tracks all regulatory activities and maintains detailed records for compliance purposes.",
          icon: Eye,
          outputs: [
            "Audit Trail Reports",
            "Activity Logs",
            "Compliance Records",
            "Documentation Trails",
            "Audit Evidence"
          ]
        },
        {
          id: "regulation_watcher",
          name: "Regulation Watcher",
          description: "AI agent that monitors regulatory changes and updates, ensuring CIMR stays current with evolving compliance requirements.",
          icon: AlertTriangle,
          outputs: [
            "Regulatory Updates",
            "Change Notifications",
            "Impact Analysis",
            "Compliance Recommendations",
            "Update Summaries"
          ]
        }
      ]
    }
  ]
};

// Member Relations Module
export const memberRelationsTeam: Team = {
  id: "member_relations",
  name: "Member Relations Module",
  description: "AI-powered member services, pension simulation, and fraud detection",
  icon: Users,
  subTeams: [
    {
      id: "member-services",
      name: "Member Services",
      description: "AI-powered member support and pension planning services",
      mode: "Coordinate",
      icon: UserCheck,
      agents: [
        {
          id: "cimr_chatbot",
          name: "CIMR Chatbot",
          description: "Intelligent chatbot providing 24/7 member support, answering pension-related questions, and guiding members through CIMR services.",
          icon: Users,
          outputs: [
            "Member Support Responses",
            "Pension Information",
            "Service Guidance",
            "FAQ Answers",
            "Member Assistance"
          ]
        },
        {
          id: "pension_simulator",
          name: "Pension Simulator",
          description: "Interactive pension simulation agent that helps members understand their retirement benefits and plan for the future.",
          icon: Calculator,
          outputs: [
            "Pension Projections",
            "Retirement Scenarios",
            "Benefit Calculations",
            "Simulation Results",
            "Planning Recommendations"
          ]
        }
      ]
    },
    {
      id: "security-monitoring",
      name: "Security & Monitoring",
      description: "Fraud detection and retirement planning security",
      mode: "Coordinate",
      icon: Shield,
      agents: [
        {
          id: "fraud_detector",
          name: "Pension Fraud Detector",
          description: "Advanced fraud detection agent that monitors member accounts for suspicious activities and protects against pension fraud.",
          icon: AlertCircle,
          outputs: [
            "Fraud Alerts",
            "Risk Assessments",
            "Suspicious Activity Reports",
            "Security Recommendations",
            "Threat Analysis"
          ]
        },
        {
          id: "retirement_planner",
          name: "Retirement Planner",
          description: "Personalized retirement planning agent that creates customized retirement strategies based on member profiles and goals.",
          icon: Target,
          outputs: [
            "Retirement Plans",
            "Financial Projections",
            "Goal Tracking",
            "Planning Recommendations",
            "Progress Reports"
          ]
        }
      ]
    }
  ]
};

// Financial Risk Management Module
export const financialRiskTeam: Team = {
  id: "financial_risk",
  name: "Financial Risk Management Module",
  description: "AI-powered risk assessment, stress testing, and financial analysis",
  icon: TrendingDown,
  subTeams: [
    {
      id: "risk-calculation",
      name: "Risk Calculation",
      description: "Advanced risk metrics calculation and analysis",
      mode: "Coordinate",
      icon: Calculator,
      agents: [
        {
          id: "var_calculator",
          name: "VaR Calculator",
          description: "Value at Risk calculation agent that computes portfolio risk metrics and provides risk assessment for investment decisions.",
          icon: Calculator,
          outputs: [
            "VaR Calculations",
            "Risk Metrics",
            "Portfolio Risk Analysis",
            "Risk Reports",
            "Statistical Models"
          ]
        },
        {
          id: "stress_tester",
          name: "Stress Tester",
          description: "Comprehensive stress testing agent that evaluates portfolio performance under various market scenarios and stress conditions.",
          icon: Activity,
          outputs: [
            "Stress Test Results",
            "Scenario Analysis",
            "Risk Scenarios",
            "Performance Metrics",
            "Stress Reports"
          ]
        }
      ]
    },
    {
      id: "monitoring-analysis",
      name: "Monitoring & Analysis",
      description: "Credit monitoring and actuarial risk assessment",
      mode: "Coordinate",
      icon: Eye,
      agents: [
        {
          id: "credit_monitor",
          name: "Credit Monitor",
          description: "Real-time credit risk monitoring agent that tracks credit quality and identifies potential credit risks in the portfolio.",
          icon: AlertTriangle,
          outputs: [
            "Credit Risk Reports",
            "Credit Quality Analysis",
            "Risk Alerts",
            "Credit Recommendations",
            "Portfolio Health"
          ]
        },
        {
          id: "actuarial_risk_bot",
          name: "Actuarial Risk Bot",
          description: "Actuarial risk assessment agent that evaluates longevity, mortality, and demographic risks affecting pension fund sustainability.",
          icon: Heart,
          outputs: [
            "Actuarial Risk Analysis",
            "Longevity Projections",
            "Mortality Risk Assessment",
            "Demographic Analysis",
            "Risk Models"
          ]
        }
      ]
    }
  ]
};

// Actuarial Projections Module
export const actuarialProjectionsTeam: Team = {
  id: "actuarial_projections",
  name: "Actuarial Projections Module",
  description: "AI-powered demographic analysis, pension calculations, and reserve optimization",
  icon: ChartBar,
  subTeams: [
    {
      id: "demographic-analysis",
      name: "Demographic Analysis",
      description: "Population demographics and longevity projections",
      mode: "Coordinate",
      icon: Users,
      agents: [
        {
          id: "demographic_ai",
          name: "Demographic AI",
          description: "Advanced demographic analysis agent that projects population structure, longevity trends, and demographic shifts affecting pension funds.",
          icon: Users,
          outputs: [
            "Demographic Projections",
            "Population Analysis",
            "Longevity Trends",
            "Demographic Reports",
            "Statistical Models"
          ]
        },
        {
          id: "pension_calculator",
          name: "Pension Calculator",
          description: "Comprehensive pension calculation agent that computes benefits, contributions, and pension entitlements based on actuarial principles.",
          icon: Calculator,
          outputs: [
            "Pension Calculations",
            "Benefit Projections",
            "Contribution Analysis",
            "Entitlement Reports",
            "Actuarial Valuations"
          ]
        }
      ]
    },
    {
      id: "optimization-planning",
      name: "Optimization & Planning",
      description: "Reserve optimization and scenario planning",
      mode: "Coordinate",
      icon: Target,
      agents: [
        {
          id: "reserve_optimizer",
          name: "Reserve Optimizer",
          description: "Intelligent reserve optimization agent that maintains optimal reserve levels while ensuring fund sustainability and regulatory compliance.",
          icon: PieChart,
          outputs: [
            "Reserve Optimization",
            "Fund Sustainability Analysis",
            "Optimization Recommendations",
            "Reserve Reports",
            "Compliance Validation"
          ]
        },
        {
          id: "scenario_planner",
          name: "Scenario Planner",
          description: "Strategic scenario planning agent that creates multiple future scenarios and develops adaptation strategies for different economic conditions.",
          icon: Brain,
          outputs: [
            "Scenario Analysis",
            "Strategic Plans",
            "Adaptation Strategies",
            "Future Projections",
            "Planning Reports"
          ]
        }
      ]
    }
  ]
};

// Allocation Optimization Module
export const allocationOptimizationTeam: Team = {
  id: "allocation_optimization",
  name: "Allocation Optimization Module",
  description: "AI-powered portfolio optimization, rebalancing, and OPCI management",
  icon: PieChartIcon,
  subTeams: [
    {
      id: "portfolio-optimization",
      name: "Portfolio Optimization",
      description: "Advanced portfolio optimization and rebalancing strategies",
      mode: "Coordinate",
      icon: TargetIcon,
      agents: [
        {
          id: "actuarial_optimizer",
          name: "Actuarial Optimizer",
          description: "AI-powered portfolio optimization agent that uses actuarial projections to optimize asset allocation and maximize long-term returns.",
          icon: TargetIcon,
          outputs: [
            "Portfolio Optimization",
            "Asset Allocation Recommendations",
            "Optimization Strategies",
            "Performance Analysis",
            "Risk-Adjusted Returns"
          ]
        },
        {
          id: "rebalancing_ai",
          name: "Rebalancing AI",
          description: "Intelligent rebalancing agent that monitors portfolio drift and executes optimal rebalancing strategies to maintain target allocations.",
          icon: Activity,
          outputs: [
            "Rebalancing Recommendations",
            "Drift Analysis",
            "Trading Strategies",
            "Portfolio Adjustments",
            "Performance Tracking"
          ]
        }
      ]
    },
    {
      id: "specialized-investments",
      name: "Specialized Investments",
      description: "OPCI optimization and scenario stress testing",
      mode: "Coordinate",
      icon: Building2,
      agents: [
        {
          id: "opci_optimizer",
          name: "OPCI Optimizer",
          description: "Real estate investment optimization agent that manages OPCI (Organisme de Placement Collectif Immobilier) allocations and maximizes real estate returns.",
          icon: Building2,
          outputs: [
            "OPCI Optimization",
            "Real Estate Analysis",
            "Property Recommendations",
            "Investment Strategies",
            "Real Estate Reports"
          ]
        },
        {
          id: "scenario_stress_tester",
          name: "Scenario Stress Tester",
          description: "Comprehensive scenario stress testing agent that evaluates portfolio performance under various market conditions and stress scenarios.",
          icon: AlertTriangle,
          outputs: [
            "Stress Test Results",
            "Scenario Analysis",
            "Risk Assessment",
            "Performance Metrics",
            "Stress Reports"
          ]
        }
      ]
    }
  ]
};

// export const fipAITeam: Team = {
//   id: "fip-ai",
//   name: "FIP AI Team",
//   description: "AI-powered Financial Insurance Platform agents for data processing, financial calculations, and scenario management",
//   icon: Building2,
//   subTeams: [
//     {
//       id: "data-processing",
//       name: "Data Processing",
//       description: "Data reading, validation, and transformation for FIP system",
//       mode: "Coordinate",
//       icon: Database,
//       agents: [
//         {
//           id: "data-processing-agent",
//           name: "Data Processing Agent",
//           description: "FIP Data Processing and Management Expert - Handle data reading, validation, and transformation for the FIP system. Manage RIC and SCG data for both P&C and L&H business units.",
//           icon: Database,
//           outputs: [
//             "Clean RIC & SCG Data",
//             "Data Quality Reports",
//             "Validated Financial Metrics",
//             "Processed Data Files",
//             "Data Transformation Results"
//           ]
//         }
//       ]
//     },
//     {
//       id: "financial-calculations",
//       name: "Financial Calculations",
//       description: "Complex financial calculations, equity projections, and financial modeling",
//       mode: "Coordinate",
//       icon: Calculator,
//       agents: [
//         {
//           id: "financial-calculations-agent",
//           name: "Financial Calculations Agent",
//           description: "FIP Financial Calculations and Modeling Expert - Perform complex financial calculations, equity projections, allocations, and financial modeling. Handle BU splits, EoF calculations, and SCG processing.",
//           icon: Calculator,
//           outputs: [
//             "Equity Projections",
//             "BU Split Calculations",
//             "EoF Calculations",
//             "Financial Ratios",
//             "Capital Requirements"
//           ]
//         }
//       ]
//     },
//     {
//       id: "scenario-management",
//       name: "Scenario Management",
//       description: "Scenario calculations, sensitivity analysis, and what-if modeling",
//       mode: "Coordinate",
//       icon: Activity,
//       agents: [
//         {
//           id: "scenario-management-agent",
//           name: "Scenario Management Agent",
//           description: "FIP Scenario Analysis and Sensitivity Testing Expert - Handle scenario calculations, sensitivity analysis, and what-if modeling. Process multiple scenarios, apply shocks, and perform stress testing.",
//           icon: Activity,
//           outputs: [
//             "Scenario Analysis Reports",
//             "Sensitivity Analysis Results",
//             "Stress Test Reports",
//             "What-If Modeling Outputs",
//             "Risk Assessment Reports"
//           ]
//         }
//       ]
//     }
//   ]
// };

export const allTeams = [
  acapsComplianceTeam,
  memberRelationsTeam,
  financialRiskTeam,
  actuarialProjectionsTeam,
  allocationOptimizationTeam
];
