import React, { useState, useEffect } from 'react'; 
import { onboardingAPI } from '../api/axios_config'; 
import StuckModal from '../components/StuckModel';

export default function NovatoDashboard({ usuarioId = 1 }) { 
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

    //Calcula a porcentagem do progresso geral do Onboarding
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

    return (
        <div style={styles.container}>
            {/*1. CABEÇALHO COM PROGRESSO GERAL*/}
            <header style={styles.header}>
                <div>
                    <h2> Meu Onboarding Técnico</h2>
                    <p style={styles.subtext}>Acompanhe suas etapas de integração e alcance sua autonomia técnica</p>
                </div>

                <div style={styles.progressContainer}>
                    <div style={styles.progressText}>
                        <span> Progresso Geral</span>
                        <strong> {porcentagem}%</strong>
                    </div>
                    <div style={styles.progressBarTrack}>
                        <div style={{ ...styles.progressBarFill, width: `${porcentagem}%` }}></div>
                    </div>
                </div>
            </header>

            {/*2. FILTRO POR PERÍODO (Dia 1, Dia 2, Semana 1...)*/}
            <nav style={styles.navTabs}>
                {['TODOS', 'DIA 1', 'DIA 2', 'SEMANA 1', 'SEMANA 2'].map((period) => (
                    <button
                        key={period}
                        style={{
                            ...styles.tabButton,
                            ...(selectedPeriod === period ? styles.activeTab : {}),
                        }}
                        onClick={() => setSelectedPeriod(period)}
                    >
                        {period.replace('_', ' ')}
                    </button>
                ))}
            </nav>

            {/*3. LISTA DE CARDS DE TAREFAS*/}
            {loading ? (
                <div style={styles.loading}>Carregando checklist de onboarding...</div>
            ) : (
                <div style={styles.taskList}>
                    {filteredTasks.length === 0 ? (
                        <p>Nenhuma tarefa encontrada para este período.</p>
                    ) : (
                        filteredTasks.map((item) => (
                            <div key={item.id_progresso} style={getCardStyle(item.status)}>
                                <div style={styles.cardHeader}>
                                    <span style={styles.periodBadge}>{item.tarefa?.periodo || 'Sem período'}</span>
                                    <span style={getStatusBadgeStyle(item.status)}>{item.status}</span>
                                </div>

                                <h4 style={styles.cardTitle}>{item.tarefa?.titulo || 'Configuração Técnica'}</h4>
                                <p style={styles.cardTime}>Tempo estimado: {item.tarefa?.tempo_estimado_min} minutos</p>

                                {item.tarefa?.link_tutorial && (
                                    <a
                                        href={item.tarefa.link_tutorial}
                                        target="_blank"
                                        rel="noreferrer"
                                        style={styles.tutorialLink}
                                    >
                                        Acessar Tutorial
                                    </a>
                                )}

                                {/* AÇÕES DA TAREFA */}
                                <div style={styles.cardActions}>
                                    {item.status !== 'CONCLUÍDO' && (
                                        <button
                                            onClick={() => handleConcluir(item.id_progresso)}
                                            style={styles.btnConcluir}
                                        >
                                            ✓ Marcar Concluído
                                        </button>
                                    )}
                                    {item.status !== 'TRAVADO' && item.status !== 'CONCLUÍDO' && (
                                        <button
                                            onClick={() => handleAbrirStuckModal(item)}
                                            style={styles.btnStuck}
                                        >
                                            🚨 Estou Travado
                                        </button>
                                    )}
                                </div>
                            </div>
                        ))
                    )}
                </div>
            )}

            {/* 4. MODAL DO BOTÃO 'ESTOU TRAVADO' */}
            <StuckModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                task={selectedTaskForStuck}
                onSuccess={handleStuckSuccess}
            />
        </div>
    );
}

// Estilos Visuais em JS 
const styles = { 
    container: { maxWidth: '1000px', margin: '0 auto', padding: '20px', fontFamily: 'sans-serif' }, 
    header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: '16px' }, 
    subtext: { color: '#666', margin: '4px 0 0 0' }, 
    progressContainer: { minWidth: '240px' }, 
    progressText: { display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }, 
    progressBarTrack: { width: '100%', height: '12px', backgroundColor: '#e0e0e0', borderRadius: '6px', overflow: 'hidden' }, 
    progressBarFill: { height: '100%', backgroundColor: '#28a745', transition: 'width 0.3s ease' }, 
    navTabs: { display: 'flex', gap: '8px', marginBottom: '20px' }, 
    tabButton: { padding: '8px 16px', border: '1px solid #ddd', borderRadius: '20px', background: '#fff', cursor: 'pointer', fontWeight: '500' }, 
    activeTab: { background: '#007bff', color: '#fff', borderColor: '#007bff' }, 
    taskList: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }, 
    cardHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }, 
    periodBadge: { fontSize: '0.75rem', padding: '2px 8px', borderRadius: '4px', background: '#eee', fontWeight:'bold' }, 
    cardTitle: { margin: '0 0 8px 0', fontSize: '1.1rem' }, 
    cardTime: { fontSize: '0.85rem', color:'#666', margin:'0 0 12px 0' }, 
    tutorialLink: { display:'inline-block', fontSize:'0.85rem', color:'#007bff', textDecoration:'none', marginBottom:'16px' }, 
    cardActions: { display:'flex', gap:'8px', marginTop:'auto' }, 
    btnConcluir: { flex:1, padding:'8px', border:'none', borderRadius:'4px', background:'#28a745', color:'#fff', cursor:'pointer', fontWeight:'bold' }, 
    btnStuck:{ padding:'8px 12px', border: '1px solid #dc3545', borderRadius: '4px', background: '#fff', color: '#dc3545', cursor: 'pointer', fontWeight: 'bold' }, 
    loading:{ textAlign:'center', padding:'40px', color:'#666' }
};

const getCardStyle = (status) => ({
    backgroundColor: '#fff',
    borderRadius: '8px',
    padding: '16px',
    display: 'flex',
    flexDirection: 'column',
    border: status === 'TRAVADO' ? '2px solid #dc3545' : status === 'CONCLUIDO' ? '1px solid #28a745' : '1px solid #ddd',
    boxShadow: '0 2px 8px rgba(0,0,0,0.05)',
    opacity: status === 'CONCLUIDO' ? 0.8 : 1,
});

const getStatusBadgeStyle = (status) => {
    const bgMap = { PENDENTE: '#ffc107', CONCLUIDO: '#28a745', TRAVADO: '#dc3545' };
    return { 
        fontSize: '0.75rem', 
        color: '#fff', 
        padding: '2px 8px', 
        borderRadius: '4px', 
        fontWeight: 'bold', 
        backgroundColor: bgMap[status] || '#6c757d', };
};