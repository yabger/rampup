import React from 'react';
import styles from './Sidebar.module.css';

// Ícones do menu (stroke) por nome
const ICONS = {
    flag: 'M4 22V4 M4 4h13l-2 4 2 4H4',
    book: 'M4 19.5A2.5 2.5 0 0 1 6.5 17H20 M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z',
    bell: 'M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9 M13.7 21a2 2 0 0 1-3.4 0',
    logout: 'M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4 M16 17l5-5-5-5 M21 12H9',
};

function Icon({ name }) {
    return (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d={ICONS[name]} />
        </svg>
    );
}

/**
 * Menu lateral compartilhado.
 * items: [{ label, href, icon, current }]
 */
export default function Sidebar({ items = [], onLogout }) {
    return (
        <aside className={styles.side}>
            <div className={styles.logo}>
                <svg className={styles.logoMark} width="34" height="34" viewBox="0 0 64 64" role="img" aria-label="Símbolo RampUp">
                    <rect width="64" height="64" rx="10" fill="#FFFFFF" />
                    <path d="M22 47V18H35a8.5 8.5 0 0 1 0 17H22" fill="none" stroke="#1A2C5B" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" />
                    <path d="M34 37l10.5 11" fill="none" stroke="#0047AB" strokeWidth="6" strokeLinecap="round" />
                </svg>
                <span className={styles.logoText}>Ramp<span className={styles.logoAccent}>Up</span></span>
            </div>

            <nav aria-label="Principal" className={styles.nav}>
                {items.map((item) => (
                    <a key={item.href} className={styles.item} href={item.href} aria-current={item.current ? 'page' : undefined}>
                        <Icon name={item.icon} />
                        {item.label}
                    </a>
                ))}
            </nav>

            <div className={styles.footer}>
                <button type="button" className={styles.item} onClick={onLogout}>
                    <Icon name="logout" />
                    Sair
                </button>
            </div>
        </aside>
    );
}
