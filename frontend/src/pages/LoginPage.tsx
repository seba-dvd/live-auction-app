import Placeholder from '../components/Placeholder.tsx'

export default function LoginPage() {
  return (
    <Placeholder
      title="Autentificare"
      todo={[
        'Formular usernameOrEmail + parolă: POST /api/auth/login',
        'Salvează accessToken și user în AuthContext (și în sessionStorage)',
        'Mesaj de eroare din ProblemDetail (câmpul code)',
        'Redirecționare înapoi la pagina cerută după login',
      ]}
    />
  )
}
