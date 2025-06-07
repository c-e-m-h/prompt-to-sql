import React, { useState } from 'react';

// Add a type for the result
type QueryResult = {
  query: string;
  result: { table: any[]; chart: any[] };
  timestamp: Date;
};

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [history, setHistory] = useState<QueryResult[]>([]); // Array of results
  const [currentPage, setCurrentPage] = useState(0); // 0 = most recent
  const [loading, setLoading] = useState(false);
  const [showMaxNotification, setShowMaxNotification] = useState(false);
  const maxHistory = 10;
  const maxVisiblePages = 5;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    // Show notification if about to hit or exceed max
    if (history.length >= maxHistory - 1) {
      setShowMaxNotification(true);
    }
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      const newEntry: QueryResult = {
        query: prompt,
        result: data,
        timestamp: new Date(),
      };
      let newHistory = [newEntry, ...history];
      if (newHistory.length > maxHistory) newHistory = newHistory.slice(0, maxHistory);
      setHistory(newHistory);
      setCurrentPage(0);
    } catch (err) {
      // Optionally show error to user
    }
    setLoading(false);
  };

  // Pagination logic
  const totalPages = history.length;
  let startPage = 0;
  let endPage = totalPages;
  if (totalPages > maxVisiblePages) {
    if (currentPage < Math.floor(maxVisiblePages / 2)) {
      startPage = 0;
      endPage = maxVisiblePages;
    } else if (currentPage > totalPages - Math.ceil(maxVisiblePages / 2)) {
      startPage = totalPages - maxVisiblePages;
      endPage = totalPages;
    } else {
      startPage = currentPage - Math.floor(maxVisiblePages / 2);
      endPage = startPage + maxVisiblePages;
    }
  }
  const visiblePages = Array.from({ length: endPage - startPage }, (_, i) => startPage + i);

  // Clear current result
  const handleClearCurrent = () => {
    if (history.length === 0) return;
    let newHistory = [...history];
    newHistory.splice(currentPage, 1);
    let newPage = currentPage;
    if (newPage >= newHistory.length) newPage = newHistory.length - 1;
    if (newPage < 0) newPage = 0;
    setHistory(newHistory);
    setCurrentPage(newPage);
  };

  // Clear all results with confirmation
  const handleClearAll = () => {
    if (window.confirm('Are you sure you want to clear all of your query results?')) {
      setHistory([]);
      setCurrentPage(0);
    }
  };

  // Format timestamp
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };
  const formatFull = (date: Date) => {
    return date.toLocaleString();
  };

  const selected = history[currentPage];

  return (
    <main className="min-h-screen grid place-content-center bg-[var(--black)] text-[var(--text)] text-center" style={{ fontFamily: 'Isra, Arial, sans-serif' }}>
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
          style={{ fontFamily: 'Isra, Arial, sans-serif', textAlign: 'center', margin: '0 auto', display: 'block', marginTop: 24 }}
        >
          Run
        </button>
      </form>
      {loading && (
        <div className="loader-wrapper text-center">
          <span className="loader border-[var(--purple)]"></span>
        </div>
      )}
      {/* Results Table */}
      {selected && (
        <div className="mt-8 bg-[var(--panel)] border border-[var(--border)] rounded-xl shadow-lg p-6 flex flex-col items-center text-center w-full">
          <h3 className="font-semibold mb-4 text-center w-full" style={{ color: 'var(--purple-accent)', textAlign: 'center' }}>Results</h3>
          {selected.result.table.length === 0 ? (
            <div style={{marginTop: 24, color: 'var(--text-muted)', fontWeight: 'bold', textAlign: 'center'}}>Please clarify your question.</div>
          ) : (
            <div className="overflow-x-auto w-full text-center">
              <table className="mx-auto border-collapse text-[var(--text)] text-center w-full" style={{ textAlign: 'center', margin: '0 auto' }}>
                <thead className="text-center w-full">
                  <tr className="text-center w-full">
                    {Object.keys(selected.result.table[0]).map((col) => (
                      <th key={col} className="border-b border-[var(--border)] px-4 py-2 text-center bg-[var(--panel)] w-full" style={{ color: 'var(--purple)', textAlign: 'center' }}>{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="text-center w-full">
                  {selected.result.table.map((row, index) => (
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
      {/* Pagination Bar */}
      {history.length > 0 && (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: 24, gap: 24 }}>
          <button
            onClick={handleClearCurrent}
            style={{ background: 'none', border: 'none', color: 'var(--purple-accent)', fontWeight: 'bold', cursor: 'pointer' }}
            disabled={history.length === 0}
          >
            Clear result
          </button>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <button
              onClick={() => setCurrentPage(Math.max(currentPage - 1, 0))}
              disabled={currentPage === 0}
              style={{ background: 'none', border: 'none', color: 'var(--purple)', fontWeight: 'bold', fontSize: 18, cursor: currentPage === 0 ? 'default' : 'pointer' }}
            >
              {'<'}
            </button>
            {visiblePages.map((page) => (
              <button
                key={page}
                onClick={() => setCurrentPage(page)}
                style={{
                  background: page === currentPage ? 'var(--purple-accent)' : 'none',
                  color: page === currentPage ? 'var(--text)' : 'var(--purple)',
                  border: 'none',
                  borderRadius: 4,
                  fontWeight: 'bold',
                  fontSize: 16,
                  padding: '4px 12px',
                  cursor: 'pointer',
                  margin: '0 2px',
                }}
              >
                {page + 1}
              </button>
            ))}
            <button
              onClick={() => setCurrentPage(Math.min(currentPage + 1, history.length - 1))}
              disabled={currentPage === history.length - 1}
              style={{ background: 'none', border: 'none', color: 'var(--purple)', fontWeight: 'bold', fontSize: 18, cursor: currentPage === history.length - 1 ? 'default' : 'pointer' }}
            >
              {'>'}
            </button>
          </div>
          <button
            onClick={handleClearAll}
            style={{ background: 'none', border: 'none', color: 'var(--purple-accent)', fontWeight: 'bold', cursor: 'pointer' }}
            disabled={history.length === 0}
          >
            Clear all results
          </button>
        </div>
      )}
      {/* Query and Timestamp */}
      {selected && (
        <div style={{ marginTop: 16, textAlign: 'center', color: 'var(--text-muted)', fontWeight: 'bold' }}>
          <div>Query: <span style={{ color: 'var(--purple)' }}>{selected.query}</span></div>
          <div>
            Time: <span title={formatFull(selected.timestamp)}>{formatTime(selected.timestamp)}</span>
          </div>
        </div>
      )}
      {/* Max Results Notification */}
      {showMaxNotification && (
        <div style={{ position: 'fixed', top: 32, left: 0, right: 0, margin: '0 auto', zIndex: 1000, display: 'flex', justifyContent: 'center' }}>
          <div style={{ background: 'var(--panel)', color: 'var(--purple-accent)', border: '2px solid var(--purple)', borderRadius: 8, padding: '16px 32px', fontWeight: 'bold', boxShadow: '0 2px 8px rgba(0,0,0,0.2)', textAlign: 'center' }}>
            Max saved results reached (10). Clear previous results, or your oldest result will be cleared for storage.
            <button onClick={() => setShowMaxNotification(false)} style={{ marginLeft: 24, background: 'none', border: 'none', color: 'var(--purple)', fontWeight: 'bold', cursor: 'pointer', fontSize: 16 }}>Dismiss</button>
          </div>
        </div>
      )}
    </main>
  );
} 