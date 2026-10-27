import Placeholder from '../components/Placeholder.tsx'

export default function WalletPage() {
  return (
    <Placeholder
      title="Portofel"
      todo={[
        'Sold: GET /api/wallet (balance, reserved, available)',
        'Istoric: GET /api/wallet/transactions?page=0&size=20',
        'Alimentare demo: POST /api/wallet/top-up (1–10000 monede)',
      ]}
    />
  )
}
