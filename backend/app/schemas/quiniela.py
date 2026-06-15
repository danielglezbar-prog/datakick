from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PartidoInputSchema(BaseModel):
    id: int
    local: str
    visitante: str
    cuota_1: float = Field(gt=1.0, description="Cuota decimal victoria local")
    cuota_x: float = Field(gt=1.0, description="Cuota decimal empate")
    cuota_2: float = Field(gt=1.0, description="Cuota decimal victoria visitante")
    lae_pct_1: float = Field(ge=0, le=100)
    lae_pct_x: float = Field(ge=0, le=100)
    lae_pct_2: float = Field(ge=0, le=100)
    es_derbi: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "local": "Real Madrid",
                "visitante": "Barcelona",
                "cuota_1": 2.10,
                "cuota_x": 3.40,
                "cuota_2": 3.20,
                "lae_pct_1": 58.2,
                "lae_pct_x": 24.1,
                "lae_pct_2": 17.7,
                "es_derbi": True
            }
        }


class AnalisisJornadaRequest(BaseModel):
    jornada: int = Field(ge=1, le=100)
    partidos: list[PartidoInputSchema] = Field(min_length=1, max_length=15)


class PartidoAnalisisSchema(BaseModel):
    id: int
    local: str
    visitante: str
    prob_1: float
    prob_x: float
    prob_2: float
    lae_pct_1: float
    lae_pct_x: float
    lae_pct_2: float
    signo: str
    confianza: float
    valor_1: float
    valor_x: float
    valor_2: float
    es_bomba: bool
    bomba_tipo: Optional[str]
    rentabilidad_esperada: float
    notas: list[str]


class AnalisisJornadaResponse(BaseModel):
    jornada: int
    partidos: list[PartidoAnalisisSchema]
    rentabilidad_total: float
    num_bombas: int
    resumen: str
    sistema_sugerido: list[str]
    generado_en: datetime = Field(default_factory=datetime.utcnow)


class WaitlistRequest(BaseModel):
    email: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    nombre: Optional[str] = None

class WaitlistResponse(BaseModel):
    ok: bool
    mensaje: str
    posicion: int


class SubscriptionCheckResponse(BaseModel):
    activa: bool
    plan: Optional[str]   # "free", "pro", "elite"
    valid_until: Optional[datetime]
