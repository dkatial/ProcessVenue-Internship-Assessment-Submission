import React, { useState } from "react";
import { searchAll } from "../api";

const Search = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const handleSearch = () => {
    searchAll(query).then(data => setResults(data));
  };

  return (
    <div>
      <h2>Search</h2>
      <input
        type="text"
        placeholder="Search skills, projects, work..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>

      <ul>
        {results.map((r, i) => (
          <li key={i}>
            {r.type === "skill" && <span>Skill: {r.name}</span>}
            {r.type === "project" && <span>Project: {r.title} - {r.description}</span>}
            {r.type === "work" && <span>Work: {r.role} at {r.company}</span>}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Search;
