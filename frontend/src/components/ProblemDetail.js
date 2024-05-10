import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import "./ProblemDetail.css"; // Import the CSS file

function ProblemDetail() {
  const { code } = useParams();
  const [problem, setProblem] = useState(null);
  const [codeInput, setCodeInput] = useState("");
  const [selectedLanguage, setSelectedLanguage] = useState("c"); // Default to 'c'
  const [submitting, setSubmitting] = useState(false);
  const [responseOutput, setResponseOutput] = useState("");

  useEffect(() => {
    const accessToken = localStorage.getItem("accessToken"); // Retrieve access token from local storage

    const config = {
      headers: {
        Authorization: `Bearer ${accessToken}`, // Include access token in Authorization header
      },
    };
    axios
      .get(`http://localhost:8000/main/api/problem/${code}/`, config)
      .then((response) => {
        setProblem(response.data);
      })
      .catch((error) => {
        console.error("Error fetching problem detail:", error);
      });
  }, [code]);

  const handleSubmit = () => {
    // Handle code submission here
    setSubmitting(true);
    // Example: Send code and selected language to backend for processing
    console.log("Submitted code:", codeInput);
    console.log("Selected language:", selectedLanguage);

    const formData = new URLSearchParams();
    formData.append("lang", selectedLanguage);
    formData.append("problem_code", code); // Assuming problemCode is available
    formData.append("code", codeInput);

    const accessToken = localStorage.getItem("accessToken"); // Retrieve access token from local storage

    const config = {
      headers: {
        Authorization: `Bearer ${accessToken}`, // Include access token in Authorization header
      },
    };

    axios.post("http://localhost:8000/main/api/execute/", formData, config)
  .then((response) => {
    console.log("Response:", response.data);
    setResponseOutput(response.data.result);
    // Handle response here
  })
  .catch((error) => {
    console.error("Error:", error);
  })
  .finally(() => {
    // Reset code input
    setCodeInput("");
    setSubmitting(false);
  });

  };

  if (!problem) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="problem-detail-container">
      <h2 className="problem-detail-title">{problem.name}</h2>
      <div className="problem-detail-content">
        <div className="problem-statement">{problem.statement}</div>
      </div>
      {/* <div className="problem-detail-content"> */}
      <div className="language-select">
        <label htmlFor="language">Select Language:</label>
        <select
          id="language"
          value={selectedLanguage}
          onChange={(e) => setSelectedLanguage(e.target.value)}
        >
          <option value="c">C</option>
          <option value="cpp">C++</option>
          <option value="py">Python</option>
        </select>
      </div>
      <textarea
        className="code-input"
        placeholder="Enter your code here..."
        value={codeInput}
        onChange={(e) => setCodeInput(e.target.value)}
      />
      <button
        className="submit-button"
        onClick={handleSubmit}
        disabled={submitting}
      >
        {submitting ? "Submitting..." : "Submit"}
      </button>
      {/* Display response output */}
      {responseOutput && (
        <div>
          <h2>Output:</h2>
          <pre>{responseOutput}</pre>
        </div>
      )}
    </div>
  );
}

export default ProblemDetail;
