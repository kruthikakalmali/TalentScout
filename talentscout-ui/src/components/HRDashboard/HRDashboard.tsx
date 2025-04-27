import React, { useState } from "react";

type JobDescription = {
  id: number;
  title: string;
  skills: string[];
};

type Candidate = {
  id: number;
  name: string;
  skills: string[];
};

const jobDescriptions: JobDescription[] = [
  {
    id: 1,
    title: "Frontend Developer",
    skills: ["React", "TypeScript", "CSS", "HTML"],
  },
  {
    id: 2,
    title: "Backend Developer",
    skills: ["Node.js", "Express", "MongoDB", "TypeScript"],
  },
];

const applications: Candidate[] = [
  {
    id: 101,
    name: "Alice Johnson",
    skills: ["React", "CSS", "HTML"],
  },
  {
    id: 102,
    name: "Bob Smith",
    skills: ["Node.js", "Express", "Docker"],
  },
  {
    id: 103,
    name: "Charlie Lee",
    skills: ["React", "TypeScript", "GraphQL"],
  },
];

const matchCandidates = (jdSkills: string[], candidates: Candidate[]) => {
  return candidates
    .map((candidate) => {
      const matchCount = candidate.skills.filter((skill) =>
        jdSkills.includes(skill)
      ).length;
      return { ...candidate, matchCount };
    })
    .filter((c) => c.matchCount > 0)
    .sort((a, b) => b.matchCount - a.matchCount);
};

const HRDashboard = () => {
  const [selectedJob, setSelectedJob] = useState<JobDescription | null>(null);

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #1e3c72, #2a5298)",
        color: "#fff",
        fontFamily: "Inter, sans-serif",
        padding: "40px",
      }}
    >
      <h1
        style={{
          textAlign: "center",
          fontSize: "2.5rem",
          marginBottom: "40px",
        }}
      >
        🎯 TalentScout — Smart JD Matcher
      </h1>

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "40px",
          justifyContent: "center",
        }}
      >
        {/* Left side - JD Cards */}
        <div style={{ flex: "1 1 400px", maxWidth: "500px" }}>
          <h2 style={{ fontSize: "1.8rem", marginBottom: "20px" }}>
            📄 Job Descriptions
          </h2>
          {jobDescriptions.map((jd) => (
            <div
              key={jd.id}
              onClick={() => setSelectedJob(jd)}
              style={{
                background: "rgba(255, 255, 255, 0.1)",
                padding: "20px",
                borderRadius: "15px",
                marginBottom: "20px",
                backdropFilter: "blur(8px)",
                cursor: "pointer",
                boxShadow:
                  selectedJob?.id === jd.id
                    ? "0 0 15px rgba(255,255,255,0.6)"
                    : "0 0 10px rgba(0,0,0,0.2)",
                transition: "0.3s ease",
              }}
            >
              <h3 style={{ fontSize: "1.3rem", marginBottom: "10px" }}>
                {jd.title}
              </h3>
              <p style={{ opacity: 0.9 }}>🛠️ {jd.skills.join(", ")}</p>
            </div>
          ))}
        </div>

        {/* Right side - Matches */}
        <div style={{ flex: "1 1 400px", maxWidth: "500px" }}>
          <h2 style={{ fontSize: "1.8rem", marginBottom: "20px" }}>
            👥 Matched Candidates
          </h2>
          {selectedJob ? (
            <>
              <h3 style={{ fontSize: "1.2rem", marginBottom: "10px" }}>
                For: {selectedJob.title}
              </h3>
              {matchCandidates(selectedJob.skills, applications).map(
                (candidate) => (
                  <div
                    key={candidate.id}
                    style={{
                      background: "rgba(255, 255, 255, 0.1)",
                      padding: "20px",
                      borderRadius: "15px",
                      marginBottom: "20px",
                      backdropFilter: "blur(8px)",
                      transition: "0.3s",
                      boxShadow: "0 0 10px rgba(0,0,0,0.3)",
                    }}
                  >
                    <h4 style={{ fontSize: "1.1rem", marginBottom: "8px" }}>
                      {candidate.name}
                    </h4>
                    <p style={{ opacity: 0.9 }}>
                      💼 {candidate.skills.join(", ")}
                    </p>
                    <p style={{ marginTop: "8px" }}>
                      🔢 Match Score: {candidate.matchCount}
                    </p>
                  </div>
                )
              )}
              {matchCandidates(selectedJob.skills, applications).length ===
                0 && <p style={{ opacity: 0.8 }}>No strong matches found.</p>}
            </>
          ) : (
            <p style={{ opacity: 0.8 }}>
              Select a job description to view matches.
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default HRDashboard;
