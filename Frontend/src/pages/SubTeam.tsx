import { useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ChevronLeft, ChevronDown, ChevronRight, Bot, User } from "lucide-react";
import { scenarioOptimizationTeam, allTeams } from "@/data/Modules";

const subTeamsData = {
  development: [
    {
      id: "frontend",
      name: "Frontend Development",
      agents: ["React Specialist", "UX Expert", "TypeScript Pro"]
    },
    {
      id: "backend",
      name: "Backend Development", 
      agents: ["API Architect", "Database Expert", "Security Specialist"]
    },
    {
      id: "mobile",
      name: "Mobile Development",
      agents: ["iOS Developer", "Android Developer", "Flutter Expert"]
    }
  ],
  security: [
    {
      id: "threat",
      name: "Threat Analysis",
      agents: ["Penetration Tester", "Vulnerability Scanner", "Risk Assessor"]
    },
    {
      id: "compliance",
      name: "Compliance & Audit",
      agents: ["GDPR Specialist", "SOC Auditor", "Policy Expert"]
    }
  ],
  operations: [
    {
      id: "devops",
      name: "DevOps & CI/CD",
      agents: ["Docker Expert", "Kubernetes Specialist", "Pipeline Engineer"]
    },
    {
      id: "monitoring",
      name: "Monitoring & Alerts",
      agents: ["Performance Monitor", "Log Analyzer", "Incident Responder"]
    }
  ],
  research: [
    {
      id: "ml",
      name: "Machine Learning",
      agents: ["ML Engineer", "Data Scientist", "Model Optimizer"]
    },
    {
      id: "nlp",
      name: "Natural Language Processing",
      agents: ["NLP Researcher", "Language Model Expert", "Text Analyzer"]
    }
  ],
  product: [
    {
      id: "strategy",
      name: "Product Strategy",
      agents: ["Product Manager", "Market Analyst", "Feature Planner"]
    },
    {
      id: "design",
      name: "Design & UX",
      agents: ["UI Designer", "UX Researcher", "Prototyper"]
    }
  ],
  support: [
    {
      id: "customer",
      name: "Customer Success",
      agents: ["Support Specialist", "Onboarding Expert", "Account Manager"]
    },
    {
      id: "technical",
      name: "Technical Support",
      agents: ["Technical Writer", "Bug Tracker", "Solution Architect"]
    }
  ]
};

const SubTeam = () => {
  const { teamId } = useParams();
  const navigate = useNavigate();
  const [expandedSubTeam, setExpandedSubTeam] = useState<string | null>(null);
  
  // Handle teams from allTeams data
  const currentTeam = allTeams.find(team => team.id === teamId);
  if (currentTeam) {
    const subTeams = currentTeam.subTeams.map(st => ({
      id: st.id,
      name: st.name,
      icon: st.icon,
      agents: st.agents.map(agent => agent.name)
    }));
    const teamName = currentTeam.name;
    
    return (
      <div className="min-h-screen bg-background">
        {/* Header */}
        <header className="bg-first-color py-6 px-6 shadow-lg">
          <div className="max-w-6xl mx-auto flex items-center gap-4">
            <Link to="/">
              <Button variant="ghost" size="sm" className="text-fourth-color hover:bg-third-color">
                <ChevronLeft className="h-4 w-4 mr-2" />
                Back to Teams
              </Button>
            </Link>
            <div className="flex items-center gap-3">
              <currentTeam.icon className="h-8 w-8 text-fourth-color" />
              <h1 className="text-3xl font-bold text-fourth-color">
                {teamName}
              </h1>
            </div>
          </div>
        </header>

        {/* Sub-teams */}
        <main className="max-w-6xl mx-auto px-6 py-12">
          <div className="space-y-4">
            {subTeams.map((subTeam) => (
              <Card key={subTeam.id} className="bg-second-color border-0 shadow-lg">
                <CardContent className="p-0">
                  {/* Sub-team Header */}
                  <div
                    className="p-6 cursor-pointer hover:bg-third-color transition-smooth flex items-center justify-between"
                    onClick={() => setExpandedSubTeam(expandedSubTeam === subTeam.id ? null : subTeam.id)}
                  >
                    <div className="flex items-center gap-3">
                      <subTeam.icon className="h-6 w-6 text-fourth-color" />
                      <h3 className="text-xl font-semibold text-fourth-color">
                        {subTeam.name}
                      </h3>
                    </div>
                    {expandedSubTeam === subTeam.id ? (
                      <ChevronDown className="h-5 w-5 text-fourth-color" />
                    ) : (
                      <ChevronRight className="h-5 w-5 text-fourth-color" />
                    )}
                  </div>

                  {/* Agents List */}
                  {expandedSubTeam === subTeam.id && (
                    <div className="px-6 pb-6 border-t border-third-color/20">
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 mt-4">
                        {subTeam.agents.map((agent, index) => (
                          <Button
                            key={index}
                            variant="ghost"
                            className="bg-third-color/20 hover:bg-third-color text-fourth-color justify-start transition-smooth"
                            onClick={() => navigate(`/team/${teamId}/subteam/${subTeam.id}/chat`)}
                          >
                            <Bot className="h-4 w-4 mr-2" />
                            {agent}
                          </Button>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </main>
      </div>
    );
  }
  
  const subTeams = subTeamsData[teamId as keyof typeof subTeamsData] || [];
  const teamName = teamId?.split(/(?=[A-Z])/).join(' ').replace(/^\w/, (c) => c.toUpperCase()) || '';

  const handleSubTeamClick = (subTeamId: string) => {
    setExpandedSubTeam(expandedSubTeam === subTeamId ? null : subTeamId);
  };

  const handleAgentClick = (subTeamId: string) => {
    navigate(`/team/${teamId}/subteam/${subTeamId}/chat`);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-first-color py-6 px-6 shadow-lg">
        <div className="max-w-6xl mx-auto flex items-center gap-4">
          <Link to="/">
            <Button variant="ghost" size="sm" className="text-fourth-color hover:bg-third-color">
              <ChevronLeft className="h-4 w-4 mr-2" />
              Back to Teams
            </Button>
          </Link>
          <h1 className="text-3xl font-bold text-fourth-color capitalize">
            {teamName} Team
          </h1>
        </div>
      </header>

      {/* Sub-teams */}
      <main className="max-w-6xl mx-auto px-6 py-12">
        <div className="space-y-4">
          {subTeams.map((subTeam) => (
            <Card key={subTeam.id} className="bg-second-color border-0 shadow-lg">
              <CardContent className="p-0">
                {/* Sub-team Header */}
                <div
                  className="p-6 cursor-pointer hover:bg-third-color transition-smooth flex items-center justify-between"
                  onClick={() => handleSubTeamClick(subTeam.id)}
                >
                  <div className="flex items-center gap-3">
                    <User className="h-6 w-6 text-fourth-color" />
                    <h3 className="text-xl font-semibold text-fourth-color">
                      {subTeam.name}
                    </h3>
                  </div>
                  {expandedSubTeam === subTeam.id ? (
                    <ChevronDown className="h-5 w-5 text-fourth-color" />
                  ) : (
                    <ChevronRight className="h-5 w-5 text-fourth-color" />
                  )}
                </div>

                {/* Agents List */}
                {expandedSubTeam === subTeam.id && (
                  <div className="px-6 pb-6 border-t border-third-color/20">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 mt-4">
                      {subTeam.agents.map((agent, index) => (
                        <Button
                          key={index}
                          variant="ghost"
                          className="bg-third-color/20 hover:bg-third-color text-fourth-color justify-start transition-smooth"
                          onClick={() => handleAgentClick(subTeam.id)}
                        >
                          <Bot className="h-4 w-4 mr-2" />
                          {agent}
                        </Button>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      </main>
    </div>
  );
};

export default SubTeam;