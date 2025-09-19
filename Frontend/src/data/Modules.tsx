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
  Workflow
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

export const scenarioOptimizationTeam: Team = {
  id: "scenario-optimization",
  name: "FiP Scenario Simulation AI Module",
  description: "AI-powered Excel scenario mix analysis, optimization, and reporting for insurance portfolios",
  icon: BarChart3,
  subTeams: [
    {
      id: "data-management",
      name: "Data Management",
      description: "Excel data loading, validation, and structured access to financial metrics",
      mode: "Coordinate",
      icon: Database,
      agents: [
        {
          id: "data-access-agent",
          name: "Data Access Agent",
          description: "Excel Scenario Data Access and Management Expert - Loading, accessing, and managing Excel scenario mix data with clean, structured access to financial metrics",
          icon: Database,
          outputs: [
            "Clean Excel Scenario Data",
            "Structured Financial Metrics Access",
            "Data Quality Reports",
            "Portfolio & Year Management",
            "Data Validation Results"
          ]
        }
      ]
    },
    {
      id: "computation-modeling",
      name: "Computation & Modeling",
      description: "Financial calculations, scenario modeling, and optimization algorithms",
      mode: "Coordinate",
      icon: Calculator,
      agents: [
        {
          id: "computation-agent",
          name: "Computation Agent",
          description: "Financial Calculations and Scenario Modeling Expert - Performing complex financial calculations, applying shocks, running scenarios, and executing optimization algorithms",
          icon: Calculator,
          outputs: [
            "Shock Application Results",
            "Scenario Modeling Outputs",
            "Portfolio Optimization Recommendations",
            "Financial Calculations",
            "Scenario Comparison Analysis"
          ]
        }
      ]
    },
    {
      id: "analytics-insights",
      name: "Analytics & Insights",
      description: "Financial analytics, risk analysis, and business intelligence",
      mode: "Coordinate",
      icon: TrendingUp,
      agents: [
        {
          id: "analytics-insights-agent",
          name: "Analytics & Insights Agent",
          description: "Financial Analytics and Business Intelligence Expert - Analyzing financial data to generate insights, perform risk analysis, conduct stress testing, and provide business intelligence",
          icon: TrendingUp,
          outputs: [
            "Financial Analysis Reports",
            "Risk Assessment & Concentration Analysis",
            "Stress Test Results",
            "Sensitivity Analysis",
            "Business Intelligence Insights"
          ]
        }
      ]
    },
    {
      id: "reporting-visualization",
      name: "Reporting & Visualization",
      description: "Data visualization, report generation, and stakeholder communication",
      mode: "Coordinate",
      icon: FileText,
      agents: [
        {
          id: "reporting-visualization-agent",
          name: "Reporting & Visualization Agent",
          description: "Data Visualization and Report Generation Expert - Creating visualizations, generating reports, and exporting analysis results in various formats for stakeholders",
          icon: FileText,
          outputs: [
            "Professional Charts & Visualizations",
            "Comprehensive Analysis Reports",
            "Multi-format Data Exports",
            "Executive Dashboards",
            "Stakeholder Presentations"
          ]
        }
      ]
    },
    {
      id: "master-coordination",
      name: "Master Coordination",
      description: "Orchestrating specialized agents for comprehensive scenario analysis",
      mode: "Coordinate",
      icon: Brain,
      agents: [
        {
          id: "scenario-optimization-team",
          name: "Scenario Optimization Team",
          description: "Master Scenario Optimization Coordinator - Orchestrating the team of specialized agents to provide comprehensive scenario analysis, optimization, and reporting services",
          icon: Brain,
          outputs: [
            "Integrated Analysis Results",
            "Coordinated Team Outputs",
            "Master Recommendations",
            "Quality Assurance Reports",
            "Comprehensive Scenario Insights"
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

export const allTeams = [scenarioOptimizationTeam]; //, fipAITeam];
