import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Home } from "lucide-react";

const NotFound = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="text-center max-w-md mx-auto px-6">
        <h1 className="text-6xl font-bold text-third-color mb-4">404</h1>
        <h2 className="text-2xl font-semibold text-fourth-color mb-4">Page Not Found</h2>
        <p className="text-fourth-color/70 mb-8">
          Sorry, the page you're looking for doesn't exist or has been moved.
        </p>
        <Link to="/">
          <Button className="bg-third-color hover:bg-third-color/80 text-first-color">
            <Home className="h-4 w-4 mr-2" />
            Return to Home
          </Button>
        </Link>
      </div>
    </div>
  );
};

export default NotFound;
