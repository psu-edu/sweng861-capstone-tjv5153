import { afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import '@testing-library/jest-dom/vitest'; // Extends 'expect' with DOM-specific matchers

// Automatically unmounts React components after each test to prevent memory leaks
afterEach(() => {
  cleanup();
});
