import Placeholder from '../components/Placeholder.tsx'

export default function CreateAuctionPage() {
  return (
    <Placeholder
      title="Licitație nouă"
      todo={[
        'Formular: titlu, descriere, preț de pornire, increment minim, început, sfârșit (validare start < end)',
        'POST /api/auctions, apoi POST /api/auctions/{id}/photos (multipart files, max 5, jpeg/png/webp, max 5 MB)',
        'Previzualizare poze înainte de încărcare',
        'Redirecționare la /auctions/{id}',
      ]}
    />
  )
}
