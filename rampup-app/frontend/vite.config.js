import { defineConfig } from 'vite'; 
import react from '@vitejs/plugin-react'; 

// Configuração base do Vite para React 

export default defineConfig({ 
    plugins: [react()], 
    server: { port: 5173, // Define a porta padrão de desenvolvimento 
    }, 
});