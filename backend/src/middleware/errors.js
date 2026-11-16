function notFound(req, res) { res.status(404).json({ error: 'Endpoint não encontrado.' }); }
function errorHandler(err, req, res, next) {
  console.error(err);
  res.status(err.status || 500).json({ error: err.status ? err.message : 'Erro interno do servidor.' });
}
module.exports = { notFound, errorHandler };
