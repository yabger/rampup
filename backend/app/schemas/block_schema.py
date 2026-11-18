from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.models.block import StatusBloqueio
from app.schemas.task_schema import ProgressoTarefaResponse
from app.schemas.user_schema import UsuarioResponse


class BloqueioCreate(BaseModel):
    id_progresso: int
    log_erro: str = Field(min_length=1, max_length=20000)


class BloqueioResponse(BaseModel):
    id_bloqueio: int
    id_progresso: int
    id_mentor: int | None = None
    log_erro: str
    status_bloqueio: StatusBloqueio
    data_bloqueio: datetime
    data_resolucao: datetime | None = None
    progresso_tarefa: ProgressoTarefaResponse | None = None
    mentor: UsuarioResponse | None = None
    model_config = ConfigDict(from_attributes=True)
