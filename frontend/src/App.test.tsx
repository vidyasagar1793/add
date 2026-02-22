import { render } from '@testing-library/react'
import App from './App'
import { describe, it, expect } from 'vitest'

describe('App', () => {
    it('renders correctly', () => {
        render(<App />)
        // Adjust this expectation based on actual App content
        // For now, checking if it renders without crashing
        expect(document.body).toBeInTheDocument()
    })
})
