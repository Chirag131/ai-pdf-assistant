import { useRef } from "react";

function FileUpload({
  file,
  onFileChange,
  onUpload,
  uploading,
  uploaded,
  uploadInfo,
}) {
  const inputRef = useRef(null);

  function handleFileChange(event) {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) {
      return;
    }

    if (selectedFile.type !== "application/pdf") {
      alert("Please select a PDF file.");
      return;
    }

    onFileChange(selectedFile);
  }

  function handleChooseFile() {
    inputRef.current?.click();
  }

  return (
    <section className="upload-card">
      <div className="section-header">
        <div>
          <p className="eyebrow">DOCUMENT</p>
          <h2>Upload a PDF</h2>
        </div>
      </div>

      <div className="drop-zone">
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,application/pdf"
          onChange={handleFileChange}
          hidden
        />

        <div className="upload-icon">↑</div>

        {file ? (
          <>
            <h3>{file.name}</h3>
            <p>
              {(file.size / 1024 / 1024).toFixed(2)} MB
            </p>
          </>
        ) : (
          <>
            <h3>Select your PDF</h3>
            <p>Only PDF files are supported.</p>
          </>
        )}

        <button
          type="button"
          className="secondary-button"
          onClick={handleChooseFile}
        >
          Choose PDF
        </button>
      </div>

      {file && !uploaded && (
        <button
          type="button"
          className="primary-button full-width"
          onClick={onUpload}
          disabled={uploading}
        >
          {uploading
            ? "Indexing PDF..."
            : "Upload & Index PDF"}
        </button>
      )}

      {uploaded && uploadInfo && (
        <div className="upload-success">
          <strong>PDF indexed successfully ✓</strong>

          <div className="upload-stats">
            <span>
              {uploadInfo.pages_extracted} pages
            </span>

            <span>
              {uploadInfo.chunks_created} chunks
            </span>
          </div>
        </div>
      )}
    </section>
  );
}

export default FileUpload;