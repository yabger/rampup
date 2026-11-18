import React, { useState } from 'react';
import { authAPI } from '../../api/axios_config';
import styles from './LoginScreen.module.css';

export default function LoginScreen({ onLoginSuccess }) {
    const [email, setEmail] = useState('');
    const [senha, setSenha] = useState('');
    const [mostrarSenha, setMostrarSenha] = useState(false);
    const [loading, setLoading] = useState(false);
    const [erro, setErro] = useState('');
    const [ativo, setAtivo] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setErro('');

        // MOCKUP: entrada livre. Tenta a API; se falhar (ou campos vazios),
        // entra com um usuário simulado. Perfil "mentor" se o e-mail contiver bruno/mentor.
        try {
            if (!email || !senha) throw new Error('mock');
            const response = await authAPI.login(email, senha);
            localStorage.setItem('rampup_token', response.access_token);
            localStorage.setItem('rampup_user', JSON.stringify(response.usuario));
            onLoginSuccess(response.usuario);
        } catch (error) {
            const mentor = /bruno|mentor|buddy|mariana/i.test(email);
            const usuario = mentor
                ? { id_usuario: 2, nome: 'Bruno Santos', tipo_perfil: 'BUDDY' }
                : { id_usuario: 1, nome: 'Lucas Rocha', tipo_perfil: 'NOVATO' };
            localStorage.setItem('rampup_user', JSON.stringify(usuario));
            onLoginSuccess(usuario);
        } finally {
            setLoading(false);
        }
    };

    // Preenchimento rápido das personas da PoC (seed.py)
    const preencherCredenciais = (id, emailTest, senhaTest) => {
        setEmail(emailTest);
        setSenha(senhaTest);
        setAtivo(id);
        setErro('');
    };

    const demos = [
        { id: 'lucas', label: 'Lucas · Novato', email: 'lucas.rocha@empresa.com' },
        { id: 'bruno', label: 'Bruno · Mentor', email: 'bruno.santos@empresa.com' },
    ];

    return (
        <div className={styles.login}>
            {/* Painel de marca */}
            <section className={styles.brand}>
                <div className={styles.logo}>
                    <svg className={styles.logoMark} width="48" height="48" viewBox="0 0 64 64" role="img" aria-label="Símbolo RampUp">
                        <rect width="64" height="64" rx="10" fill="#ffffff" />
                        <path d="M22 47V18H35a8.5 8.5 0 0 1 0 17H22" fill="none" stroke="#1A2C5B" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M34 37l10.5 11" fill="none" stroke="#0047AB" strokeWidth="6" strokeLinecap="round" />
                    </svg>
                    <span className={styles.logoText}>
                        Ramp<span className={styles.logoAccent}>Up</span>
                    </span>
                </div>

                <div className={styles.brandCopy}>
                    <span className={styles.eyebrow}>Hub de onboarding técnico</span>
                    <h1 className={styles.headline}>Sua jornada de integração, em um só lugar.</h1>
                </div>
            </section>

            {/* Formulário */}
            <section className={styles.formSide}>
                <div className={styles.card}>
                    <div className={styles.cardHeader}>
                        <h2 className={styles.title}>Que bom ter você aqui</h2>
                        <p className={styles.subtitle}>Entre para continuar sua jornada de integração.</p>
                    </div>

                    {erro && <div role="alert" className={styles.error}>{erro}</div>}

                    <form onSubmit={handleSubmit} className={styles.form}>
                        <div className={styles.inputGroup}>
                            <label htmlFor="email" className={styles.label}>E-mail</label>
                            <input
                                id="email"
                                className={styles.field}
                                type="email"
                                autoComplete="username"
                                placeholder="ex: lucas.rocha@empresa.com"
                                value={email}
                                onChange={(e) => { setEmail(e.target.value); setAtivo(''); }}
                            />
                        </div>

                        <div className={styles.inputGroup}>
                            <label htmlFor="senha" className={styles.label}>Senha</label>
                            <div className={styles.passwordWrap}>
                                <input
                                    id="senha"
                                    className={`${styles.field} ${styles.fieldPassword}`}
                                    type={mostrarSenha ? 'text' : 'password'}
                                    autoComplete="current-password"
                                    placeholder="Digite sua senha"
                                    value={senha}
                                    onChange={(e) => setSenha(e.target.value)}
                                />
                                <button
                                    type="button"
                                    className={styles.eye}
                                    aria-label="Mostrar ou ocultar senha"
                                    onClick={() => setMostrarSenha(!mostrarSenha)}
                                >
                                    {mostrarSenha ? 'Ocultar' : 'Mostrar'}
                                </button>
                            </div>
                        </div>

                        <button type="submit" className={styles.btn} disabled={loading}>
                            {loading ? 'Autenticando...' : 'Entrar na plataforma'}
                        </button>
                    </form>

                    {/* ATALHOS PARA APRESENTAÇÃO DO PROJETO INTEGRADOR */}
                    <div className={styles.quick}>
                        <span className={styles.label}>Acessos demonstrativos</span>
                        <div className={styles.chips}>
                            {demos.map((d) => (
                                <button
                                    key={d.id}
                                    type="button"
                                    className={styles.chip}
                                    aria-pressed={ativo === d.id}
                                    onClick={() => preencherCredenciais(d.id, d.email, '123456')}
                                >
                                    {d.label}
                                </button>
                            ))}
                        </div>
                        <span className={styles.hint}>Senha de todos: 123456</span>
                    </div>
                </div>
            </section>
        </div>
    );
}
