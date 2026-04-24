import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Recommendations() {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedData = localStorage.getItem("careerFormData");

    if (!savedData) {
      navigate("/");
      return;
    }

    const formData = JSON.parse(savedData);

    const fetchRecommendations = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/match-jobs", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });

        const data = await response.json();
        setJobs(data.jobs || []);
      } catch (error) {
        console.error("Error fetching recommendations:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [navigate]);

  return (
    <div className="app">
      <div className="card results-card">
        <h1>Your Job Matches</h1>

        <button className="secondary-btn top-back-btn" onClick={() => navigate("/")}>
          Back to Form
        </button>

        {loading ? (
          <p>Loading recommendations...</p>
        ) : jobs.length === 0 ? (
          <p>No matching jobs found yet.</p>
        ) : (
          <div className="results-list">
            {jobs.map((job, index) => (
              <div key={index} className="job-card">
                <h2>{job.title}</h2>
                <p><strong>Company:</strong> {job.company}</p>
                <p><strong>Location:</strong> {job.location}</p>
                <p><strong>Match Score:</strong> {job.match_score}%</p>
                <p><strong>Education Match:</strong> {job.education_match ? "Yes" : "No"}</p>
                {job.missing_education && (
                  <p><strong>Missing Education:</strong> {job.missing_education}</p>
                )}

                <p><strong>Why this matches you:</strong> {job.why_match}</p>
                <p><strong>Matched Skills:</strong> {job.matched_skills.join(", ") || "None"}</p>
                <p><strong>Missing Skills:</strong> {job.missing_skills.join(", ") || "None"}</p>

                <p><strong>Suggested Projects:</strong></p>
                <ul>
                  {job.projects.map((project, i) => (
                    <li key={i}>{project}</li>
                  ))}
                </ul>

                <p><strong>Suggested Certifications:</strong></p>
                <ul>
                  {job.certifications.map((cert, i) => (
                    <li key={i}>{cert}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Recommendations;