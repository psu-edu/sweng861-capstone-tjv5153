import React from 'react';
import { expect, test, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, redirect } from 'react-router-dom';
import CheckTickets from '../CheckTickets.jsx';
import userEvent from '@testing-library/user-event';
import ApiClientFetch from '../ApiClient.jsx';
import LicensePlate from '../LicensePlate.jsx';
import { ApiClientPostFile } from '../ApiClient.jsx';

vi.mock('../ApiClient.jsx', () => ({ default: vi.fn() }));
vi.mock('../ApiClient.jsx', () => ({ ApiClientPostFile: vi.fn() }));

test('LicensePlate component renders', () => {
    render(
        <MemoryRouter>
            <LicensePlate />
        </MemoryRouter>
    );
    const inputElement = screen.getByText(/Please upload an image of your license plate to access the garage/i);
    expect(inputElement).toBeInTheDocument();
});