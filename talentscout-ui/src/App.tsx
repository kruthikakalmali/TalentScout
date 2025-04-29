import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import HRJobPortal from "./components/HRJobPortal/HRJobPortal";
import CandidateAIInterviewPortal from "./components/CandidateAIInterviewPortal/CandidateAIInterviewPortal";
import InterviewCompletedCandidates from "./components/HRJobPortal/InterviewCompletedCandidates";
import GeneratedReportCandidate from "./components/CandidateAIInterviewPortal/components/GeneratedReportCandidate";
import GeneratedReportRecruiter from "./components/HRJobPortal/GeneratedReportRecruiter";
import NotFound from "./components/NotFound/NotFound";

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HRJobPortal />} />
          <Route path="/recruiter" element={<HRJobPortal />} />
          <Route
            path="/recruiter/interview-completed-candidates"
            element={<InterviewCompletedCandidates />}
          />
          <Route
            path="/recruiter/generated-feedback-report"
            element={<GeneratedReportRecruiter />}
          />
          <Route
            path="/candidate-ai-interview-portal"
            element={<CandidateAIInterviewPortal />}
          />
          <Route
            path="/candidate/generated-feedback-report"
            element={<GeneratedReportCandidate />}
          />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
