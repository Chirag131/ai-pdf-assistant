import { useEffect, useState } from "react";

import {
  checkHealth,
  uploadPdf,
  askQuestion,
} from "./services/api";

import FileUpload from "./components/FileUpload";
import ChatInput from "./components/ChatInput";
import Answer from "./components/Answer";
import Sources from "./components/Sources";

function App() {
  const [pdfUrl, setPdfUrl] = useState("");

  const [backendOnline, setBackendOnline] =
    useState(false);

  const [file, setFile] = useState(null);

  const [uploading, setUploading] =
    useState(false);

  const [uploaded, setUploaded] =
    useState(false);

  const [uploadInfo, setUploadInfo] =
    useState(null);

  const [answer, setAnswer] =
    useState("");

  const [sources, setSources] =
    useState([]);

  const [asking, setAsking] =
    useState(false);

  const [error, setError] =
    useState("");

  useEffect(() => {
    checkHealth()
      .then(() => {
        setBackendOnline(true);
      })
      .catch(() => {
        setBackendOnline(false);
      });
  }, []);

  

  function handleFileChange(selectedFile) {
    setFile(selectedFile);
    setUploaded(false);
    setUploadInfo(null);
    setAnswer("");
    setSources([]);
    setError("");
  }

  async function handleUpload() {
  if (!file) {
    return;
  }

  setUploading(true);
  setError("");
  setAnswer("");
  setSources([]);

  try {
    const data = await uploadPdf(file);

    setUploadInfo(data);
    setUploaded(true);

    setPdfUrl(
      `http://127.0.0.1:8000/uploads/${data.filename}`
    );
  } catch (error) {
    console.error("Upload error:", error);

    setError(
      error.message ||
        "Failed to upload the PDF."
    );
  } finally {
    setUploading(false);
  }
}

  async function handleAsk(question) {
    setAsking(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      const data = await askQuestion(question);

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (error) {
      console.error("Question error:", error);

      setError(
        error.message ||
          "Failed to generate an answer."
      );
    } finally {
      setAsking(false);
    }
  }

  function handleNewDocument() {
    setFile(null);
    setUploaded(false);
    setUploadInfo(null);
    setAnswer("");
    setSources([]);
    setError("");
  }

  return (
    <div className="app">
      <header className="header">
        <div className="brand">
          <div className="brand-icon">AI</div>

          <div>
            <h1>AI PDF Assistant</h1>
            <p>
              Ask questions. Get answers from your
              documents.
            </p>
          </div>
        </div>

        <div
          className={`status ${
            backendOnline
              ? "status-online"
              : "status-offline"
          }`}
        >
          <span className="status-dot" />

          {backendOnline
            ? "Backend online"
            : "Backend offline"}
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <p className="eyebrow">RAG POWERED</p>

          <h2>
            Chat with your
            <br />
            <span>PDF documents.</span>
          </h2>

          <p className="hero-description">
            Upload a document and ask questions.
            The assistant retrieves relevant
            sections before generating an answer.
          </p>
        </section>

        <div className="workspace">
          <FileUpload
            file={file}
            onFileChange={handleFileChange}
            onUpload={handleUpload}
            uploading={uploading}
            uploaded={uploaded}
            uploadInfo={uploadInfo}
          />

          <ChatInput
            onAsk={handleAsk}
            loading={asking}
            disabled={!uploaded}
          />
        </div>

        {error && (
          <div className="error-card">
            <strong>Something went wrong</strong>
            <p>{error}</p>
          </div>
        )}

        <Answer
          answer={answer}
          loading={asking}
        />

        {!asking && answer && (
          <Sources sources={sources} />
        )}

        {uploaded && (
          <div className="new-document">
            <button
              type="button"
              className="text-button"
              onClick={handleNewDocument}
            >
              Upload another document
            </button>
          </div>
        )}
      </main>

      <footer>
        <p>
          AI PDF Assistant · Built with React,
          FastAPI & Gemini
        </p>
      </footer>
    </div>
  );
}

export default App;