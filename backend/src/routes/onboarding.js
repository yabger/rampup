const router = require('express').Router();
const db = require('../config/db');
const { authenticate, authorize } = require('../middleware/auth');
router.use(authenticate);

router.get('/trilha', authorize('novato'), async (req, res, next) => {
  try {
    const result = await db.query(`SELECT t.id,t.title,t.description,t.period,t.position,COALESCE(p.status,'pendente') status
      FROM tasks t LEFT JOIN task_progress p ON p.task_id=t.id AND p.user_id=$1 ORDER BY t.position,t.id`, [req.user.sub]);
    const total = result.rowCount;
    const completed = result.rows.filter(t => t.status === 'concluido').length;
    res.json({ tasks: result.rows, progress: total ? Math.round(completed / total * 100) : 0, total, completed });
  } catch (e) { next(e); }
});
router.put('/tasks/:id/complete', authorize('novato'), async (req, res, next) => {
  try {
    const taskId = Number(req.params.id);
    if (!Number.isInteger(taskId)) return res.status(400).json({ error: 'Identificador de tarefa inválido.' });
    const task = await db.query('SELECT id FROM tasks WHERE id=$1', [taskId]);
    if (!task.rowCount) return res.status(404).json({ error: 'Tarefa não encontrada.' });
    const open = await db.query("SELECT id FROM blockers WHERE task_id=$1 AND user_id=$2 AND status='aberto'", [taskId, req.user.sub]);
    if (open.rowCount) return res.status(409).json({ error: 'Resolva o bloqueio antes de concluir a tarefa.' });
    await db.query(`INSERT INTO task_progress(user_id,task_id,status) VALUES($1,$2,'concluido')
      ON CONFLICT(user_id,task_id) DO UPDATE SET status='concluido',updated_at=NOW()`, [req.user.sub, taskId]);
    res.json({ message: 'Tarefa concluída.', taskId, status: 'concluido' });
  } catch (e) { next(e); }
});
router.post('/tasks/:id/stuck', authorize('novato'), async (req, res, next) => {
  try {
    const taskId = Number(req.params.id); const { errorLog } = req.body || {};
    if (!Number.isInteger(taskId) || typeof errorLog !== 'string' || !errorLog.trim()) return res.status(400).json({ error: 'Informe uma tarefa válida e o log do erro.' });
    const task = await db.query('SELECT id FROM tasks WHERE id=$1', [taskId]);
    if (!task.rowCount) return res.status(404).json({ error: 'Tarefa não encontrada.' });
    const result = await db.query('INSERT INTO blockers(user_id,task_id,error_log) VALUES($1,$2,$3) RETURNING id,status,created_at', [req.user.sub, taskId, errorLog.trim()]);
    await db.query(`INSERT INTO task_progress(user_id,task_id,status) VALUES($1,$2,'travado') ON CONFLICT(user_id,task_id) DO UPDATE SET status='travado',updated_at=NOW()`, [req.user.sub, taskId]);
    res.status(201).json({ message: 'Bloqueio registrado e disponibilizado ao Buddy.', blocker: result.rows[0] });
  } catch (e) { next(e); }
});
router.post('/documentation-issues', authorize('novato'), async (req, res, next) => {
  try {
    const { taskId, description } = req.body || {};
    if (typeof description !== 'string' || !description.trim()) return res.status(400).json({ error: 'Descreva o problema na documentação.' });
    const result = await db.query('INSERT INTO documentation_issues(user_id,task_id,description) VALUES($1,$2,$3) RETURNING *', [req.user.sub, taskId || null, description.trim()]);
    res.status(201).json({ issue: result.rows[0] });
  } catch (e) { next(e); }
});
module.exports = router;
