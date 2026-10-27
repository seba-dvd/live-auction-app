import Placeholder from '../components/Placeholder.tsx'

export default function HomePage() {
  return (
    <Placeholder
      title="Licitații"
      todo={[
        'Tab-uri SCHEDULED / ACTIVE / ENDED: GET /api/auctions?status=ACTIVE&page=0&size=12&sort=endTime,asc',
        'Card AuctionSummary: poză principală, titlu, preț curent, număr de oferte, timp rămas',
        'Paginare din răspunsul PagedModel (page.number, page.totalPages)',
        'Stări de încărcare, listă goală și eroare',
      ]}
    />
  )
}
