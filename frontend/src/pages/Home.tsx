import React, { useState } from 'react';
import ResearchInput from '../components/ResearchInput';
import ResearchResult from '../components/ResearchResult';
import axios from 'axios';

const lightTheme = {
  background: "#ededed",
  card: "#fff",
  text: "#222",
  inputBorder: "#2563eb",
  button: "#1e3a8a",
  buttonText: "#fff"
};

const darkTheme = {
  background: "#18181b",
  card: "#232329",
  text: "#fff",
  inputBorder: "#2563eb",
  button: "#2563eb",
  buttonText: "#fff"
};

const Home: React.FC = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState<{ final_answer: string; steps: any[] }>({ final_answer: '', steps: [] });
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(true);

  const theme = darkMode ? darkTheme : lightTheme;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResult({ final_answer: '', steps: [] });
    try {
      const response = await axios.post('http://localhost:8000/answer', { text: query });
      setResult(response.data.data);
    } catch (err) {
      setResult({ final_answer: 'Error fetching answer.', steps: [] });
    }
    setLoading(false);
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: theme.background,
      color: theme.text,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center"
    }}>
      <button
        onClick={() => setDarkMode(dm => !dm)}
        style={{
          position: "absolute",
          top: 24,
          right: 24,
          background: theme.button,
          color: theme.buttonText,
          border: "none",
          borderRadius: 6,
          padding: "8px 16px",
          fontWeight: 600,
          cursor: "pointer"
        }}
      >
        {darkMode ? "☀️ Light Mode" : "🌙 Dark Mode"}
      </button>
      <form
        onSubmit={handleSubmit}
        style={{
          width: 600,
          background: theme.card,
          borderRadius: 12,
          padding: 32,
          boxShadow: "0 2px 12px #0001",
          display: "flex",
          flexDirection: "column",
          alignItems: "center"
        }}
      >
        <h1 style={{ marginBottom: 24, color: theme.text }}>Deep Research</h1>
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Ask a research question..."
          style={{
            width: "100%",
            padding: 12,
            fontSize: 18,
            borderRadius: 6,
            border: `2px solid ${theme.inputBorder}`,
            marginBottom: 16,
            background: darkMode ? "#232329" : "#fff",
            color: theme.text
          }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{
            background: theme.button,
            color: theme.buttonText,
            border: "none",
            borderRadius: 6,
            padding: "10px 24px",
            fontSize: 16,
            fontWeight: 600,
            cursor: loading ? "not-allowed" : "pointer",
            marginBottom: 16
          }}
        >
          {loading ? "Thinking..." : "Submit"}
        </button>
      </form>
      <div style={{ width: 600 }}>
        <ResearchResult final_answer={result.final_answer} steps={result.steps} />
      </div>
    </div>
  );
};

export default Home;