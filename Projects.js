import React, { useEffect, useState } from "react";
import { getProjectsBySkill, getTopSkills } from "../api";

const Projects = () => {
  const [skill, setSkill] = useState("");
  const [projects, setProjects] = useState([]);
  const [topSkills, setTopSkills] = useState([]);

  useEffect(() => {
    getTopSkills().then(data => setTopSkills(data));
  }, []);

  const searchProjects = () => {
    getProjectsBySkill(skill).then(data => setProjects(data));
  };

  return (
    <div>
      <h2>Projects</h2>
      <input
        type="text"
        placeholder="Search by skill"
        value={skill}
        onChange={(e) => setSkill(e.target.value)}
      />
      <button onClick={searchProjects}>Search</button>

      <h3>Top Skills:</h3>
      <ul>
        {topSkills.map((s, i) => <li key={i}>{s}</li>)}
      </ul>

      <h3>Results:</h3>
      <ul>
        {projects.map((p, i) => (
          <li key={i}>
            <strong>{p.title}</strong>: {p.description} (<a href={p.links} target="_blank" rel="noopener noreferrer">Link</a>)
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Projects;
