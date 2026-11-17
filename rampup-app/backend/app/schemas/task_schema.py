from datetime import datetime 
from typing import Optional, List 
from pydantic import BaseModel, ConfigDict 
from app.models.task import PeriodoOnboarding, StatusTarefa

# --- SCHEMAS DE TAREFA ---
class TarefaBase(BaseModel): 
    titulo: str 
    periodo: PeriodoOnboarding = PeriodoOnboarding.DIA_1 
    tempo_estimado_min: Optional[int] = 30 
    link_tutorial: Optional[str] = None 
    ordem: int = 1

class TarefaCreate(TarefaBase): 
    id_trilha: int

class TarefaResponse(TarefaBase): 
    id_tarefa: int 
    id_trilha: int 
    model_config = ConfigDict(from_attributes=True)

# --- SCHEMAS DE TRILHA ---
class TrilhaBase(BaseModel): 
    titulo_trilha: str 
    cargo_destino: str 
    descricao: Optional[str] = None

class TrilhaCreate(TrilhaBase): 
    pass

class TrilhaResponse(TrilhaBase): 
    id_trilha: int 
    tarefas: List[TarefaResponse] = [] 

    model_config = ConfigDict(from_attributes=True)

#--- SCHEMAS DE PROGRESSO DA TAREFA ---
class ProgressoTarefaUpdate(BaseModel): 
    status: StatusTarefa 

class ProgressoTarefaResponse(BaseModel): 
    id_progresso: int 
    id_usuario: int 
    id_tarefa: int 
    status: StatusTarefa 
    data_inicio: Optional[datetime] = None 
    data_conclusao: Optional[datetime] = None 
    tarefa: Optional[TarefaResponse] = None 


    model_config = ConfigDict(from_attributes=True)