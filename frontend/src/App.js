import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const App = () => {
  const [formData, setFormData] = useState({
    location: "",
    date: "",
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setPrediction(null);

    try {
      const response = await axios.post("http://localhost:8000/predict", formData);
      if (response.data.error) {
        setError(response.data.error);
      } else {
        setPrediction(response.data.rain_prediction);
      }
    } catch (err) {
      console.error("Error fetching prediction:", err);
      setError("Failed to get prediction. Ensure backend is running.");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h2>Rainfall Prediction</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="location"
          placeholder="Enter State/UT"
          value={formData.location}
          onChange={handleChange}
          required
        />
        <input
          type="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}
      {prediction !== null && (
        <h3 className="result">
          Rain Prediction for {formData.date}: <span>{prediction}</span>
        </h3>
      )}
    </div>
  );
};

export default App;

