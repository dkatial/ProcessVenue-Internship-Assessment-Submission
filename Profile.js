import React, { useEffect, useState } from "react";
import { getProfile } from "../api";

const Profile = () => {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    getProfile().then(data => setProfile(data));
  }, []);

  if (!profile) return <div>Loading...</div>;

  return (
    <div>
      <h2>{profile.name}</h2>
      <p>Email: {profile.email}</p>
      <p>Education: {profile.education}</p>
      <p>
        Links:{" "}
        <a href={profile.github} target="_blank" rel="noopener noreferrer">Github</a> |{" "}
        <a href={profile.linkedin} target="_blank" rel="noopener noreferrer">LinkedIn</a> |{" "}
        <a href={profile.portfolio} target="_blank" rel="noopener noreferrer">Portfolio</a>
      </p>
      <h3>Skills:</h3>
      <ul>
        {profile.skills.map((skill, i) => <li key={i}>{skill}</li>)}
      </ul>
      <h3>Projects:</h3>
      <ul>
        {profile.projects.map((p, i) => (
          <li key={i}>
            <strong>{p.title}</strong>: {p.description} (<a href={p.links} target="_blank" rel="noopener noreferrer">Link</a>)
          </li>
        ))}
      </ul>
      <h3>Work Experience:</h3>
      <ul>
        {profile.work.map((w, i) => (
          <li key={i}>
            {w.role} at {w.company} ({w.duration})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Profile;
