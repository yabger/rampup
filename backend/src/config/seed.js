require('dotenv').config();
const bcrypt = require('bcryptjs');
const db = require('./db');
(async () => {
  try {
    const hash = await bcrypt.hash('RampUpDemo!2026', 12);
    const users = [
      ['Lucas Rocha','lucas@rampup.local','novato'],
      ['Bruno Santos','bruno@rampup.local','buddy'],
      ['Mariana Costa','mariana@rampup.local','gestor'],
    ];
    const ids = {};
    for (const [name,email,role] of users) {
      const result = await db.query(`INSERT INTO users(name,email,password_hash,role) VALUES($1,$2,$3,$4) ON CONFLICT(email) DO UPDATE SET name=EXCLUDED.name,role=EXCLUDED.role,password_hash=EXCLUDED.password_hash RETURNING id`, [name,email,hash,role]);
      ids[role] = result.rows[0].id;
    }
    const tasks = [
      ['Configurar ambiente de desenvolvimento','Instalar ferramentas e preparar a estação.','Dia 1',1],
      ['Clonar repositório','Solicitar acesso e clonar o repositório do time.','Dia 1',2],
      ['Configurar Docker','Validar instalação e executar os containers necessários.','Dia 2',3],
      ['Executar testes do projeto','Executar a suíte de testes e analisar resultados.','Semana 1',4],
      ['Realizar primeira entrega','Enviar uma contribuição revisada por Pull Request.','Semana 1',5]
    ];
    for (const [title,description,period,position] of tasks) {
      await db.query(`INSERT INTO tasks(title,description,period,position) SELECT $1,$2,$3,$4 WHERE NOT EXISTS(SELECT 1 FROM tasks WHERE title=$1)`,[title,description,period,position]);
    }
    await db.query('INSERT INTO mentorships(novice_id,buddy_id) VALUES($1,$2) ON CONFLICT DO NOTHING',[ids.novato,ids.buddy]);
    await db.query(`INSERT INTO task_progress(user_id,task_id,status) SELECT $1,id,'pendente' FROM tasks ON CONFLICT(user_id,task_id) DO NOTHING`,[ids.novato]);
    console.log('Dados demonstrativos criados. Senha comum: RampUpDemo!2026');
  } catch(e) { console.error('Falha no seed:',e.message); process.exitCode=1; }
  finally { await db.pool.end(); }
})();
