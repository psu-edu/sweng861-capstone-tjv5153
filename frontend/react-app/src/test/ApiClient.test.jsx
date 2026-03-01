import React from 'react';
import { expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, redirect } from 'react-router-dom';
import ApiClientFetch, { ApiClientGetUserInfo, ApiClientPost, ApiClientDelete, ApiClientPut, ApiClientPostFile } from '../ApiClient.jsx';

global.fetch = vi.fn()

describe('ApiClient', () => {
    beforeEach(() => {
        sessionStorage.clear();
    });

    afterAll(() => {
        delete global.fetch;
    });

    test('ApiClientFetch should fetch data from API', async () => {
        const mockResponse = { message: 'Success' };
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => mockResponse
        });
        
        const response = await ApiClientFetch('/test-endpoint');
        const data = await response.json();
        expect(data).toEqual(mockResponse);
    });

    test('ApiClientFetch should handle 404 error', async () => {
        global.fetch.mockResolvedValueOnce({
            ok: false,
            status: 404,
            statusText: 'Not Found'
        });
        try {
            await ApiClientFetch('/nonexistent-endpoint');
        } catch (error) {
            expect(error.message).toBe('API request failed: Not Found');
        }  
    });

    test('ApiClientPost should post data to API', async () => {
        const mockResponse = { message: 'Data posted successfully' };
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => mockResponse
        });
        const response = await ApiClientPost('/post-endpoint', { key: 'value' });
        const data = await response.json();
        expect(data).toEqual(mockResponse);
    });

    test('ApiClientPut should update data to API', async () => {
        const mockResponse = { message: 'PUT successfully' };
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => mockResponse
        });
        const response = await ApiClientPut('/put-endpoint', { key: 'value' });
        const data = await response.json();
        expect(data).toEqual(mockResponse);
    });

    test('ApiClientDelete should delete data from API', async () => {
        const mockResponse = { message: 'DELETE successfully' };
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => mockResponse
        });
        const response = await ApiClientDelete('/delete-endpoint');
        const data = await response.json();
        expect(data).toEqual(mockResponse);
    });

    test('ApiClientPostFile should post file to API', async () => {
        const mockResponse = { message: 'File uploaded successfully' };
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => mockResponse
        });
        const file = new File(['file content'], 'test.txt', { type: 'text/plain' });
        const response = await ApiClientPostFile('/upload-endpoint', file);
        const data = await response.json();
        expect(data).toEqual(mockResponse);
    });

    test('ApiClientFetch protected endpoint without authentication', async () => {
        sessionStorage.setItem("authStatus", "true");
        global.fetch.mockResolvedValueOnce({
            ok: false,
            status: 403,
            statusText: 'Forbidden'
        });
        await ApiClientFetch('/protected-endpoint');
        expect(sessionStorage.getItem("authStatus")).toBe("false");
    });
});