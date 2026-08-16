import ReactMarkdown from "react-markdown";

function Answer({ answer, loading }) {
  if (loading) {
    return (
      <section className="answer-card">
        <div className="loading">
          <div className="spinner" />
          <p>Searching your document...</p>
        </div>
      </section>
    );
  }

  if (!answer) {
    return null;
  }

  return (
    <section className="answer-card">
      <div className="answer-header">
        <p className="eyebrow">ANSWER</p>
      </div>

      <div className="answer-content">
        <ReactMarkdown>
          {answer}
        </ReactMarkdown>
      </div>
    </section>
  );
}

export default Answer;