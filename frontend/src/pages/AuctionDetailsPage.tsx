import { useParams } from 'react-router-dom'
import Placeholder from '../components/Placeholder.tsx'

export default function AuctionDetailsPage() {
  const { id } = useParams()
  return (
    <Placeholder
      title={`Licitație #${id}`}
      todo={[
        'Detalii: GET /api/auctions/{id} (poze, descriere, preț curent, increment, serverTime)',
        'Istoric oferte: GET /api/bids/auction/{id}?page=0&size=20 (cele mai noi primele)',
        'Live: STOMP /ws, abonare la /topic/auctions/{id} (BID_PLACED, AUCTION_STARTED, AUCTION_ENDED)',
        'Cronometru calculat din endTime + offset față de serverTime (nu din ceasul clientului)',
        'Formular ofertă: POST /api/bids cu suma minimă sugerată; mesaje per code (BID_TOO_LOW, OWN_AUCTION, AUCTION_NOT_ACTIVE, INSUFFICIENT_FUNDS)',
      ]}
    />
  )
}
