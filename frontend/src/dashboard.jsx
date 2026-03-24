import { useEffect, useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

const COLORS = {
  High: "#ef5350",
  Medium: "#ffb300",
  Low: "#43a047"
};

function Dashboard() {
  const [summary, setSummary] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [selectedRisk, setSelectedRisk] = useState("All");
  const [loading, setLoading] = useState(true);

  const [productId, setProductId] = useState("");
  const [productData, setProductData] = useState(null);

  // ✅ FETCH DASHBOARD DATA
  useEffect(() => {
    fetch("http://localhost:8000/dashboard-summary")
      .then(res => res.json())
      .then(data => {
        console.log("Dashboard data:", data);

        const cleaned = data.map(item => ({
          ...item,
          expected_loss: Number(item.expected_loss) || 0
        }));

        setSummary(cleaned);
        setFilteredData(cleaned);
        setLoading(false);
      })
      .catch(err => {
        console.error("Fetch error:", err);
        setLoading(false);
      });
  }, []);

  // ✅ FILTERING
  useEffect(() => {
    if (selectedRisk === "All") {
      setFilteredData(summary);
    } else {
      setFilteredData(summary.filter(p => p.risk === selectedRisk));
    }
  }, [selectedRisk, summary]);

  // ✅ PIE DATA
  const pieData = [
    { name: "High", value: summary.filter(p => p.risk === "High").length },
    { name: "Medium", value: summary.filter(p => p.risk === "Medium").length },
    { name: "Low", value: summary.filter(p => p.risk === "Low").length }
  ];

  // ✅ BAR DATA
  const topLossProducts = [...filteredData]
    .sort((a, b) => b.expected_loss - a.expected_loss)
    .slice(0, 10);

  // ✅ PRODUCT SEARCH
  const fetchProductDetails = async () => {
    if (!productId) return;

    try {
      const res = await fetch(
        `http://localhost:8000/product-insights/${productId}`
      );

      if (!res.ok) {
        throw new Error("Product not found");
      }

      const data = await res.json();
      console.log("Product data:", data);
      setProductData(data);

    } catch (err) {
      console.error(err);
      alert("Backend not running or product not found");
    }
  };

  return (
    <div style={{ display: "flex", fontFamily: "Segoe UI, sans-serif" }}>

      {/* SIDEBAR */}
      <div style={{
        width: "240px",
        background: "#1f2937",
        color: "white",
        minHeight: "100vh",
        padding: "30px 20px"
      }}>
        <h2 style={{ marginBottom: "40px" }}>📊 Inventory AI</h2>
        <p>Dashboard</p>
        <p>Analytics</p>
        <p>Reports</p>
        <p>Settings</p>
      </div>

      {/* MAIN CONTENT */}
      <div style={{
        flex: 1,
        padding: "40px",
        background: "#f3f4f6",
        minHeight: "100vh"
      }}>

        <h1 style={{ marginBottom: "30px", color: "#111827" }}>
          Inventory Risk Intelligence Dashboard
        </h1>

        {loading && <p>Loading dashboard...</p>}

        {/* FILTER BUTTONS */}
        <div style={{ marginBottom: "30px", display: "flex", gap: "10px" }}>
          {["All", "High", "Medium", "Low"].map(risk => (
            <button
              key={risk}
              onClick={() => setSelectedRisk(risk)}
              style={{
                padding: "8px 16px",
                borderRadius: "20px",
                border: "none",
                cursor: "pointer",
                background:
                  risk === "High"
                    ? COLORS.High
                    : risk === "Medium"
                    ? COLORS.Medium
                    : risk === "Low"
                    ? COLORS.Low
                    : "#e5e7eb",
                color: risk === "All" ? "#111" : "white"
              }}
            >
              {risk}
            </button>
          ))}
        </div>

        {/* CHARTS */}
        {!loading && summary.length > 0 && (
          <div style={{ display: "flex", gap: "30px", flexWrap: "wrap" }}>

            {/* PIE */}
            <div style={{
              flex: 1,
              minWidth: 350,
              background: "white",
              padding: "20px",
              borderRadius: "16px",
              boxShadow: "0 4px 12px rgba(0,0,0,0.08)"
            }}>
              <h3>Risk Distribution</h3>

              <div style={{ width: "100%", height: 320 }}>
                <ResponsiveContainer>
                  <PieChart>
                    <Pie
                      data={pieData}
                      dataKey="value"
                      outerRadius={110}
                      label
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={index} fill={COLORS[entry.name]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* BAR */}
            <div style={{
              flex: 1,
              minWidth: 350,
              background: "white",
              padding: "20px",
              borderRadius: "16px",
              boxShadow: "0 4px 12px rgba(0,0,0,0.08)"
            }}>
              <h3>Top 10 Loss Making Products</h3>

              <div style={{ width: "100%", height: 320 }}>
                <ResponsiveContainer>
                  <BarChart data={topLossProducts}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="product_name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="expected_loss" fill="#6366f1" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

          </div>
        )}

        {/* PRODUCT SEARCH */}
        <div style={{ marginTop: "50px" }}>
          <h2>Analyze Specific Product</h2>

          <input
            type="number"
            placeholder="Enter Product ID"
            value={productId}
            onChange={(e) => setProductId(e.target.value)}
            style={{
              padding: "10px 15px",
              borderRadius: "8px",
              border: "1px solid #d1d5db",
              marginRight: "10px"
            }}
          />

          <button
            onClick={fetchProductDetails}
            style={{
              padding: "10px 20px",
              borderRadius: "8px",
              border: "none",
              background: "#4f46e5",
              color: "white",
              cursor: "pointer"
            }}
          >
            Analyze
          </button>

          {productData && (
            <div style={{
              marginTop: "25px",
              padding: "25px",
              borderRadius: "16px",
              background: "white",
              boxShadow: "0 4px 12px rgba(0,0,0,0.08)"
            }}>
              <h3>{productData.product_name}</h3>
              <p><strong>Risk:</strong> {productData.predicted_risk_category}</p>
              <p><strong>Confidence:</strong> {(productData.confidence_score * 100).toFixed(1)}%</p>
              <p><strong>Expected Loss:</strong> ₹{productData.expected_revenue_loss}</p>
              <p><strong>Suggested Discount:</strong> {productData.suggested_discount}%</p>
              <p><strong>Urgency:</strong> {productData.urgency_level}</p>
              <p><strong>Recommendation:</strong> {productData.recommendation}</p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}

export default Dashboard;