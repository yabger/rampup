import axios from 'axios'; 

// 1. Instância principal conectada ao backend FastAPI 

const api = axios.create({ 
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000', 
    headers: { 
        'Content-Type': 'application/json', 
    }, 
});

// 2. Interceptor para injetar o Token JWT automaticamente em todas as requisições 

api.interceptors.request.use( 
    (config) => { 
        const token = localStorage.getItem('rampup_token'); 
        if (token) { 
            config.headers.Authorization = `Bearer ${token}`; 
        } 
        return config; 
    }, 
    (error) => { return Promise.reject(error); } 
);

// ========================================== 
// MÓDULO 1: AUTENTICAÇÃO E USUÁRIOS
// ========================================== 

export const authAPI = { 
    login: async (email, senha) => { 
        const response = await api.post('/api/v1/auth/login', { email, senha }); 
        return response.data; 
    }, 
    cadastrar: async (usuarioData) => { 
        const response = await api.post('/api/v1/auth/cadastro', usuarioData); 
        return response.data; 
    }, 
};

// ========================================== 
// MÓDULO 2: TRILHAS E ONBOARDING (NOVATO) 
// ========================================== 

export const onboardingAPI = { 
    // Busca a lista de tarefas/checklist do novato 
    getTrilha: async (usuarioId) => {
         const response = await api.get(`/api/v1/onboarding/trilha/${usuarioId}`); 
         return response.data; 
        }, 
        // Atualiza o status de uma tarefa (ex: de PENDENTE para CONCLUIDO) 
    atualizarStatus: async (progressoId, status) => { 
        const response = await api.put(`/api/v1/onboarding/tasks/${progressoId}/status`, { status, }); 
        return response.data; 
    },
};

// ========================================== 
// MÓDULO 3: GESTÃO DE BLOQUEIOS ("ESTOU TRAVADO") 
// ========================================== 

export const blockAPI = { 
    // Acionado pelo botão "Estou Travado" no card da tarefa 
    acionarEstouTravado: async (progressoId, logErro) => { 
        const response = await api.post('/api/v1/blocks/stuck', { 
            id_progresso: progressoId, 
            log_erro: logErro, 
        }); 
        return response.data; 
    }, 
    // Acionado pelo Mentor (Buddy) para destravar o novato 
    destravarNovato: async (bloqueioId) => { 
        const response = await api.put(`/api/v1/blocks/${bloqueioId}/unblock`); 
        return response.data; 
    }, 
};

// ========================================== 
// MÓDULO 4: PAINEL DO MENTOR (BUDDY) 
// ========================================== 

export const mentorAPI = { 
    // Retorna os alertas de bloqueio ativos na fila do mentor 
    getDashboard: async (mentorId) => { 
        const response = await api.get(`/api/v1/mentor/dashboard/${mentorId}`); 
        return response.data; 
    }, 
}; 

export default api;