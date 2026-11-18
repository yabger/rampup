import React, { useState, useEffect } from 'react';
import LoginScreen from './pages/LoginScreen/LoginScreen';
import NovatoDashboard from './pages/NovatoDashboard/NovatoDashboard';
import MentorDashboard from './pages/MentorDashboard/MentorDashboard';

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
    // Novato: a dashboard já traz o próprio menu lateral e cabeçalho
    if (usuario.tipo_perfil === 'NOVATO') {
        return <NovatoDashboard usuarioId={usuario.id_usuario} usuario={usuario} onLogout={handleLogout} />;
    }
    // Demais perfis (mentor/buddy/tech lead): painel do mentor, que também traz menu e cabeçalho próprios
    return <MentorDashboard usuarioId={usuario.id_usuario} usuario={usuario} onLogout={handleLogout} />;
}