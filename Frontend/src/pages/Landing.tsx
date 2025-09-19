import { useNavigate } from "react-router-dom";
import { Card, CardContent } from "@/components/ui/card";
import { Users, Shield, Code, Zap, Brain, Globe, BarChart3, Building2 } from "lucide-react";

const teams = [
  { id: "scenario-optimization", name: "FiP Scenario Simulation AI Module", icon: BarChart3, description: "AI-powered Excel scenario mix analysis, optimization, and reporting for insurance portfolios" },
  // { id: "fip-ai", name: "FIP AI Team", icon: Building2, description: "AI-powered Financial Insurance Platform agents for data processing, financial calculations, and scenario management" },
  // { id: "development", name: "Development Team", icon: Code, description: "Software development and engineering" },
  // { id: "security", name: "Security Team", icon: Shield, description: "Cybersecurity and threat analysis" },
  // { id: "operations", name: "Operations Team", icon: Zap, description: "Infrastructure and deployment" },
  // { id: "research", name: "Research Team", icon: Brain, description: "AI research and innovation" },
  // { id: "product", name: "Product Team", icon: Globe, description: "Product strategy and management" },
  // { id: "support", name: "Support Team", icon: Users, description: "Customer success and support" }
];

const Landing = () => {
  const navigate = useNavigate();

  const handleTeamClick = (teamId: string) => {
    navigate(`/team/${teamId}`);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-first-color py-8 px-6 shadow-lg">
        <div className="max-w-6xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-fourth-color mb-4">
            Team Hub
          </h1>
          <p className="text-xl text-fourth-color/80 max-w-2xl mx-auto">
            Connect with specialized teams and their AI agents to get instant help and collaboration
          </p>
        </div>
      </header>

      {/* Teams Grid */}
      <main className="max-w-6xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {teams.map((team) => {
            const IconComponent = team.icon;
            return (
              <Card
                key={team.id}
                className="bg-second-color border-0 hover:bg-third-color transition-smooth cursor-pointer transform hover:scale-105 shadow-lg hover:shadow-xl"
                onClick={() => handleTeamClick(team.id)}
              >
                <CardContent className="p-6 text-center">
                  <div className="mb-4 flex justify-center">
                    <IconComponent className="h-12 w-12 text-fourth-color" />
                  </div>
                  <h3 className="text-xl font-semibold text-fourth-color mb-2">
                    {team.name}
                  </h3>
                  <p className="text-fourth-color/70">
                    {team.description}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </main>
    </div>
  );
};

export default Landing;