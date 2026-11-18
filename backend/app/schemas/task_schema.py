from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.models.task import PeriodoOnboarding, StatusTarefa
from app.schemas.user_schema import UsuarioResponse


class TarefaResponse(BaseModel):
    id_tarefa: int
    id_trilha: int
    titulo: str
    descricao: str | None = None
    periodo: PeriodoOnboarding
    tempo_estimado_min: int
    link_tutorial: str | None = None
    ordem: int
    model_config = ConfigDict(from_attributes=True)


class ProgressoTarefaUpdate(BaseModel):
    status: StatusTarefa


class ProgressoTarefaResponse(BaseModel):
    id_progresso: int
    id_usuario: int
    id_tarefa: int
    status: StatusTarefa
    data_inicio: datetime
    data_conclusao: datetime | None = None
    tarefa: TarefaResponse
    usuario: UsuarioResponse | None = None
    model_config = ConfigDict(from_attributes=True)


class ProgressoResumo(BaseModel):
    total_tarefas: int
    concluidas: int
    travadas: int
    percentual_conclusao: int
