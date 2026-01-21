// What this does:                                      
//   - 'use client' - Makes it a client component         
//   (required for Monaco)                                
//   - dynamic() - Next.js function to load component only
//    on client side                                      
//   - ssr: false - Disables server-side rendering for    
//   Monaco                                               
//   - interface - TypeScript type definition for props   
//   - Props destructuring in function parameters 

'use client'

// React import
import React from 'react'

// Dynamic import for Monaco Editor (avoids SSR issues in Next.js)                                   
// dynamic: Next.js utility for client-side only imports
// ssr: false means don't render on server
import dynamic from 'next/dynamic'

// Import Monaco Editor component (client-side only)
const Editor = dynamic(() =>
import('@monaco-editor/react'), {
    ssr:false
})

// Props interface: defines what props this component accepts
interface CodeInputProps {
    value: string // Current code content
    onChange: (value: string) => void // Function called when code changes
    language: string // Programming language for syntax highlighting
}

export default function CodeInput({ value, onChange, language }: CodeInputProps) {

    // Function that takes one parameter and call onChange function with the value (string or undefined)
    // newValue can be string or undefined, default to empty string
    const handleEditorChange = (newValue: string | undefined) => {
        onChange(newValue || '') 
    }

    return (
        <div className="border rounded-lg overflow-hidden">
            <Editor 
                height="400px"
                language={language} // Sets syntax highlighting based on prop
                value={value} // COntrolled components
                onChange={handleEditorChange} // Caleed when user types
                theme="vs-dark"
                options={{ // COnfiguration objects
                    minimap: { enabled: false },        // Disable minimap (small code preview)                              
                    fontSize: 14,                       // Font size                                                         
                    lineNumbers: 'on',                  // Show line numbers                                                 
                    scrollBeyondLastLine: false,        // Don't scroll past last line                                       
                    automaticLayout: true,              // Auto-resize editor                                                
                    tabSize: 2,                         // Tab = 2 spaces                                                    
                    wordWrap: 'on',                     // Wrap long lines
                }}
            />
        </div>
    )
}