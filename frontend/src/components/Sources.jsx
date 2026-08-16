function Sources({ sources, pdfUrl }) {
  if (!sources || sources.length === 0) {
    return null;
  }

  return (
    <section className="sources-card">
      <p className="eyebrow">SOURCES</p>

      <div className="source-list">
        {sources.map((page) => (
          <a
            key={page}
            href={`${pdfUrl}#page=${page}`}
            target="_blank"
            rel="noopener noreferrer"
            className="source-badge"
          >
            Page {page}
          </a>
        ))}
      </div>
    </section>
  );
}

export default Sources;