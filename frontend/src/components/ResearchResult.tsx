import React from 'react';

interface Step {
  type: string;
  content: string;
}

interface ResearchResultProps {
  final_answer: string;
  steps: Step[];
}

const ResearchResult: React.FC<ResearchResultProps> = ({ final_answer, steps }) => (
  <div style={{ marginTop: 32 }}>
    <h2>Research</h2>
    <div style={{ background: "#f5f5f5", borderRadius: 8, padding: 16 }}>
      {steps && steps.length > 0 && (
        <ol>
          {steps.map((step, idx) => (
            <li key={idx} style={{ marginBottom: 8 }}>
              <strong>{step.type}:</strong> {step.content}
            </li>
          ))}
        </ol>
      )}
      <div style={{ marginTop: 24, background: "#e0e7ef", borderRadius: 8, padding: 16 }}>
        <strong>Final Answer:</strong>
        <div>{final_answer}</div>
      </div>
    </div>
  </div>
);

export default ResearchResult;