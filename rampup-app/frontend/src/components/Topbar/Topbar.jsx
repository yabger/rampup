import React from 'react';
import styles from './Topbar.module.css';

/**
 * Barra superior compartilhada.
 * section: "Espaço do mentor", page: "Alertas de bloqueio", nome, papel: "Mentor (Buddy)"
 */
export default function Topbar({ section, page, nome, papel }) {
    const inicial = (nome || '?').charAt(0).toUpperCase();

    return (
        <header className={styles.topbar}>
            <div className={styles.breadcrumb}>
                <span>{section}</span>
                <span aria-hidden="true" className={styles.separator}>/</span>
                <span className={styles.current}>{page}</span>
            </div>
            <div className={styles.user}>
                <span className={styles.avatar}>{inicial}</span>
                <div className={styles.userInfo}>
                    <span className={styles.userName}>{nome}</span>
                    <span className={styles.userRole}>{papel}</span>
                </div>
            </div>
        </header>
    );
}
