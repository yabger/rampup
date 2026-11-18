import React from 'react';
import Sidebar from '../Sidebar/Sidebar';
import Topbar from '../Topbar/Topbar';
import styles from './AppLayout.module.css';

/**
 * Casco comum: menu lateral + barra superior + área de conteúdo (children).
 */
export default function AppLayout({ menu, onLogout, topbar, children }) {
    return (
        <div className={styles.app}>
            <Sidebar items={menu} onLogout={onLogout} />
            <div className={styles.content}>
                <Topbar {...topbar} />
                {children}
            </div>
        </div>
    );
}
