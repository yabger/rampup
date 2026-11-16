const router = require('express').Router();
const db = require('../config/db');
const { authenticate, authorize } = require('../middleware/auth');
router.use(authenticate, authorize('gestor'));
router.get('/rampup-time', async (req, res, next) => {
  try {
    const progress = await db.query(`SELECT COUNT(DISTINCT user_id)::int active_novices,
      ROUND(AVG(progress_pct))::int average_completion FROM (
        SELECT user_id,100.0*COUNT(*) FILTER(WHERE status='concluido')/NULLIF(COUNT(*),0) progress_pct
        FROM task_progress GROUP BY user_id) p`);
    const docs = await db.query("SELECT status,COUNT(*)::int total FROM documentation_issues GROUP BY status ORDER BY status");
    const blockers = await db.query("SELECT COUNT(*) FILTER(WHERE status='aberto')::int open,COUNT(*) FILTER(WHERE status='resolvido')::int resolved FROM blockers");
    res.json({ ...progress.rows[0], documentationIssues: docs.rows, blockers: blockers.rows[0] });
  } catch (e) { next(e); }
});
router.get('/documentation-issues', async (req, res, next) => {
  try {
    const result = await db.query(`SELECT d.id,d.description,d.status,d.created_at,u.name reporter,t.title task_title
      FROM documentation_issues d JOIN users u ON u.id=d.user_id LEFT JOIN tasks t ON t.id=d.task_id ORDER BY d.created_at DESC`);
    res.json({ issues: result.rows });
  } catch (e) { next(e); }
});
router.patch('/documentation-issues/:id', async (req, res, next) => {
  try {
    const { status } = req.body || {};
    if (!['pendente','em_revisao','resolvido'].includes(status)) return res.status(400).json({ error: 'Status inválido.' });
    const result = await db.query('UPDATE documentation_issues SET status=$1 WHERE id=$2 RETURNING *', [status, Number(req.params.id)]);
    if (!result.rowCount) return res.status(404).json({ error: 'Registro não encontrado.' });
    res.json({ issue: result.rows[0] });
  } catch (e) { next(e); }
});
module.exports = router;
