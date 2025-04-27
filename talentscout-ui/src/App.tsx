import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import HRDashboard from "./components/HRDashboard/HRDashboard";
import AIInterviewer from "./components/AIInterviewer/AIInterviewer";
import NotFound from "./components/NotFound/NotFound";
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HRDashboard />} />
        <Route path="/ai-interviewer" element={<AIInterviewer />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
