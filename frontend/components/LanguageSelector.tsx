'use client'

import React from 'react'

// Props interface
interface LanguageSelectorProps {
    value: string // Currently selected language
    onChange: (language:string) => void // Function called when selection changes
}

export default function LanguageSelector({value, onChange }: LanguageSelectorProps) {

    // Array of supported languages
    const languages = [
        { value: 'python', label: 'Python' },                                                                          
      { value: 'javascript', label: 'JavaScript' },                                                                  
      { value: 'typescript', label: 'TypeScript' },                                                                  
      { value: 'java', label: 'Java' },                                                                              
      { value: 'go', label: 'Go' },                                                                                  
      { value: 'rust', label: 'Rust' },                                                                              
      { value: 'cpp', label: 'C++' },                                                                                
      { value: 'csharp', label: 'C#' },                                                                              
    ]

    return (
        <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
                Programming Language
            </label>

            {/* select: HTML dropdown element */}
            {/* e.traget.value: gets selected option's value */}
            <select 
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
                {/* map() : loops through languages array and creates option for each*/}
                {languages.map((lang) => (
                    <option key={lang.value} value={lang.value}>
                        {lang.label}
                    </option>
                ))}
            </select>
        </div>
    )
}