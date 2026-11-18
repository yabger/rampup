import React, { useState, useEffect } from 'react'; 
import { mentorAPI, blockAPI } from '../api/axios_config';

export default function MentorDashboard({ mentorId = 2 }) { 
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
            setBloqueios((prev) =>
                prev.filter((item) => item.id_bloqueio !== idBloqueio)
            );
        } catch (err) {
	     alert('Falha ao destravar tarefa. Tente novamente.');
        } finally {
            setResolvingId(null);
        }
    };

    return (
        <div style={styles.container}>
            {/* 1. CABEÇALHO DO PAINEL DO MENTOR */}
            <header style={styles.header}>
                <div>
                    <h2>🛡️ Painel do Mentor (Buddy)</h2>
                    <p style={styles.subtext}>
                        Acompanhe os alertas de bloqueio técnico em tempo real e destrave o seu time.
                    </p>
                </div>

                <div style={styles.badgeContainer}>
                    <div style={styles.badgeCount}>{bloqueios.length}</div>
                    <span style={styles.badgeLabel}>
                        {bloqueios.length === 1 ? 'Alerta Ativo' : 'Alertas Ativos'}
                    </span>
                </div>
            </header>

            {/* 2. CONTEÚDO / LISTA DE ALERTAS DE BLOQUEIO */}
            {loading ? (
                <div style={styles.loading}>Carregando alertas da fila...</div>
            ) : bloqueios.length === 0 ? (
                /* ESTADO VAZIO: NENHUM ERRO ATIVO */
                <div style={styles.emptyState}>
                    <div style={styles.emptyIcon}>🎉</div>
                    <h3>Nenhum alerta de bloqueio no momento.</h3>
                    <p style={styles.emptyText}>
                    Seus novatos supervisionados estão avançando pelas trilhas de onboarding sem travamentos ativos.
                    </p>
                </div>     
            ) : (
                /* GRID DE CARDS DE BLOQUEIO ATIVOS */
                <div style={styles.grid}>
                    {bloqueios.map((item) => (
                        <div key={item.id_bloqueio} style={styles.card}>
                            <div style={styles.cardHeader}>
                                <span style={styles.userBadge}>
                                    👤 Colaborador: <strong>{item.progresso_tarefa?.usuario?.nome || 'Lucas Rocha'}</strong>
                                </span>
                                <span style={styles.timeBadge}>
                                    🕒 {new Date(item.data_bloqueio).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </span>
                                </div>

                                <h4 style={styles.taskTitle}>
                                    📌 {item.progresso_tarefa?.tarefa?.titulo || 'Configuração Técnica'}
                                </h4>

                                {/* BLUSTRO COM O LOG DE ERRO (TERMINAL STYLE) */}
                                <div style={styles.logContainer}>
                                    <div style={styles.logHeader}>Terminal / Stacktrace do Erro:</div>
                                    <pre style={styles.logCode}>{item.log_erro}</pre>
                                </div>

                                {/* BOTÃO DE AÇÃO DO MENTOR */}
                                <button
                                    onClick={() => handleDestravar(item.id_bloqueio)}
                                    disabled={resolvingId === item.id_bloqueio}
                                    style={{
                                        ...styles.btnDestravar,
                                        ...(resolvingId === item.id_bloqueio ? styles.btnDisabled : {}),
                                    }}
                                >
                                    {resolvingId === item.id_bloqueio ? 'Destravando...' : 'Destravar Tarefa'}
                                </button>
                            </div>
                    ))}
                </div>
            )}
        </div>
    );
}

// Estilos visuais dinâmicos 

const styles = { 
    container: { maxWidth: '1000px', margin: '0 auto', padding: '20px', fontFamily: 'sans-serif' }, 
    header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: '16px' }, 
    subtext: { color: '#666', margin: '4px 0 0 0' }, 
    badgeContainer: { display: 'flex', alignItems: 'center', gap: '12px', background: '#fff3cd', padding: '10px 16px', borderRadius: '8px', border: '1px solid #ffeeba' }, 
    badgeCount: { background: '#dc3545', color: '#fff', fontSize: '1.2rem', fontWeight: 'bold', width: '32px', height: '32px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }, 
    badgeLabel: { fontWeight: 'bold', color: '#856404' }, 
    grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '20px' }, 
    card: { backgroundColor: '#fff', borderRadius: '10px', padding: '20px', borderLeft: '5px solid #dc3545', boxShadow: '0 4px 12px rgba(0,0,0,0.08)', display: 'flex', flexDirection: 'column' }, 
    cardHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px', fontSize: '0.85rem' }, 
    userBadge: { color: '#333' }, 
    timeBadge: { color: '#888' }, 
    taskTitle: { margin: '0 0 16px 0', fontSize: '1.1rem', color: '#111' }, 
    logContainer: { backgroundColor: '#1e1e1e', borderRadius: '6px', padding: '12px', marginBottom: '16px', flex: 1 }, 
    logHeader: { color: '#aaa', fontSize: '0.75rem', textTransform: 'uppercase', marginBottom: '6px', fontWeight: 'bold' }, 
    logCode: { color: '#ff6b6b', fontFamily: 'monospace', fontSize: '0.85rem', margin: 0, whiteSpace: 'pre-wrap', wordBreak: 'break-word', maxHeight: '120px', overflowY: 'auto' }, 
    btnDestravar: { width: '100%', padding: '10px', border: 'none', borderRadius: '6px', backgroundColor: '#28a745', color: '#fff', fontSize: '0.95rem', fontWeight: 'bold', cursor: 'pointer', transition: 'background-color 0.2s' }, 
    btnDisabled: { backgroundColor: '#6c757d', cursor: 'not-allowed' }, 
    emptyState: { textAlign: 'center', padding: '60px 20px', backgroundColor: '#f8f9fa', borderRadius: '12px', border: '2px dashed #dee2e6' }, 
    emptyIcon: { fontSize: '3rem', marginBottom: '12px' }, 
    emptyText: { color: '#666', maxWidth: '400px', margin: '0 auto' }, 
    loading: { textAlign: 'center', padding: '40px', color: '#666' } 
};


