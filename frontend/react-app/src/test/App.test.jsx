import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../App';

vi.mock('../MenuBar', () => ({ default: () => <div data-testid="menubar">MenuBar</div> }));
vi.mock('../Login', () => ({ default: () => <div>Login Page</div> }));


describe('App', () => {
    beforeEach(() => {
        sessionStorage.clear();
        });

    afterAll(() => {
    });

    test('renders MenuBar and Home page by default', () => {
        render(
            <MemoryRouter>
                <App />
            </MemoryRouter>
        );
        expect(screen.getByTestId('menubar')).toBeInTheDocument();
        expect(screen.getByText(/Campus Transit Portal/i)).toBeInTheDocument();
    });

    test('renders Login page when navigating to /login', () => {
        render(
            <MemoryRouter initialEntries={['/login']}>
                <App />
            </MemoryRouter>
        );
        expect(screen.getByText(/Login Page/i)).toBeInTheDocument();
    });

    test('renders 404 page for unknown routes', () => {
        render(
            <MemoryRouter initialEntries={['/unknown']}>
                <App />
            </MemoryRouter>
        );
        expect(screen.getByText(/Error 404 Page Not Found/i)).toBeInTheDocument();
    });

});