import React, { useState, useEffect } from "react";
import axios from "axios";
import "./ProblemList.css"; // Import the CSS file

function ProblemList() {
  const [problems, setProblems] = useState([]);

  useEffect(() => {
    const accessToken = localStorage.getItem("accessToken"); // Retrieve access token from local storage

    const config = {
      headers: {
        Authorization: `Bearer ${accessToken}`, // Include access token in Authorization header
      },
    };
    axios
      .get("http://localhost:8000/main/api/problems/",config)
      .then((response) => {
        setProblems(response.data);
      })
      .catch((error) => {
        console.error("Error fetching problems:", error);
      });
  }, []);

  return (
    <div className="problem-list-container">
      <h2 className="problem-list-title">Available Problems</h2>
      <div className="problem-list">
        {problems.map((problem) => (
          <div key={problem.id} className="problem-item">
            <div className="problem-info">
              <span className="problem-name">{problem.name}</span>
              {/* <span className="problem-code">Code: {problem.code}</span> */}
            </div>
            <a href={`/problem/${problem.code}`} className="problem-link">
              Solve
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ProblemList;
