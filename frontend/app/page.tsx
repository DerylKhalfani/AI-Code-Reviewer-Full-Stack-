'use client'
import { useState } from 'react'
import CodeInput from '@/components/CodeInput'
import LanguageSelector from '@/components/LanguageSelector'

export default function Home() {

  // State for code input
  const [code, setCode] = useState('')

  // State for selected language
  const [language, setLanguage] = useState('python')

  // State for loading indicator
  const [loading, setLoading] = useState(false)

  // State for API results
  // any type allows any structure - TypeScript won't complain about nested properties
  const [results, setResults] = useState<any>(null)

  // State for error messages
  const [error, setError] = useState('')

  // async function allows using await inside
  const handleAnalyze = async () => {
    setError('')

    // Validate code input
    if (!code.trim()) {
      setError('Please enter some code to analyze')
      return
    }

    // Check line count limit
    const lineCount = code.split('\n').length
    if (lineCount > 2000) {
      setError(`Code has ${lineCount} lines. Maximum is 2000 lines.`)
      return
    }

    setLoading(true)
    setResults(null)

    // try/catch/finally: error handling structure
    try{
      // await: waits for promise to resolve
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        // JSON.stringify: converts JS object to JSON string
        body: JSON.stringify({ code, language}),
      })

      if (!response.ok) {
        throw new Error('Failed to analyze code')
      }

      const data = await response.json()
      setResults(data)

    } catch(err) {
      setError('Failed to analyze code. Make sure the backend is running')
    } finally {
      // finally: always runs regardless of success/error
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">

      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <h1 className="text-4xl font-bold text-gray-900">AI Code Review Agent</h1>
        <p className="text-gray-600 mt-2">Paste your code below for intelligent analysis</p>
      </div>

      {/* Two column grid: 1 column on mobile, 2 on large screens */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-6">

        {/* LEFT SIDE - Code Input */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className='text-xl font-semibold mb-4 text-gray-900'>Code Input</h2>

          {/* Language selector dropdown */}
          <LanguageSelector
            value={language}
            onChange={setLanguage}
          />

          {/* Monaco Editor component for code input */}
          <CodeInput
            value={code}
            onChange={setCode}
            language={language}
          />

          {/* && operator: renders right side only if left side is truthy */}
          {error && (
            <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
              {error}
            </div>
          )}

          {/* Button with click handler */}
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="mt-4 w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400"
          >
            {/* Ternary: condition ? ifTrue : ifFalse */}
            {loading ? 'Analyzing...' : 'Analyze Code'}
          </button>
        </div>

        {/* RIGHT SIDE - Results */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-900">Analysis Results</h2>

          {/* Conditional rendering with && */}
          {loading && <p className="text-gray-500">Analyzing your code...</p>}

          {results && (
            <div>
              {/* Optional chaining ?.: safely access nested properties */}
              {/* || operator: provides fallback value */}
              <p className="text-sm text-gray-900">
                Total issues: {results.metrics?.total_issues || 0}
              </p>

              {/* JSON.stringify(obj, null, 2): formats object as indented string */}
              <pre className="mt-4 text-xs overflow-auto max-h-96 text-gray-900 bg-gray-50 p-4 rounded">
                {JSON.stringify(results, null, 2)}
              </pre>
            </div>
          )}

          {/* ! operator: logical NOT (negates boolean) */}
          {!loading && !results && (
            <p className="text-gray-900">Results will appear here after analysis</p>
          )}

        </div>
      </div>
    </div>
  )
}