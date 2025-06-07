import React, { useState } from 'react';

// Add a type for the result
type QueryResult = {
  table: any[];
  chart: any[];
};

export default function Home() {
  // Update result state to use QueryResult | null
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState<QueryResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ table: [], chart: [] });
      // Optionally show error to user
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen grid place-content-center bg-[var(--black)] text-[var(--text)] text-center" style={{ fontFamily: 'Isra, Arial, sans-serif' }}>
      <div className="flex flex-col items-center text-center w-full">
        <h1 className="text-4xl font-bold mb-8 headline text-center w-full" style={{ color: 'var(--purple)', fontFamily: 'Simplified Arabic, Arial, sans-serif', fontWeight: 'bold', textAlign: 'center' }}>
          Prompt-to-SQL Tool
        </h1>
        <form
          className="flex flex-col items-center text-center w-full"
          onSubmit={handleSubmit}
          style={{ fontFamily: 'Isra, Arial, sans-serif', width: '100%' }}
        >
          <input
            className="min-h-[64px] px-8 py-5 mb-4 rounded-md border border-[var(--border)] focus:outline-none focus:ring-2 focus:ring-[var(--purple)] text-center text-lg placeholder-[var(--text-muted)] bg-[var(--text)] text-[var(--black)] w-full"
            type="text"
            placeholder="Ask a question about your dataset..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            style={{ fontFamily: 'Isra, Arial, sans-serif', width: 400, textAlign: 'center', margin: '0 auto', display: 'block' }}
          />
          <button
            className="py-3 px-8 rounded-md bg-[var(--purple)] hover:bg-[var(--purple-accent)] transition-colors text-[var(--text)] font-semibold shadow text-lg mt-2 text-center"
            type="submit"
            disabled={loading}
            style={{ fontFamily: 'Isra, Arial, sans-serif', textAlign: 'center', margin: '0 auto', display: 'block' }}
          >
            Run
          </button>
        </form>
        {loading && (
          <div className="loader-wrapper text-center">
            <span className="loader border-[var(--purple)]"></span>
          </div>
        )}
        {result && Array.isArray(result.table) && (
          <div className="mt-8 bg-[var(--panel)] border border-[var(--border)] rounded-xl shadow-lg p-6 flex flex-col items-center text-center w-full">
            <h3 className="font-semibold mb-4 text-center w-full" style={{ color: 'var(--purple-accent)', textAlign: 'center' }}>Results</h3>
            {result.table.length === 0 ? (
              <div style={{marginTop: 24, color: 'var(--text-muted)', fontWeight: 'bold', textAlign: 'center'}}>Please clarify your question.</div>
            ) : (
              <div className="overflow-x-auto w-full text-center">
                <table className="mx-auto border-collapse text-[var(--text)] text-center w-full" style={{ textAlign: 'center', margin: '0 auto' }}>
                  <thead className="text-center w-full">
                    <tr className="text-center w-full">
                      {Object.keys(result.table[0]).map((col) => (
                        <th key={col} className="border-b border-[var(--border)] px-4 py-2 text-center bg-[var(--panel)] w-full" style={{ color: 'var(--purple)', textAlign: 'center' }}>{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="text-center w-full">
                    {result.table.map((row, index) => (
                      <tr key={index} className={index % 2 ? 'bg-[var(--black)] text-center w-full' : 'text-center w-full'}>
                        {Object.values(row).map((val, i) => (
                          <td key={i} className="border-b border-[var(--border)] px-4 py-2 text-center w-full" style={{ textAlign: 'center' }}>{String(val)}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
} 