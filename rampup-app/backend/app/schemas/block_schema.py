from datetime import datetime 
from typing import Optional 
from pydantic import BaseModel, ConfigDict 
from app.models.block import StatusBloqueio 
from app.schemas.user_schema import UsuarioResponse 
from app.schemas.task_schema import ProgressoTarefaResponse

# --- SCHEMAS DO BOTÃO 'ESTOU TRAVADO' --- 

class BloqueioCreate(BaseModel): 
    id_progresso: int 
    log_erro: str 

# Stacktrace colado pelo novato 
class BloqueioResponse(BaseModel): 
    id_bloqueio: int 
    id_progresso: int 
    id_mentor: Optional[int] = None 
    log_erro: str 
    status_bloqueio: StatusBloqueio 
    data_bloqueio: datetime 
    data_resolucao: Optional[datetime] = None 
    progresso_tarefa: Optional[ProgressoTarefaResponse] = None 
    mentor: Optional[UsuarioResponse] = None 
    model_config = ConfigDict(from_attributes=True)

# --- SCHEMAS DE VÍNCULO DE MENTORIA --- 
class VinculoMentoriaCreate(BaseModel): 
    id_novato: int 
    id_mentor: int

class VinculoMentoriaResponse(BaseModel): 
    id_vinculo: int 
    id_novato: int 
    id_mentor: int 
    data_inicio: datetime 
    novato: Optional[UsuarioResponse] = None 
    mentor: Optional[UsuarioResponse] = None 
    model_config = ConfigDict(from_attributes=True)

# \--- SCHEMAS DE DOCUMENTAÇÃO OBSOLETA --- 
class DocumentacaoObsoletaCreate(BaseModel): 
    id_tarefa: int 
    trecho_desatualizado: str 
    sugestao_correcao: Optional[str] = None

class DocumentacaoObsoletaResponse(DocumentacaoObsoletaCreate): 
    id_report: int 
    id_usuario: int 
    data_registro: datetime 
    model_config = ConfigDict(from_attributes=True)