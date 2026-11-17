import React, { useState } from 'react'; 
import { authAPI } from '../api/axios_config'; 

export default function LoginScreen({ onLoginSuccess }) { 
    const [email, setEmail] = useState(''); 
    const [senha, setSenha] = useState(''); 
    const [loading, setLoading] = useState(false); 
    const [erro, setErro] = useState('');

    const handleSubmit = async (e) => { 
        e.preventDefault(); if (!email || !senha) { 
            setErro('Por favor, preencha todos os campos.'); 
            return; 
        }

        try { 
            setLoading(true); 
            setErro('');
            // Dispara a chamada REST POST /api/v1/auth/login 
            const response = await authAPI.login(email, senha);
            // Armazena o token JWT e os dados do usuário no localStorage 
            localStorage.setItem('rampup_token', response.access_token); 
            localStorage.setItem('rampup_user', JSON.stringify(response.usuario));

            // Notifica o App.jsx que o login foi bem-sucedido 
            onLoginSuccess(response.usuario);
        } catch (error) { 
            console.error('Erro ao fazer login:', error); 
            setErro(error.response?.data?.detail || 'E-mail ou senha incorretos.'); 
        } finally { 
            setLoading(false); 
        }
    };

    // Função auxiliar para preenchimento rápido das personas da PoC (seed.py)
    const preencherCredenciais = (emailTest, senhaTest) => { 
        setEmail(emailTest); 
        setSenha(senhaTest); 
        setErro(''); 
    };

    return ( 
        <div style={styles.container}> 
        <div style={styles.card}> 
            <h1 style={styles.logoContainer}> 🚀 RampUp</h1>
            <p style={styles.logoSubtext}>Hub Interativo de Onboarding Técnico</p> 
            </div>
            {erro && <div style={styles.errorMessage}>{erro}</div>}

            <form onSubmit={handleSubmit} style={styles.form}>
                <div style={styles.inputGroup}>
                <label style={styles.label}>E-mail Corporativo</label>
                <input
                type="email"
                style={styles.input}
                placeholder="ex: lucas.rocha@empresa.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                />
            </div>

            <div style={styles.inputGroup}>
                <label style={styles.label}>Senha</label>
                <input
                type="password"
                style={styles.input}
                placeholder="Digite sua senha"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
                />
            </div>
            <button type="submit" style={styles.btnLogin} disabled={loading}>
                {loading ? 'Autenticando...' : 'Entrar no Sistema'}
            </button>
            </form>

            {/* ATALHOS PARA APRESENTAÇÃO DO PROJETO INTEGRADOR */}
            <div style={styles.quickAccess}>
                <p style={styles.quickTitle}>💡 Atalhos de Teste para a Banca:</p>
                <div style={styles.quickButtons}>
                    <button
                        type="button"
                        onClick={() => preencherCredenciais('lucas.rocha@empresa.com', '123456')}
                        style={styles.quickBtnNovato}
                    >
                        👤 Novato (Lucas)
                    </button>
                    <button
                        type="button"
                        onClick={() => preencherCredenciais('bruno.santos@empresa.com', '123456')} 
                        style={styles.quickBtnMentor}
                    >
                        🛡️ Mentor (Bruno)
                    </button>
                </div>
            </div>
        </div>
    );
}

// Estilos visuais 
const styles = { container: { display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', backgroundColor: '#f4f6f9', fontFamily: 'sans-serif', padding: '20px' }, card: { backgroundColor: '#fff', borderRadius: '12px', padding: '36px', width: '100%', maxWidth: '420px', boxShadow: '0 8px 24px rgba(0,0,0,0.08)' }, logoContainer: { textAlign: 'center', marginBottom: '24px' }, logoTitle: { margin: '0', color: '#007bff', fontSize: '2rem' }, logoSubtext: { color: '#666', fontSize: '0.9rem', marginTop: '4px' }, form: { display: 'flex', flexDirection: 'column', gap: '16px' }, inputGroup: { display: 'flex', flexDirection: 'column', gap: '6px' }, label: { fontSize: '0.85rem', fontWeight: 'bold', color: '#333' }, input: { padding: '10px 14px', borderRadius: '6px', border: '1px solid #ccc', fontSize: '0.95rem' }, btnLogin: { padding: '12px', borderRadius: '6px', border: 'none', backgroundColor: '#007bff', color: '#fff', fontSize: '1rem', fontWeight: 'bold', cursor: 'pointer', marginTop: '8px' }, errorMessage: { backgroundColor: '#f8d7da', color: '#721c24', padding: '10px', borderRadius: '6px',
 fontSize:'0.85rem',
 marginBottom: '16px',
 border: '1px solid #f5c6cb'
 },
 quickAccess:
 {
 marginTop:
 '28px',
 paddingTop: '16px',
 borderTop: '1px solid #eee',
 textAlign: 'center'
 },
 quickTitle: { fontSize: '0.8rem', color: '#666', marginBottom: '8px' },
 quickButtons: { display: 'flex', gap: '8px', justifyContent: 'center' },
 quickBtnNovato: { padding: '6px 12px', border: '1px solid #007bff', background: '#e7f1ff', color: '#007bff', borderRadius: '4px', cursor: 'pointer', fontSize: '0.8rem', fontWeight: 'bold' },
 quickBtnMentor: { padding: '6px 12px', border: '1px solid #28a745', background: '#e6f4ea', color: '#28a745', borderRadius: '4px', cursor: 'pointer', fontSize: '0.8rem', fontWeight: 'bold' },
 };