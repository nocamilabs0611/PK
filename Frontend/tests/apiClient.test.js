import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import apiClient from '../src/services/apiClient.js';

describe('ApiClient Core Suite', () => {
  it('should allow setting auth tokens and toggling mock mode', () => {
    apiClient.setToken('test-bearer-token-123');
    assert.equal(apiClient.token, 'test-bearer-token-123');

    apiClient.setUseMock(true);
    assert.equal(apiClient.useMock, true);

    apiClient.setUseMock(false);
    assert.equal(apiClient.useMock, false);

    // Reset back to mock for safe unit testing
    apiClient.setUseMock(true);
  });

  it('should return mock response directly when in mock mode', async () => {
    apiClient.setUseMock(true);
    const mockData = { id: 'TEST-1', status: 'OK' };
    const response = await apiClient.get('/test/endpoint', mockData, 0);
    assert.deepEqual(response, mockData);
  });

  it('should execute functional mock handlers with request payload', async () => {
    apiClient.setUseMock(true);
    const mockFn = (payload) => ({ echoed: payload.value * 2 });
    const response = await apiClient.post('/test/echo', { value: 21 }, mockFn, 0);
    assert.equal(response.echoed, 42);
  });
});
