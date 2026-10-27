import { Route, Routes } from 'react-router-dom'
import Layout from './components/Layout.tsx'
import AuctionDetailsPage from './pages/AuctionDetailsPage.tsx'
import CreateAuctionPage from './pages/CreateAuctionPage.tsx'
import HomePage from './pages/HomePage.tsx'
import LoginPage from './pages/LoginPage.tsx'
import NotFoundPage from './pages/NotFoundPage.tsx'
import RegisterPage from './pages/RegisterPage.tsx'
import WalletPage from './pages/WalletPage.tsx'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="login" element={<LoginPage />} />
        <Route path="register" element={<RegisterPage />} />
        <Route path="auctions/new" element={<CreateAuctionPage />} />
        <Route path="auctions/:id" element={<AuctionDetailsPage />} />
        <Route path="wallet" element={<WalletPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  )
}
