import React, { useState } from "react";
import axios from "axios";
import "./App.css";  

const App = () => {
  const [formData, setFormData] = useState({
    location: "",
    jun_sep_rainfall: "",
    oct_dec_rainfall: "",
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
      const response = await axios.post("http://localhost:8000/predict", formData, {headers: { "Content-Type": "application/json"}});
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
        <input type="text" name="location" placeholder="State/UT Name" value={formData.location} onChange={handleChange} required />
        <input type="number" name="jun_sep_rainfall" placeholder="Rainfall (Jun-Sep)" value={formData.jun_sep_rainfall} onChange={handleChange} required />
        <input type="number" name="oct_dec_rainfall" placeholder="Rainfall (Oct-Dec)" value={formData.oct_dec_rainfall} onChange={handleChange} required />
        <button type="submit" disabled={loading}>{loading ? "Predicting..." : "Predict"}</button>
      </form>

      {loading && <p>Loading prediction...</p>}
      {error && <p className="error">{error}</p>}
      {prediction !== null && (
        <h3 className="result">
          Predicted Rainfall: <span>{prediction}</span>
        </h3>
      )}
    </div>
  );
};

export default App;
