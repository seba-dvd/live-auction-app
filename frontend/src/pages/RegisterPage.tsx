import Placeholder from '../components/Placeholder.tsx'

export default function RegisterPage() {
  return (
    <Placeholder
      title="Cont nou"
      todo={[
        'Formular username, email, parolă, nume afișat: POST /api/auth/register',
        'Validare în client: username ^[a-zA-Z0-9_.-]{3,30}$, email, parolă minim 8 caractere',
        'Erori de validare per câmp din ProblemDetail',
        'Mesaj: ai primit 1000 de monede bonus, apoi redirecționare la login',
      ]}
    />
  )
}
