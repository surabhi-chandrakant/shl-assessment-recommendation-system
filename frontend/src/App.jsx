import React, { useState, useEffect } from "react";
import {
  Search,
  Loader2,
  CheckCircle2,
  AlertCircle,
  Download
} from "lucide-react";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const App = () => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [systemStats, setSystemStats] = useState(null);
  const [tab, setTab] = useState("search");

  const sampleQueries = [
    "Java developer with strong problem-solving skills",
    "Hiring data analyst with logical reasoning",
    "Cognitive and personality tests for analyst role",
    "Software engineer with communication skills",
    "Entry-level accountant with attention to detail"
  ];

  // ---------------------------
  // Load system health (REAL)
  // ---------------------------
  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then(res => res.json())
      .then(data => {
        setSystemStats({
          total: data.total_assessments,
          status: data.status
        });
      })
      .catch(() => setSystemStats(null));
  }, []);

  // ---------------------------
  // Search using REAL backend
  // ---------------------------
  const handleSearch = async () => {
    if (!query.trim()) {
      setError("Please enter a job description");
      return;
    }

    setLoading(true);
    setError("");
    setResults([]);

    try {
      const res = await fetch(`${API_URL}/recommend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query,
          max_results: 10
        })
      });

      if (!res.ok) throw new Error("Backend error");

      const data = await res.json();

      const formatted = data.recommendations.map(rec => {
        let shortType = "G";
        if (rec.test_type?.length) {
          const t = rec.test_type[0];
          if (t.includes("Knowledge") || t.includes("Skills")) shortType = "K";
          else if (t.includes("Personality")) shortType = "P";
          else if (t.includes("Ability")) shortType = "C";
        }

        return {
          name: rec.name,
          url: rec.url,
          category: rec.test_type.join(", "),
          duration: `${rec.duration} min`,
          score: rec.score,
          type: shortType
        };
      });

      setResults(formatted);
    } catch (e) {
      setError("Failed to fetch recommendations. Is backend running?");
    } finally {
      setLoading(false);
    }
  };

  // ---------------------------
  // Export CSV (REAL)
  // ---------------------------
  const exportCSV = () => {
    if (!results.length) return;

    const csv = [
      "Query,Assessment_url",
      ...results.map(r => `"${query}","${r.url}"`)
    ].join("\n");

    const blob = new Blob([csv], { type: "text/csv" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "shl_recommendations.csv";
    link.click();
  };

  const badgeColor = t => {
    if (t === "K") return "bg-emerald-100 text-emerald-700";
    if (t === "P") return "bg-blue-100 text-blue-700";
    if (t === "C") return "bg-amber-100 text-amber-700";
    return "bg-gray-100 text-gray-700";
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-indigo-600">
              SHL Assessment Recommendation System
            </h1>
            <p className="text-sm text-gray-600">
              Semantic matching using real SHL data
            </p>
          </div>

          {systemStats && (
            <div className="flex items-center gap-2 bg-green-50 border border-green-200 px-4 py-2 rounded-lg">
              <CheckCircle2 className="w-5 h-5 text-green-600" />
              <span className="text-green-800 text-sm font-semibold">
                {systemStats.total} Assessments Loaded
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="max-w-7xl mx-auto px-6 mt-6">
        <div className="flex gap-6 border-b">
          {["search", "api", "about"].map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`pb-2 font-medium ${
                tab === t
                  ? "border-b-2 border-indigo-600 text-indigo-600"
                  : "text-gray-600"
              }`}
            >
              {t.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* SEARCH TAB */}
        {tab === "search" && (
          <>
            <div className="bg-white p-6 rounded-xl shadow">
              <label className="block font-semibold mb-2">
                Enter Job Description or Hiring Requirement
              </label>
              <div className="flex gap-3">
                <input
                  value={query}
                  onChange={e => setQuery(e.target.value)}
                  onKeyDown={e => e.key === "Enter" && handleSearch()}
                  className="flex-1 border rounded-lg px-4 py-2"
                  placeholder="Java developer with problem-solving skills"
                />
                <button
                  onClick={handleSearch}
                  disabled={loading}
                  className="bg-indigo-600 text-white px-6 py-2 rounded-lg flex items-center gap-2"
                >
                  {loading ? <Loader2 className="animate-spin" /> : <Search />}
                  Search
                </button>
              </div>

              <div className="mt-4 flex flex-wrap gap-2">
                {sampleQueries.map((q, i) => (
                  <button
                    key={i}
                    onClick={() => setQuery(q)}
                    className="text-xs bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>

            {error && (
              <div className="mt-4 bg-red-50 border border-red-200 p-4 rounded-lg flex gap-2">
                <AlertCircle className="text-red-600" />
                <span className="text-red-700 text-sm">{error}</span>
              </div>
            )}

            {results.length > 0 && (
              <div className="mt-6 bg-white rounded-xl shadow overflow-hidden">
                <div className="bg-indigo-600 text-white px-6 py-4 flex justify-between">
                  <div>
                    <h2 className="font-bold text-lg">
                      Recommended Assessments
                    </h2>
                    <p className="text-sm">
                      Ranked by cosine similarity score
                    </p>
                  </div>
                  <button
                    onClick={exportCSV}
                    className="bg-white text-indigo-600 px-4 py-2 rounded-lg"
                  >
                    <Download className="inline w-4 h-4 mr-1" />
                    Export CSV
                  </button>
                </div>

                <table className="w-full text-sm">
                  <thead className="bg-gray-100">
                    <tr>
                      <th className="px-4 py-3">#</th>
                      <th className="px-4 py-3 text-left">Assessment</th>
                      <th className="px-4 py-3">Type</th>
                      <th className="px-4 py-3">Duration</th>
                      <th className="px-4 py-3">Score</th>
                      <th className="px-4 py-3">Link</th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.map((r, i) => {
                      const percent = Math.min(
                        Math.max(r.score * 100, 0),
                        100
                      );
                      return (
                        <tr key={i} className="border-t">
                          <td className="px-4 py-3 font-bold">{i + 1}</td>
                          <td className="px-4 py-3">
                            <div className="font-semibold">{r.name}</div>
                            <div className="text-xs text-gray-600">
                              {r.category}
                            </div>
                          </td>
                          <td className="px-4 py-3">
                            <span
                              className={`px-3 py-1 rounded-full text-xs font-bold ${badgeColor(
                                r.type
                              )}`}
                            >
                              {r.type}
                            </span>
                          </td>
                          <td className="px-4 py-3">{r.duration}</td>
                          <td className="px-4 py-3 font-semibold">
                            {percent.toFixed(2)}%
                          </td>
                          <td className="px-4 py-3">
                            <a
                              href={r.url}
                              target="_blank"
                              rel="noreferrer"
                              className="text-indigo-600 font-medium"
                            >
                              View →
                            </a>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </>
        )}

        {/* API TAB */}
        {tab === "api" && (
          <div className="bg-white p-8 rounded-xl shadow space-y-5">
            <h2 className="text-2xl font-bold">API Documentation</h2>

            <p>
              The backend is implemented using <b>FastAPI</b> and exposes a
              semantic recommendation endpoint. It uses sentence-transformer
              embeddings and cosine similarity to compute real relevance scores.
            </p>

            <div>
              <h3 className="font-semibold mb-1">Base URL</h3>
              <code className="block bg-gray-900 text-gray-100 p-3 rounded">
                http://localhost:8000
              </code>
            </div>

            <div>
              <h3 className="font-semibold mb-1">Endpoint</h3>
              <code className="bg-blue-100 text-blue-800 px-3 py-1 rounded font-mono">
                POST /recommend
              </code>
            </div>

            <div>
              <h3 className="font-semibold mb-1">Request</h3>
              <pre className="bg-gray-900 text-gray-100 p-3 rounded text-sm">{`{
  "query": "Java developer with collaboration skills",
  "max_results": 10
}`}</pre>
            </div>

            <div>
              <h3 className="font-semibold mb-1">Response</h3>
              <pre className="bg-gray-900 text-gray-100 p-3 rounded text-sm">{`{
  "name": "Java Programming Test",
  "url": "https://www.shl.com/...",
  "test_type": ["Knowledge & Skills"],
  "duration": 60,
  "score": 0.7421
}`}</pre>
            </div>

            <p className="text-sm text-gray-600">
              <b>score</b> represents the cosine similarity between the job
              description and the assessment content.
            </p>
          </div>
        )}

        {/* ABOUT TAB */}
        {tab === "about" && (
          <div className="bg-white p-8 rounded-xl shadow">
            <p>
              This system uses real SHL assessment data, semantic embeddings
              generated using sentence-transformers, and cosine similarity for
              ranking. The entire pipeline is data-driven with no mocked
              recommendations.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
