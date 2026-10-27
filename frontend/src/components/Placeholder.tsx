type PlaceholderProps = {
  title: string
  todo: string[]
}

/** Temporary page body used by the skeleton: lists what A has to build (see docs/team/A.md). */
export default function Placeholder({ title, todo }: PlaceholderProps) {
  return (
    <section className="placeholder">
      <h1>{title}</h1>
      <p className="todo-badge">TODO (A)</p>
      <ul>
        {todo.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  )
}
