require('dotenv').config();
if (!process.env.JWT_SECRET) throw new Error('JWT_SECRET não definido. Copie .env.example para .env e configure um segredo.');
const app = require('./app');
const port = Number(process.env.PORT || 3000);
const server = app.listen(port, () => console.log(`RampUp API disponível em http://localhost:${port}`));
async function shutdown() { server.close(); }
process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
