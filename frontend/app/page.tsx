'use client'
import { useState } from 'react'

export default function Home() {

  // State for code input
  const [code, setCode] = useState('')

  // State for selected language
  const [language, setLanguage] = useState('python')

  // State for loading indicator
  const [loading, setLoading] = useState(false)

  // State for API results
  const [results, setResults] = useState(null)

  // State for error messages
  const [error, setError] = useState('')

  // Function to call the backendAPI

  return (
    <div>
      <h1>AI Code Review Agent</h1>
      <p>Coming soon...</p>
    </div>
  )
}