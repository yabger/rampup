import React, { useState, useEffect } from 'react';
import AppLayout from '../../components/AppLayout/AppLayout';
import layout from '../../styles/dashboard.module.css';
import styles from './NovatoDashboard.module.css';
import { cx } from '../../utils/cx';
import { onboardingAPI } from '../../api/axios_config';
import StuckModal from '../../components/StruckModel/StuckModel';

// Itens do menu lateral
const menu = [
    { label: 'Minha jornada', href: '#jornada', icon: 'flag', current: true },
    { label: 'Documentação', href: '#documentacao', icon: 'book' },
];

export default function NovatoDashboard({ usuarioId = 1, usuario, onLogout }) {
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedPeriod, setSelectedPeriod] = useState('TODOS');
    const [selectedTaskForStuck, setSelectedTaskForStuck] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    // Carrega as tarefas da API ao montar o componente
    useEffect(() => {
        carregarTrilha();
    }, [usuarioId]);

    const carregarTrilha = async () => {
        try {
            setLoading(true);
            const data = await onboardingAPI.getTrilha(usuarioId);
            setTasks(data);
        } catch (err) {
            console.error('Erro ao carregar trilha:', err);
        } finally {
            setLoading(false);
        }
    };

    // Calcula a porcentagem do progresso geral do Onboarding
    const totalTarefas = tasks.length;
    const concluidas = tasks.filter((t) => t.status === 'CONCLUIDO').length;
    const porcentagem = totalTarefas > 0 ? Math.round((concluidas / totalTarefas) * 100) : 0;

    // Filtra as tarefas por período
    const filteredTasks = tasks.filter((t) => {
        if (selectedPeriod === 'TODOS') return true;
        return t.tarefa?.periodo === selectedPeriod;
    });

    // Marca uma tarefa como CONCLUÍDA
    const handleConcluir = async (progressoId) => {
        try {
            await onboardingAPI.atualizarStatus(progressoId, 'CONCLUIDO');
            // Atualiza a lista de tarefas após a conclusão
            setTasks((prev) =>
                prev.map((t) => (t.id_progresso === progressoId ? { ...t, status: 'CONCLUIDO' } : t))
            );
        } catch (err) {
            alert('Erro ao concluir tarefa. Tente novamente.');
        }
    };

    // Abre o modal de "Estou Travado" para a tarefa selecionada
    const handleAbrirStuckModal = (task) => {
        setSelectedTaskForStuck(task);
        setIsModalOpen(true);
    };

    // Callback acionado após confirmar o bloqueio no modal, para atualizar a lista de tarefas
    const handleStuckSuccess = (progressoId) => {
        // Atualiza a tarefa para indicar que está bloqueada
        setTasks((prev) =>
            prev.map((t) => (t.id_progresso === progressoId ? { ...t, status: 'BLOQUEADO' } : t))
        );
    };

    const nome = usuario?.nome || 'Novo colaborador';
    const primeiroNome = nome.split(' ')[0];

    return (
        <AppLayout
            menu={menu}
            onLogout={onLogout}
            topbar={{ section: 'Espaço do novo colaborador', page: 'Minha jornada', nome, papel: 'Novo colaborador' }}
        >
            <main className={layout.main}>
                {/* 1. CABEÇALHO COM PROGRESSO GERAL */}
                <div className={layout.greeting}>
                    <h2 className={layout.title}>Olá, {primeiroNome}</h2>
                    <p className={layout.lead}>Meu Onboarding Técnico — acompanhe suas etapas de integração e alcance sua autonomia técnica.</p>
                </div>

                <section aria-label="Resumo" className={layout.summary}>
                    <div className={layout.statCard}>
                        <span className={layout.statLabel}>Progresso Geral</span>
                        <span className={layout.statValue}>{porcentagem}%</span>
                        <div className={styles.barTrack}>
                            <div className={styles.barFill} style={{ width: `${porcentagem}%` }} />
                        </div>
                        <span className={layout.statLabel}>{concluidas} de {totalTarefas} tarefas concluídas</span>
                    </div>
                </section>

                {/* 2. FILTRO POR PERÍODO (Dia 1, Dia 2, Semana 1...) */}
                <section aria-labelledby="trilha-titulo" className={layout.section}>
                    <div className={styles.sectionHead}>
                        <h3 id="trilha-titulo" className={layout.sectionTitle}>Trilha de onboarding</h3>
                        <nav aria-label="Filtrar por período" className={styles.tabs}>
                            {['TODOS', 'DIA 1', 'DIA 2', 'SEMANA 1', 'SEMANA 2'].map((period) => (
                                <button
                                    key={period}
                                    type="button"
                                    className={styles.tab}
                                    aria-pressed={selectedPeriod === period}
                                    onClick={() => setSelectedPeriod(period)}
                                >
                                    {period.replace('_', ' ')}
                                </button>
                            ))}
                        </nav>
                    </div>

                    {/* 3. LISTA DE TAREFAS */}
                    {loading ? (
                        <div className={layout.loading}>Carregando checklist de onboarding...</div>
                    ) : filteredTasks.length === 0 ? (
                        <p className={styles.empty}>Nenhuma tarefa encontrada para este período.</p>
                    ) : (
                        <div className={styles.list}>
                            {filteredTasks.map((item, i) => {
                                const done = item.status === 'CONCLUIDO' || item.status === 'CONCLUÍDO';
                                const stuck = item.status === 'TRAVADO' || item.status === 'BLOQUEADO';
                                const last = i === filteredTasks.length - 1;
                                return (
                                    <div key={item.id_progresso} className={styles.row}>
                                        <div className={styles.rail}>
                                            <div className={cx(styles.node, done && styles.nodeDone, stuck && styles.nodeStuck)} />
                                            {!last && <div className={cx(styles.line, done && styles.lineDone)} />}
                                        </div>

                                        <div className={cx(styles.card, done && styles.cardDone, stuck && styles.cardStuck)}>
                                            <div className={styles.cardBody}>
                                                <div className={styles.titleRow}>
                                                    <span className={styles.num}>{String(i + 1).padStart(2, '0')}</span>
                                                    <h4 className={styles.cardTitle}>{item.tarefa?.titulo || 'Configuração Técnica'}</h4>
                                                    <span className={cx(styles.status, done && styles.statusDone, stuck && styles.statusStuck)}>{item.status}</span>
                                                </div>
                                                <span className={styles.meta}>
                                                    {item.tarefa?.periodo || 'Sem período'} · Tempo estimado: {item.tarefa?.tempo_estimado_min} minutos
                                                </span>
                                                {item.tarefa?.link_tutorial && (
                                                    <a href={item.tarefa.link_tutorial} target="_blank" rel="noreferrer" className={styles.tutorialLink}>
                                                        Acessar Tutorial
                                                    </a>
                                                )}
                                            </div>

                                            {/* AÇÕES DA TAREFA */}
                                            <div className={styles.actions}>
                                                {item.status !== 'TRAVADO' && item.status !== 'CONCLUÍDO' && (
                                                    <button type="button" className={styles.ghost} onClick={() => handleAbrirStuckModal(item)}>
                                                        Estou Travado
                                                    </button>
                                                )}
                                                {item.status !== 'CONCLUÍDO' && (
                                                    <button type="button" className={styles.btn} onClick={() => handleConcluir(item.id_progresso)}>
                                                        Marcar Concluído
                                                    </button>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </section>
            </main>

            {/* 4. MODAL DO BOTÃO 'ESTOU TRAVADO' */}
            <StuckModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                task={selectedTaskForStuck}
                onSuccess={handleStuckSuccess}
            />
        </AppLayout>
    );
}
