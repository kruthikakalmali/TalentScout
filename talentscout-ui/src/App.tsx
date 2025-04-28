import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import HRJobPortal from "./components/HRJobPortal/HRJobPortal";
import CandidateAIInterviewPortal from "./components/CandidateAIInterviewPortal/CandidateAIInterviewPortal";
import NotFound from "./components/NotFound/NotFound";
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HRJobPortal />} />
        <Route path="/hr-job-portal" element={<HRJobPortal />} />
        <Route path="/candidate-ai-interview-portal" element={<CandidateAIInterviewPortal />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
