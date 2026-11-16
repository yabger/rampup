const request = require('supertest');
const app = require('../src/app');
describe('API RampUp', () => {
  test('GET /health responde status ok', async () => {
    const response = await request(app).get('/health');
    expect(response.status).toBe(200);
    expect(response.body.status).toBe('ok');
  });
  test('rota inexistente responde 404 em JSON', async () => {
    const response = await request(app).get('/nao-existe');
    expect(response.status).toBe(404);
    expect(response.body.error).toBeDefined();
  });
});
