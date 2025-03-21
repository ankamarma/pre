import React, { useEffect, useState } from "react";

export default function StockForecast() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/predict")
      .then((response) => response.json())
      .then((data) => {
        setData(data);
        setLoading(false);
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <div className="p-6 bg-gray-100 min-h-screen flex flex-col items-center">
      <h1 className="text-2xl font-bold text-blue-600">Stock Price Forecast</h1>
      
      {loading ? (
        <p className="text-lg text-gray-700 mt-4">Loading predictions...</p>
      ) : (
        <div className="bg-white shadow-lg p-6 rounded-lg mt-6">
          <h2 className="text-xl font-semibold text-gray-800">{data.symbol}</h2>
          <p className="text-gray-700 text-lg">📈 Current Price: ${data.current_price}</p>
          <p className="text-green-600 text-lg">🔹 Predicted High: ${data.predicted_high}</p>
          <p className="text-red-600 text-lg">🔹 Predicted Low: ${data.predicted_low}</p>
        </div>
      )}
    </div>
  );
}
