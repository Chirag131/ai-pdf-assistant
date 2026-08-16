import { useState } from "react";

function ChatInput({
  onAsk,
  loading,
  disabled,
}) {
  const [question, setQuestion] = useState("");

  function handleSubmit(event) {
    event.preventDefault();

    const cleanedQuestion = question.trim();

    if (!cleanedQuestion || disabled || loading) {
      return;
    }

    onAsk(cleanedQuestion);

    setQuestion("");
  }

  return (
    <section className="question-card">
      <p className="eyebrow">ASK YOUR DOCUMENT</p>

      <h2>What would you like to know?</h2>

      <form
        className="question-form"
        onSubmit={handleSubmit}
      >
        <textarea
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          placeholder={
            disabled
              ? "Upload a PDF first..."
              : "Ask a question about your PDF..."
          }
          disabled={disabled || loading}
          rows={4}
        />

        <button
          type="submit"
          className="primary-button"
          disabled={
            disabled ||
            loading ||
            !question.trim()
          }
        >
          {loading ? "Thinking..." : "Ask Question"}
        </button>
      </form>
    </section>
  );
}

export default ChatInput;