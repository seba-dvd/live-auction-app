import { NavLink, Outlet } from 'react-router-dom'

// TODO (A) S1: show the logged-in user and a logout button (auth context), hide links that need a JWT.
export default function Layout() {
  return (
    <div className="app">
      <header className="app-header">
        <NavLink to="/" end className="brand">
          Live Auction
        </NavLink>
        <nav>
          <NavLink to="/" end>
            Licitații
          </NavLink>
          <NavLink to="/auctions/new">Licitație nouă</NavLink>
          <NavLink to="/wallet">Portofel</NavLink>
          <NavLink to="/login">Autentificare</NavLink>
          <NavLink to="/register">Cont nou</NavLink>
        </nav>
      </header>
      <main className="app-main">
        <Outlet />
      </main>
    </div>
  )
}
