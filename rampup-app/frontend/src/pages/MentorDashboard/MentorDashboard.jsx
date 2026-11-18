import React, { useState, useEffect } from 'react';
import AppLayout from '../../components/AppLayout/AppLayout';
import layout from '../../styles/dashboard.module.css';
import styles from './MentorDashboard.module.css';
import { mentorAPI, blockAPI } from '../../api/axios_config';

// Itens do menu lateral
const menu = [
    { label: 'Alertas de bloqueio', href: '#alertas', icon: 'bell', current: true },
    { label: 'Documentação', href: '#documentacao', icon: 'book' },
];

export default function MentorDashboard({ mentorId = 2, usuario, onLogout }) {
    const [bloqueios, setBloqueios] = useState([]);
    const [loading, setLoading] = useState(true);
    const [resolvingId, setResolvingId] = useState(null);

    // Carrega os alertas direcionados a este mentor ao montar a página
    useEffect(() => {
        carregarAlertas();
    }, [mentorId]);

    const carregarAlertas = async () => {
        try {
            setLoading(true);
            const data = await mentorAPI.getDashboard(mentorId);
            setBloqueios(data);
        } catch (error) {
            console.error('Erro ao carregar alertas:', error);
        } finally {
            setLoading(false);
        }
    };

    // Aciona a rota REST para marcar o bloqueio como RESOLVIDO
    const handleDestravar = async (idBloqueio) => {
        try {
            setResolvingId(idBloqueio);
            await blockAPI.destravarNovato(idBloqueio);
            // Remove o alerta resolvido da lista na tela em tempo real
            setBloqueios((prev) => prev.filter((item) => item.id !== idBloqueio));
        } catch (err) {
            alert('Falha ao destravar tarefa. Tente novamente.');
        } finally {
            setResolvingId(null);
        }
    };

    const nome = usuario?.nome || 'Mentor';
    const primeiroNome = nome.split(' ')[0];

    return (
        <AppLayout
            menu={menu}
            onLogout={onLogout}
            topbar={{ section: 'Espaço do mentor', page: 'Alertas de bloqueio', nome, papel: 'Mentor (Buddy)' }}
        >
            <main className={layout.main}>
                {/* 1. CABEÇALHO DO PAINEL DO MENTOR */}
                <div className={layout.greeting}>
                    <h2 className={layout.title}>Olá, {primeiroNome}</h2>
                    <p className={layout.lead}>
                        Painel do Mentor — acompanhe os alertas de bloqueio técnico em tempo real e destrave o seu time.
                    </p>
                </div>

                <section aria-label="Resumo" className={layout.summary}>
                    <div className={layout.statCard}>
                        <span className={layout.statLabel}>{bloqueios.length === 1 ? 'Alerta Ativo' : 'Alertas Ativos'}</span>
                        <span className={layout.statValue}>{bloqueios.length}</span>
                        <span className={layout.statLabel}>
                            {bloqueios.length === 0 ? 'Nenhum bloqueio na fila' : 'Aguardando a sua ajuda'}
                        </span>
                    </div>
                </section>

                {/* 2. LISTA DE ALERTAS DE BLOQUEIO */}
                <section aria-labelledby="alertas-titulo" className={layout.section}>
                    <h3 id="alertas-titulo" className={layout.sectionTitle}>Fila de alertas</h3>

                    {loading ? (
                        <div className={layout.loading}>Carregando alertas da fila...</div>
                    ) : bloqueios.length === 0 ? (
                        /* ESTADO VAZIO: NENHUM ERRO ATIVO */
                        <div className={styles.emptyState}>
                            <h4 className={styles.emptyTitle}>Nenhum alerta de bloqueio no momento.</h4>
                            <p className={styles.emptyText}>
                                Seus novatos supervisionados estão avançando pelas trilhas de onboarding sem travamentos ativos.
                            </p>
                        </div>
                    ) : (
                        /* GRID DE CARDS DE BLOQUEIO ATIVOS */
                        <div className={styles.grid}>
                            {bloqueios.map((item) => (
                                <div key={item.id_bloqueio} className={styles.card}>
                                    <div className={styles.cardHeader}>
                                        <span>
                                            Colaborador: <strong>{item.progresso_tarefa?.usuario?.nome || 'Lucas Rocha'}</strong>
                                        </span>
                                        <span className={styles.time}>
                                            {new Date(item.data_bloqueio).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </span>
                                    </div>

                                    <h4 className={styles.taskTitle}>
                                        {item.progresso_tarefa?.tarefa?.titulo || 'Configuração Técnica'}
                                    </h4>

                                    {/* LOG DE ERRO (TERMINAL STYLE) */}
                                    <div className={styles.log}>
                                        <div className={styles.logHeader}>Terminal / Stacktrace do Erro</div>
                                        <pre className={styles.logCode}>{item.log_erro}</pre>
                                    </div>

                                    {/* BOTÃO DE AÇÃO DO MENTOR */}
                                    <button
                                        type="button"
                                        className={styles.btn}
                                        onClick={() => handleDestravar(item.id_bloqueio)}
                                        disabled={resolvingId === item.id_bloqueio}
                                    >
                                        {resolvingId === item.id_bloqueio ? 'Destravando...' : 'Destravar Tarefa'}
                                    </button>
                                </div>
                            ))}
                        </div>
                    )}
                </section>
            </main>
        </AppLayout>
    );
}
