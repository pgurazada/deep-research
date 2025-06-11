import React from 'react';

interface ResearchHistoryProps {
  history: any[]; // You can replace `any[]` with a more specific type if you have one
}

const ResearchHistory: React.FC<ResearchHistoryProps> = ({ history }) => {
  return (
    <div>
      {/* Render your history here */}
      {history.length === 0 ? (
        <p>No history yet.</p>
      ) : (
        <ul>
          {history.map((item, idx) => (
            <li key={idx}>{JSON.stringify(item)}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ResearchHistory;