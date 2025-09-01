
import React from "react";
import Profile from "./components/Profile";
import Projects from "./components/Projects";
import Search from "./components/Search";

function App() {
  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ textAlign: "center", marginBottom: "20px" }}>
        Me-API Playground
      </h1>

      {/* Profile Section */}
      <section style={{ marginBottom: "40px" }}>
        <Profile />
      </section>

      <hr />
      {/* Projects Section */}
      <section style={{ margin: "40px 0" }}>
        <Projects />
      </section>

      <hr />

      {/* Search Section */}
      <section style={{ marginTop: "40px" }}>
        <Search />
      </section>
    </div>
  );
}

export default App;
