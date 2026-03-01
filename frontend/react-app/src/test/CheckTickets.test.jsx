import React from 'react';
import { expect, test, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, redirect } from 'react-router-dom';
import CheckTickets from '../CheckTickets.jsx';
import userEvent from '@testing-library/user-event';
import ApiClientFetch from '../ApiClient.jsx';

vi.mock('../ApiClient.jsx', () => ({ default: vi.fn() }));


describe('CheckTickets render', () => {
    test('renders CheckTickets component', () => {
        render(
            <MemoryRouter>
                <CheckTickets />
            </MemoryRouter>
        );
        const headerElement = screen.getByText(/Check Tickets/i);
        expect(headerElement).toBeInTheDocument();
    });
});

test('CheckTickets API call and display', async () => {
    const mockTickets = [
        { id: 1, licensePlate: 'ABC123', violation: 'Expired Meter', fineAmount: 25 },
        { id: 2, licensePlate: 'XYZ789', violation: 'No Parking Zone', fineAmount: 50 }
    ];

        ApiClientFetch.mockResolvedValue(mockTickets);

    render(
        <MemoryRouter>
            <CheckTickets />
        </MemoryRouter>
    );

    userEvent.click(screen.getByRole('button', { name: /Submit Details/i }));
});

