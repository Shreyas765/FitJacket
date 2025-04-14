import React, { useState } from "react";

const App = () => {
  const [account, setAccount] = useState({ email: "", password: "" });
  const [goals, setGoals] = useState("");
  const [workouts, setWorkouts] = useState([]);
  const [workoutInput, setWorkoutInput] = useState("");

  const handleLogin = () => {
    alert("Login simulated for " + account.email);
  };

  const handleSetGoals = () => {
    alert("Fitness goal set: " + goals);
  };

  const handleLogWorkout = () => {
    if (workoutInput) {
      setWorkouts([...workouts, workoutInput]);
      setWorkoutInput("");
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif", maxWidth: "600px", margin: "auto" }}>
      <h1>Fitness App Demo</h1>

      <section style={{ marginBottom: "2rem" }}>
        <h2>1. Login</h2>
        <input
          type="email"
          placeholder="Email"
          value={account.email}
          onChange={(e) => setAccount({ ...account, email: e.target.value })}
          style={{ display: "block", marginBottom: "0.5rem", width: "100%", padding: "0.5rem" }}
        />
        <input
          type="password"
          placeholder="Password"
          value={account.password}
          onChange={(e) => setAccount({ ...account, password: e.target.value })}
          style={{ display: "block", marginBottom: "0.5rem", width: "100%", padding: "0.5rem" }}
        />
        <button onClick={handleLogin} style={{ padding: "0.5rem 1rem" }}>Login</button>
      </section>

      <section style={{ marginBottom: "2rem" }}>
        <h2>2. Set Fitness Goal</h2>
        <input
          type="text"
          placeholder="e.g. Run 5km"
          value={goals}
          onChange={(e) => setGoals(e.target.value)}
          style={{ display: "block", marginBottom: "0.5rem", width: "100%", padding: "0.5rem" }}
        />
        <button onClick={handleSetGoals} style={{ padding: "0.5rem 1rem" }}>Save Goal</button>
      </section>

      <section>
        <h2>3. Log Workout</h2>
        <input
          type="text"
          placeholder="e.g. 30 min cardio"
          value={workoutInput}
          onChange={(e) => setWorkoutInput(e.target.value)}
          style={{ display: "block", marginBottom: "0.5rem", width: "100%", padding: "0.5rem" }}
        />
        <button onClick={handleLogWorkout} style={{ padding: "0.5rem 1rem" }}>Add Workout</button>

        <div style={{ marginTop: "1rem" }}>
          <h3>Workout History</h3>
          <ul>
            {workouts.map((workout, index) => (
              <li key={index}>{workout}</li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  );
};

export default App;
