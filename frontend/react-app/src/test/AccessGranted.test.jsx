import React from 'react';
import { expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, redirect } from 'react-router-dom';
import AccessGranted from '../AccessGranted.jsx';

describe('AccessGranted', () => {
    test('renders AccessGranted component', () => {
        render(
            <MemoryRouter>
                <AccessGranted />
            </MemoryRouter>
        );
        const headerElement = screen.getByText(/Access Granted/i);
        expect(headerElement).toBeInTheDocument();
        const messageElement = screen.getByText(/Welcome to Penn State Campus! You may enter the parking garage when the gate is open./i);
        expect(messageElement).toBeInTheDocument();
        const noteElement = screen.getByText(/Please have your permit visible/i);
        expect(noteElement).toBeInTheDocument();
    });
});