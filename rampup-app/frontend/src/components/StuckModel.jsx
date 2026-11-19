import React, { useState } from 'react'; 
import { blockAPI } from '../api/axios_config';

export default function StuckModal({ isOpen, onClose, task, onSuccess }) { 
    const [logErro, setLogErro] = useState(''); 
    const [loading, setLoading] = useState(false); 
    const [error, setError] = useState('');

    if (!isOpen || !task) return null;

    const handleSubmit = async (e) => { 
        e.preventDefault(); 
        if (!logErro.trim()) { 
            setError('Por favor, cole a mensagem ou log de erro para o mentor.'); 
            return; 
        }

        try { 
            setLoading(true); 
            setError(''); 
            // Dispara a chamada REST para registrar o bloqueio e notificar o mentor 
            await blockAPI.acionarEstouTravado(task.id_progresso, logErro); 
            onSuccess(task.id_progresso); 
            onClose(); 
            setLogErro(''); 
        } catch (err) { 
            setError('Falha ao registrar bloqueio. Tente novamente.'); 
            console.error(err); 
        } finally { 
            setLoading(false); 
        } 
    };

    return ( 
        <div style={styles.overlay}>
        <div style={styles.modal}> 
            <h3>🚨 Sinalizar Bloqueio Técnico</h3> 
            <p><strong>Tarefa:</strong> {task.tarefa?.titulo || 'Configuração Técnica'}</p> 
            <p style={styles.subtitle}> 
                Cole abaixo a linha de comando, log de terminal ou print da mensagem de erro. 
                Seu Buddy/Mentor será notificado imediatamente para te ajudar. 
                </p> 
                
                {error && <div style={styles.errorMessage}>{error}</div>}

            <form onSubmit={handleSubmit}>
                <textarea
                    style={styles.textarea}
                    rows="5"
                    placeholder="Ex: Error: Permission denied (publickey) on git clone... ou Docker daemon not running"
                    value={logErro}
                    onChange={(e) => setLogErro(e.target.value)}
            />

            <div style={styles.actions}>
                <button type="button" onClick={onClose}  style={styles.cancelBtn} disabled={loading}>
                    Cancelar
                </button>
                <button type="submit" style={styles.submitBtn} disabled={loading}>
                    {loading ? 'Enviando...' : 'Confirmar e Notificar Mentor'}
                </button>
            </div>
            </form>
        </div>
        </div>
    ); 
}

// Estilos inline para o Modal (podem ser migrados para CSS/Tailwind) 
const styles = { 
    overlay: { 
        position: 'fixed', 
        top: 0, 
        left: 0, 
        right: 0, 
        bottom: 0, 
        backgroundColor: 'rgba(0, 0, 0, 0.6)', 
        display: 'flex', alignItems: 'center', justifyContent: 'center', 
        zIndex: 1000, 
    }, 
    modal: { 
        backgroundColor: '#fff', 
        borderRadius: '10px', 
        padding: '24px', 
        width: '100%', 
        maxWidth: '500px', 
        boxShadow: '0 4px 20px rgba(0,0,0,0.15)', 
    }, 
    subtitle: { 
        fontSize: '0.9rem', 
        color: '#666', marginBottom: '16px' 
    }, 
    textarea: { 
        width: '100%', 
        padding: '12px', 
        borderRadius: '6px', 
        border: '1px solid #ccc', 
        fontFamily: 'monospace', 
        fontSize: '0.85rem', 
        resize: 'vertical', marginBottom: '16px', boxSizing: 'border-box' 
    }, 
    actions: { 
        display: 'flex', justifyContent: 'flex-end', gap: '12px' 
    }, 
    cancelBtn: { 
        padding: '8px 16px', border: '1px solid #ccc', borderRadius: '6px', cursor: 'pointer', background: '#f5f5f5' 
    }, 
    submitBtn: { 
        padding: '8px 16px', border: 'none', borderRadius: '6px', cursor: 'pointer', background: '#dc3545', color: '#fff', fontWeight: 'bold' 
    }, 
    errorMessage: { 
        color: '#dc3545', marginBottom: '12px', fontSize: '0.85rem' 
    } 
};
