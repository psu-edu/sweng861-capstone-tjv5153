import Login from '../Login.jsx';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { expect, test, beforeEach, afterEach, vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';

const originalLocation = window.location;

beforeEach(() => {
    Object.defineProperty(window, 'location', {
        configurable: true,
        value: { href: '' }
    });
    sessionStorage.clear();
});

afterEach(() => {
    Object.defineProperty(window, 'location', {
        configurable: true,
        value: originalLocation
    });
    vi.restoreAllMocks();
    sessionStorage.clear();
});

test('renders prompt text and login button', () => {
    render(
        <MemoryRouter>
            <Login />
        </MemoryRouter>
    );
    expect(screen.getByRole('button', { name: /Login with Okta/i })).toBeTruthy();
});

test('clicking login calls backend and redirects on success', async () => {
    const mockResponse = { redirect_uri: 'http://example.com' };
    global.fetch = vi.fn(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(mockResponse)
        })
    );
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {});
    render(
        <MemoryRouter>
            <Login />
        </MemoryRouter>
    );
    fireEvent.click(screen.getByRole('button', { name: /Login with Okta/i }));
    await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/signin', { method: 'GET' });
        expect(window.location.href).toBe(mockResponse.redirect_uri);
    });
    expect(alertSpy).toHaveBeenCalledWith('Redirecting to Okta login...');
});

test('shows alert on fetch failure', async () => {
    global.fetch = vi.fn(() => Promise.reject(new Error('network')));
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {});
    render(
        <MemoryRouter>
            <Login />
        </MemoryRouter>
    );
    fireEvent.click(screen.getByRole('button', { name: /Login with Okta/i }));
    await waitFor(() => {
        expect(alertSpy).toHaveBeenCalledWith('Login failed. Please try again.');
    });
    expect(alertSpy).toHaveBeenCalledWith('Redirecting to Okta login...');
});