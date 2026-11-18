import React, { useState } from 'react'; 
import { blockAPI } from '../../api/axios_config';
import styles from './StuckModel.module.css';

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
        <div className={styles.overlay}>
        <div className={styles.modal}> 
            <h3>🚨 Sinalizar Bloqueio Técnico</h3> 
            <p><strong>Tarefa:</strong> {task.tarefa?.titulo || 'Configuração Técnica'}</p> 
            <p className={styles.subtitle}> 
                Cole abaixo a linha de comando, log de terminal ou print da mensagem de erro. 
                Seu Buddy/Mentor será notificado imediatamente para te ajudar. 
                </p> 
                
                {error && <div className={styles.errorMessage}>{error}</div>}

            <form onSubmit={handleSubmit}>
                <textarea
                    className={styles.textarea}
                    rows="5"
                    placeholder="Ex: Error: Permission denied (publickey) on git clone... ou Docker daemon not running"
                    value={logErro}
                    onChange={(e) => setLogErro(e.target.value)}
            />

            <div className={styles.actions}>
                <button type="button" onClick={onClose}  className={styles.cancelBtn} disabled={loading}>
                    Cancelar
                </button>
                <button type="submit" className={styles.submitBtn} disabled={loading}>
                    {loading ? 'Enviando...' : 'Confirmar e Notificar Mentor'}
                </button>
            </div>
            </form>
        </div>
        </div>
    ); 
}
