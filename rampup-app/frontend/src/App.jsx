import React, { useState, useEffect } from 'react';
import LoginScreen from './pages/LoginScreen';
import NovatoDashboard from './pages/NovatoDashboard';
import MentorDashboard from './pages/MentorDashboard';

export default function App() {
    const [usuario, setUsuario] = useState(null);

    // Recupera o usuário salvo no localStorage se a página for recarregada
    useEffect(() => {
        const savedUser = localStorage.getItem('rampup_user');
        if (savedUser) {
            try {
                setUsuario(JSON.parse(savedUser));
            } catch (e) {
                localStorage.removeItem('rampup_user');
            }
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('rampup_token');
        localStorage.removeItem('rampup_user');
        setUsuario(null);
    };

    // 1\. Se não houver usuário logado, exibe a Tela de Login
    if (!usuario) {
        return <LoginScreen onLoginSuccess={setUsuario} />;
    }
    // 2\. Se o usuário estiver logado, exibe o Header de perfil + a Dashboard correspondente
    return (
    <div>
        {/* Barra de controle superior */}
        <nav style={styles.navBar}>
            <div style={styles.navInfo}>
                <span style={styles.brand}>🚀 RampUp</span>
                <span style={styles.userBadge}>
                    Conectado como: <strong>{usuario.nome}</strong> ({usuario.tipo_perfil})
                    </span>
                </div>
                <button onClick={handleLogout} style={styles.btnLogout}>
                    🚪 Sair / Logout
                </button>
                </nav>
                {/* Roteamento dinâmico pelo perfil do usuário */}
                {usuario.tipo_perfil === 'NOVATO' ? (
                    <NovatoDashboard usuarioId={usuario.id_usuario} />
        ) : (
                    <MentorDashboard mentorId={usuario.id_usuario} />
                )}
                </div>
    );
}
const styles = {
    navBar: { background: '#1e293b', color: '#fff', padding: '12px 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }, navInfo: { display: 'flex', alignItems: 'center', gap: '16px' }, brand: { fontWeight: 'bold', fontSize: '1.2rem', color: '#38bdf8' }, userBadge: { fontSize: '0.9rem', color: '#cbd5e1' }, btnLogout: { background: '#ef4444', color: '#fff', border: 'none', padding: '6px 14px', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold', fontSize: '0.85rem' } };
