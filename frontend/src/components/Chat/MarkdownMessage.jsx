import ReactMarkdown from 'react-markdown'
import './MarkdownMessage.css'

const MarkdownMessage = ({ content }) => {
  return (
    <div className="markdown-message">
      <ReactMarkdown
        components={{
          p: ({ children }) => <p className="md-paragraph">{children}</p>,
          strong: ({ children }) => <strong className="md-bold">{children}</strong>,
          em: ({ children }) => <em className="md-italic">{children}</em>,
          ul: ({ children }) => <ul className="md-list">{children}</ul>,
          ol: ({ children }) => <ol className="md-list md-list-ordered">{children}</ol>,
          li: ({ children }) => <li className="md-list-item">{children}</li>,
          h1: ({ children }) => <h3 className="md-heading">{children}</h3>,
          h2: ({ children }) => <h3 className="md-heading">{children}</h3>,
          h3: ({ children }) => <h4 className="md-heading">{children}</h4>,
          a: ({ href, children }) => (
            <a href={href} target="_blank" rel="noopener noreferrer" className="md-link">
              {children}
            </a>
          ),
          code: ({ inline, children }) =>
            inline ? (
              <code className="md-code-inline">{children}</code>
            ) : (
              <pre className="md-code-block"><code>{children}</code></pre>
            ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}

export default MarkdownMessage
