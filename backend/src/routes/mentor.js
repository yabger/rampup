const router = require('express').Router();
const db = require('../config/db');
const { authenticate, authorize } = require('../middleware/auth');
router.use(authenticate, authorize('buddy','gestor'));
router.get('/buddies/dashboard', async (req, res, next) => {
  try {
    const novices = await db.query(`SELECT u.id,u.name,COUNT(p.id)::int total,COUNT(p.id) FILTER (WHERE p.status='concluido')::int completed,
      CASE WHEN COUNT(p.id)=0 THEN 0 ELSE ROUND(100.0*COUNT(p.id) FILTER (WHERE p.status='concluido')/COUNT(p.id))::int END progress
      FROM mentorships m JOIN users u ON u.id=m.novice_id LEFT JOIN task_progress p ON p.user_id=u.id
      WHERE m.buddy_id=$1 GROUP BY u.id,u.name ORDER BY u.name`, [req.user.sub]);
    const blockers = await db.query(`SELECT b.id,b.error_log,b.created_at,u.id novice_id,u.name novice_name,t.id task_id,t.title task_title
      FROM blockers b JOIN users u ON u.id=b.user_id JOIN tasks t ON t.id=b.task_id
      JOIN mentorships m ON m.novice_id=u.id WHERE m.buddy_id=$1 AND b.status='aberto' ORDER BY b.created_at`, [req.user.sub]);
    res.json({ novices: novices.rows, blockers: blockers.rows });
  } catch (e) { next(e); }
});
router.put('/blockers/:id/resolve', async (req, res, next) => {
  const client = await db.pool.connect();
  try {
    const id = Number(req.params.id); const note = (req.body || {}).resolutionNote || null;
    await client.query('BEGIN');
    const result = await client.query(`UPDATE blockers b SET status='resolvido',resolution_note=$2,resolved_by=$3,resolved_at=NOW()
      FROM mentorships m WHERE b.id=$1 AND m.novice_id=b.user_id AND m.buddy_id=$3 AND b.status='aberto' RETURNING b.user_id,b.task_id`, [id,note,req.user.sub]);
    if (!result.rowCount) { await client.query('ROLLBACK'); return res.status(404).json({ error: 'Bloqueio não encontrado ou não pertence a um novato acompanhado por você.' }); }
    await client.query("UPDATE task_progress SET status='pendente',updated_at=NOW() WHERE user_id=$1 AND task_id=$2 AND status='travado'", [result.rows[0].user_id,result.rows[0].task_id]);
    await client.query('COMMIT');
    res.json({ message: 'Bloqueio resolvido. A tarefa foi liberada para o novato.' });
  } catch (e) { await client.query('ROLLBACK'); next(e); }
  finally { client.release(); }
});
module.exports = router;
