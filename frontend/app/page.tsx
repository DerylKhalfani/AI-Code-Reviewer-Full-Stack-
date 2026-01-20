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

  // Function to send code to backend API for analysis
  const handleAnalyze = async () => {
    // Clear previous errors
    setError('')

    // Validate: check if code is empty
    if (!code.trim()) {
      setError('Please enter some code to analyze')
      return
    }

    // Validate: check line count, max 2000 lines
    const lineCount = code.split('\n').length
    if (lineCount > 2000) {
      setError(`Code has ${lineCount} lines. Maximum is 2000 lines.`)
      return
    }

    // Start loading
    setLoading(true)
    // Clear previous results
    setResults(null)

    try{
      // Fetch API: sends HTTP request to backend
      // await: waits for the request to complete before continuing
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST', // POST request (sending data)
        headers: {
          'Content-Type': 'application/json' // Sending json
        },
        // converting to JSON string, and send { code: "...", language: "python"}
        body: JSON.stringify({ code, language}),
      })

      if (!response.ok) {
        throw new Error('Failed to analyze code')
      }

      // Convert response from JSON string to JavaScript object
      const data = await response.json()

      // Store result in state 
      setResults(data)

    } catch(err) {
      // Runs if error occurs
      setError('Failed to analyze code. Make sure the backend is running')
    } finally {
      // Stop loading
      setLoading(false)
    }
  }

  return (
    // Main container - full screen with light gray background
    <div className="min-h-screen bg-gray-50 p-8">

      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <h1 className="text-gray-600 mt-2">AI Code Review Agent</h1>
        <p className="text-gray-600 mt-2">Paste your code below for intelligent analysis</p>
      </div>
    </div>
  )
}