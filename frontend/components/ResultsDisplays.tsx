'use client'

import React from 'react'

// Props interface
interface ResultsDisplayProps {
    results: any // Analysis results from API
    loading: boolean // Whether analysis is in progress
}

export default function ResultsDisplay({ results, loading}: ResultsDisplayProps) {

    // Show loading state
    if (loading) {
        return (
            <div className='flex items-center justify-center h-64'>
                <div className='="text-center'>
                    <div className='animate-spin roudned-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4'></div>
                    <p className='text-gray-700'>Analyzing your code...</p>
                    <p className='text-sm text-gray-700 mt-2'>This may take 30-60 seconds, depending on the amount of the code</p>
                </div>
            </div>
        )
    }

    // Show empty state
    if (!results) {
        return (
            <div className='flex items-center justify-center h-64'>
                <p className='text-gray-700'>Results will appear here after analysis</p>
            </div>
        )
    }

    // Show results ()
    if (results) {
        return (
            <div className='space-y-6'>
                {/* 1. METRICS CARDS */}
                <h3 className='text-lg font-semibold text-gray-900 mb-3'>Metrics Overview</h3>

                {/* Grid of 5 cards */}
                <div className='bg-blue-50 border border-blue-200 rounded-lg p-4 text-center'>
                    <p className='text-2xl font-bold text-blue-200'>5</p>
                    <p className='text-sm text-blue-600'>Total Issues</p>
                </div>

                {/* Critical Card */}
                <div className='bg-red-50 border border-red-200 rounded-lg p-4 text-center'>
                    <p className='text-2xl font-bold text-red-700'>2</p>
                    <p className='text-sm text-red-600'>Critical</p>
                </div>

                {/* High Card */}
                <div className='bg-red-50 border border-red-200 rounded-lg p-4 text-center'>
                    <p className='text-2xl font-bold text-red-700'>2</p>
                    <p className='text-sm text-orange-600'>High</p>
                </div>

                {/* Medium Card */}
                <div className='bg-red-50 border border-red-200 rounded-lg p-4 text-center'>
                    <p className='text-2xl font-bold text-red-700'>2</p>
                    <p className='text-sm text-yellow-600'>Medium</p>
                </div>

                {/* Low Card */}
                <div className='bg-red-50 border border-red-200 rounded-lg p-4 text-center'>
                    <p className='text-2xl font-bold text-red-700'>2</p>
                    <p className='text-sm text-green-600'>Low</p>
                </div>
            </div>

            {/* SUMMARY SECTION */}
            <div>
                <h3 className='text-lg font-semibold text-gray-900 mb-3'>Summary</h3>
                <div className='bg-blue-50 border border-blue-200 rounded-lg p-4'>
                    <p className='text-gray-800'>
                        Code has blablabla
                    </p>
                </div>
            </div>

            {/* ISSUES LIST */}
            <div>
                <h3 className='text=lg font-semibold text-gray-900 mb-3'>
                    Issues Found
                </h3>

                <div className='space-y-3'>

                    {/* Issue Card */}
                    <div className='border border-gray-200 rounded-lh p-4'>

                        {/* Issue Header */}
                        <div className='flex items-start justify-between mb-2'>
                            <div className='flex items-center gap-2'>
                                {/* Severity Badge */}
                                <span className="px-2 py-1 text-xs font-semibold rounded bg-red-100 text-red-700">
                                    CRITICAL
                                </span>

                                {/* Issue Type */}
                                <span className='text-sm text-gray-400'>security</span>
                            </div>

                            {/* Line Number */}
                            <span className="text-sm text-gray-400">Line 2</span>
                        </div>

                        {/* Issue Message */}
                        <p className='text-gray-900 font-medium mb-2'>
                            Hardcoded password detected
                        </p>

                        {/* Suggestion */}
                        <div className='bg-gray-50 rounded p-2 mt-2'>
                            <p className='text-sm text-gray-700'>
                                <span className='font-semibold'>Suggestion:</span> Use environment variables instead
                            </p>
                        </div>
                    </div>
                </div>

            </div>
        )
    }
}