require('dotenv').config();
const fs = require('fs');
const path = require('path');
const db = require('./db');

(async () => {
  try {
    const schema = fs.readFileSync(path.join(__dirname, 'schema.sql'), 'utf8');
    await db.query(schema);
    console.log('Esquema RampUp criado/verificado com sucesso.');
  } catch (error) {
    console.error('Falha ao inicializar banco:', error.message);
    process.exitCode = 1;
  } finally {
    await db.pool.end();
  }
})();
