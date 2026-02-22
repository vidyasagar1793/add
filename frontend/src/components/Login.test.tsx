/// <reference types="vitest" />
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import Login from './Login';
import { MemoryRouter } from 'react-router-dom';
import axios from 'axios';
import * as useAuthHook from '../hooks/useAuth';

// Mock axios
vi.mock('axios');

// Mock useAuth
const mockLogin = vi.fn();
vi.mock('../hooks/useAuth', () => ({
    useAuth: () => ({
        login: mockLogin
    })
}));

// Mock useNavigate
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual('react-router-dom');
    return {
        ...actual,
        useNavigate: () => mockNavigate,
    };
});

describe('Login Component', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('renders correctly', () => {
        render(
            <MemoryRouter>
                <Login />
            </MemoryRouter>
        );

        expect(screen.getByLabelText(/email address/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
    });

    it('updates input values', () => {
        render(
            <MemoryRouter>
                <Login />
            </MemoryRouter>
        );

        const emailInput = screen.getByLabelText(/email address/i) as HTMLInputElement;
        const passwordInput = screen.getByLabelText(/password/i) as HTMLInputElement;

        fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
        fireEvent.change(passwordInput, { target: { value: 'password123' } });

        expect(emailInput.value).toBe('test@example.com');
        expect(passwordInput.value).toBe('password123');
    });

    it('handles successful login', async () => {
        const mockToken = 'mock-jwt-token';
        (axios.post as any).mockResolvedValueOnce({ data: { access_token: mockToken } });

        render(
            <MemoryRouter>
                <Login />
            </MemoryRouter>
        );

        fireEvent.change(screen.getByLabelText(/email address/i), { target: { value: 'test@example.com' } });
        fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
        fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

        await waitFor(() => {
            expect(axios.post).toHaveBeenCalledWith(
                'http://localhost:8000/api/v1/auth/login',
                expect.any(FormData),
                expect.objectContaining({
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
                })
            );
            expect(mockLogin).toHaveBeenCalledWith(mockToken);
            expect(mockNavigate).toHaveBeenCalledWith('/');
        });
    });

    it('handles failed login', async () => {
        (axios.post as any).mockRejectedValueOnce(new Error('Invalid credentials'));

        render(
            <MemoryRouter>
                <Login />
            </MemoryRouter>
        );

        fireEvent.change(screen.getByLabelText(/email address/i), { target: { value: 'wrong@example.com' } });
        fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'wrongpass' } });
        fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

        await waitFor(() => {
            expect(screen.getByText('Invalid email or password')).toBeInTheDocument();
            expect(mockLogin).not.toHaveBeenCalled();
            expect(mockNavigate).not.toHaveBeenCalled();
        });
    });
});
