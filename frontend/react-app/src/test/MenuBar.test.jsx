import { render, screen } from '@testing-library/react';
import { expect, test } from 'vitest';
import MenuBar from '../MenuBar.jsx';
import { MemoryRouter } from 'react-router-dom';

test('renders MenuBar with correct links', () => {
    render(
        <MemoryRouter>
            <MenuBar />
        </MemoryRouter>
    );
    const homeLink = screen.getByText('Home');
    expect(homeLink).toBeInTheDocument();
    const commuter = screen.getByText('Commuter Dashboard');
    expect(commuter).toBeInTheDocument();
    const officer = screen.getByText('Officer Dashboard');
    expect(officer).toBeInTheDocument();
    const loginLink = screen.getByText('Login');
    expect(loginLink).toBeInTheDocument();  
});