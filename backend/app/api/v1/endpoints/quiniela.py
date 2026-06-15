from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime

from app.schemas.quiniela import (
    AnalisisJornadaRequest,
    AnalisisJornadaResponse,
    PartidoAnalisisSchema,
    WaitlistRequest,
    WaitlistResponse,
)
from app.services.motor_quiniela import motor, PartidoInput

router = APIRouter(prefix="/quiniela", tags=["quiniela"])


# ─── Análisis de jornada ─────────────────────────────────────────────────────

@router.post(
    "/analizar",
    response_model=AnalisisJornadaResponse,
    summary="Analizar una jornada completa",
    description="""
    Recibe los datos de una jornada (cuotas + porcentajes LAE)
    y devuelve el análisis completo: probabilidades, bombazos,
    rentabilidad esperada y sistema sugerido.
    
    Requiere suscripción Pro o Elite.
    """
)
async def analizar_jornada(
    request: AnalisisJornadaRequest,
    # user = Depends(require_pro_subscription)  # TODO: activar auth
):
    # Convertir schemas a objetos del motor
    partidos_input = [
        PartidoInput(
            id=p.id,
            local=p.local,
            visitante=p.visitante,
            cuota_1=p.cuota_1,
            cuota_x=p.cuota_x,
            cuota_2=p.cuota_2,
            lae_pct_1=p.lae_pct_1,
            lae_pct_x=p.lae_pct_x,
            lae_pct_2=p.lae_pct_2,
            es_derbi=p.es_derbi,
            jornada_num=request.jornada,
        )
        for p in request.partidos
    ]

    # Ejecutar motor
    resultado = motor.analizar_jornada(request.jornada, partidos_input)

    # Serializar respuesta
    partidos_resp = [
        PartidoAnalisisSchema(**p.__dict__)
        for p in resultado.partidos
    ]

    return AnalisisJornadaResponse(
        jornada=resultado.jornada,
        partidos=partidos_resp,
        rentabilidad_total=resultado.rentabilidad_total,
        num_bombas=resultado.num_bombas,
        resumen=resultado.resumen,
        sistema_sugerido=resultado.sistema_sugerido,
        generado_en=datetime.utcnow(),
    )


@router.get(
    "/jornada/{numero}/preview",
    summary="Preview público de la jornada (Free)",
    description="Devuelve datos básicos sin análisis detallado. Disponible para todos."
)
async def preview_jornada(numero: int):
    """Vista pública — sin análisis, solo los partidos."""
    # TODO: obtener de Supabase
    return {
        "jornada": numero,
        "disponible": True,
        "num_partidos": 15,
        "analisis_disponible": "Pro y Elite",
        "mensaje": "Suscríbete a Pro para ver el análisis completo y los bombazos."
    }


@router.get(
    "/historico",
    summary="Histórico de resultados públicos",
)
async def historico(limite: int = 10):
    """
    Últimas jornadas con resultado real vs sistema.
    Público — es nuestra credibilidad.
    """
    # TODO: obtener de Supabase
    return {
        "jornadas": [],
        "track_record": {
            "total_jornadas": 65,
            "mejor_jornada": {"numero": 59, "aciertos_pct": 86},
            "peor_jornada":  {"numero": 64, "aciertos_pct": 43},
            "media": 68.2,
        }
    }


# ─── Waitlist ────────────────────────────────────────────────────────────────

@router.post(
    "/waitlist",
    response_model=WaitlistResponse,
    summary="Unirse a la lista de espera",
)
async def unirse_waitlist(request: WaitlistRequest):
    """Registra email en la waitlist. Sin auth requerida."""
    # TODO: guardar en Supabase tabla waitlist
    # Por ahora devuelve respuesta mock
    return WaitlistResponse(
        ok=True,
        mensaje="Apuntado. Recibirás acceso anticipado antes del inicio de temporada.",
        posicion=42,  # TODO: contar reales
    )
