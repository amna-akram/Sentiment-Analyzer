import { useState } from "react";
import "./SentimentAnalyzer.scss";

export default function SentimentAnalyzer() {
    const [text, setText] = useState("");
    const [model, setModel] = useState("custom");
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleAnalyze = async () => {
        setError(null);
        setResult(null);
        setLoading(true);

        try {
            const response = await fetch("http://localhost:3000/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text, model }),
            });

            const data = await response.json();
            if (response.ok) {
                setResult(data);
            } else {
                setError(data.error || "An error occurred");
            }
        } catch (err) {
            setError("Failed to connect to the server.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="sentiment-analyzer">
            <h1>Sentiment Analyzer</h1>
            <textarea
                placeholder="Enter text here..."
                value={text}
                onChange={(e) => setText(e.target.value)}
            ></textarea>

            <div className="controls">
                <label>Choose Model</label>
                <select value={model} onChange={(e) => setModel(e.target.value)}>
                    <option value="custom">Custom Model</option>
                    <option value="llama">Llama 3</option>
                </select>
            </div>

            <button onClick={handleAnalyze} disabled={loading}>
                {loading ? "Analyzing..." : "Analyze Sentiment"}
            </button>

            {error && <p className="error">{error}</p>}

            {result && (
                <div className="result">
                    <h2>Sentiment Analysis Result</h2>
                    <p><strong>Sentiment:</strong> {result.sentiment}</p>
                    <p><strong>Confidence:</strong> {result.confidence}</p>
                </div>
            )}
        </div>
    );
}
