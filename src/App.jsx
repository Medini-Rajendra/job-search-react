import { useState } from 'react'
import './App.css'
import './index.css'
import Search from './components'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1 className='text-2xl font-semibold'>Job Application Portal</h1>
      <Search />
    </>
  )
}

export default App
