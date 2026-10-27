import { Link } from 'react-router-dom'

export default function NotFoundPage() {
  return (
    <section className="placeholder">
      <h1>Pagina nu există</h1>
      <p>
        <Link to="/">Înapoi la licitații</Link>
      </p>
    </section>
  )
}
