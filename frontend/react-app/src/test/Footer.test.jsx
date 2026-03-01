import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Footer from '../Footer';


describe('Footer', () => {
    test('renders Footer component', () => {
        render(
            <MemoryRouter>
                <Footer />
            </MemoryRouter>
        );
        const footerElement = screen.getByText(/Penn State Campus Transit/i);
        const footerElement2 = screen.getByText(/SWENG 861 Capstone Project/i);
        const footerElement3 = screen.getByText(/© 2026 Tim Volkar. All rights reserved./i);
        expect(footerElement).toBeInTheDocument();
        expect(footerElement2).toBeInTheDocument();
        expect(footerElement3).toBeInTheDocument();

    });
});