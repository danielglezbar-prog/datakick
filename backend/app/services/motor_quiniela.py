"""
Motor analítico Datakick — QuinielaAI Engine
============================================
Convierte probabilidades de casas de apuestas y porcentajes LAE
en señales de valor (bombazos) y rentabilidad esperada.

16 reglas de análisis derivadas de 65+ jornadas de track record.
"""

from dataclasses import dataclass, field
from typing import Optional
import math


# ─── Modelos de datos ────────────────────────────────────────────────────────

@dataclass
class PartidoInput:
    """Datos de entrada por partido."""
    id: int
    local: str
    visitante: str

    # Cuotas de la casa de apuestas (decimal)
    cuota_1: float   # Victoria local
    cuota_x: float   # Empate
    cuota_2: float   # Victoria visitante

    # Porcentajes LAE (% de jugadores que marcan cada signo)
    lae_pct_1: float
    lae_pct_x: float
    lae_pct_2: float

    # Datos adicionales opcionales
    racha_local: Optional[str] = None   # "WDWLW" últimos 5
    racha_visitante: Optional[str] = None
    es_derbi: bool = False
    jornada_num: Optional[int] = None


@dataclass
class PartidoAnalisis:
    """Resultado del análisis por partido."""
    id: int
    local: str
    visitante: str

    # Probabilidades implícitas (sin margen)
    prob_1: float
    prob_x: float
    prob_2: float

    # Porcentajes LAE
    lae_pct_1: float
    lae_pct_x: float
    lae_pct_2: float

    # Signo recomendado
    signo: str          # "1", "X", "2"
    confianza: float    # 0-100

    # Valor esperado
    valor_1: float      # (prob_real - prob_masa) normalizado
    valor_x: float
    valor_2: float

    # Flags de análisis
    es_bomba: bool = False
    bomba_tipo: Optional[str] = None   # "X_infravalorada", "1_contrarian", etc.
    rentabilidad_esperada: float = 0.0
    notas: list[str] = field(default_factory=list)


@dataclass
class AnalisisJornada:
    """Análisis completo de una jornada."""
    jornada: int
    partidos: list[PartidoAnalisis]
    rentabilidad_total: float
    num_bombas: int
    resumen: str
    sistema_sugerido: list[str]   # Lista de signos para el sistema


# ─── Motor principal ─────────────────────────────────────────────────────────

class QuinielaMotor:
    """
    Motor analítico QuinielaAI.

    Compara probabilidades reales (derivadas de cuotas) vs distribución
    de la masa (LAE) para identificar ineficiencias de mercado.
    """

    # Umbrales de detección de bombazos (calibrados con 65 jornadas)
    UMBRAL_BOMBA_FUERTE = 15.0    # Diferencia prob_real vs lae > 15pp
    UMBRAL_BOMBA_MEDIA  = 8.0     # Diferencia > 8pp
    UMBRAL_CONFIANZA    = 60.0    # Confianza mínima para recomendar

    def calcular_prob_implícita(self, cuota: float) -> float:
        """Probabilidad implícita desde cuota decimal."""
        if cuota <= 0:
            return 0.0
        return 1.0 / cuota

    def normalizar_probs(self, p1: float, px: float, p2: float) -> tuple[float, float, float]:
        """
        Elimina el margen de la casa y normaliza a 100%.
        El margen (overround) suele ser 5-8% en quinielas.
        """
        total = p1 + px + p2
        if total == 0:
            return (0.333, 0.333, 0.334)
        return (p1 / total, px / total, p2 / total)

    def calcular_valor(self, prob_real: float, prob_masa: float) -> float:
        """
        Valor = (prob_real - prob_masa).
        Positivo = infravalorado por la masa (oportunidad).
        Negativo = sobrevalorado por la masa (evitar).
        """
        return (prob_real - prob_masa / 100) * 100

    def detectar_bomba(self, partido: PartidoInput,
                       prob_1: float, prob_x: float, prob_2: float) -> tuple[bool, Optional[str], float]:
        """
        Aplica las 16 reglas de detección de bombazos.
        Retorna (es_bomba, tipo_bomba, rentabilidad_esperada).
        """
        lae_1 = partido.lae_pct_1
        lae_x = partido.lae_pct_x
        lae_2 = partido.lae_pct_2

        # Diferencias prob_real vs masa
        diff_1 = self.calcular_valor(prob_1, lae_1)
        diff_x = self.calcular_valor(prob_x, lae_x)
        diff_2 = self.calcular_valor(prob_2, lae_2)

        # REGLA 1: X muy infravalorada — masa ignora el empate
        if diff_x > self.UMBRAL_BOMBA_FUERTE and lae_x < 20:
            rent = diff_x * 0.35  # Factor de escala calibrado
            return True, "X_infraval_masa", rent

        # REGLA 2: Favorito local muy sobrevalorado por la masa
        if diff_1 < -self.UMBRAL_BOMBA_MEDIA and lae_1 > 60 and prob_2 > 0.30:
            rent = abs(diff_1) * 0.28
            return True, "1_sobrevalorado", rent

        # REGLA 3: Visitante sorpresa — masa ignora al equipo de fuera
        if diff_2 > self.UMBRAL_BOMBA_FUERTE and lae_2 < 15 and prob_2 > 0.35:
            rent = diff_2 * 0.40
            return True, "2_contrarian", rent

        # REGLA 4: Partido equilibrado que la masa polariza
        if (abs(prob_1 - prob_2) < 0.08 and     # Partidos muy igualados
            abs(lae_1 - lae_2) > 20):             # Pero la masa se decanta fuerte
            signo = "1" if lae_2 > lae_1 else "2"
            rent = abs(lae_1 - lae_2) * 0.20
            return True, f"{signo}_equilibrio_ignorado", rent

        # REGLA 5: Derbi — la masa exagera siempre al local
        if partido.es_derbi and lae_1 > 55 and prob_x > 0.28:
            return True, "X_derbi", 8.5

        # Sin bomba detectada
        return False, None, 0.0

    def calcular_confianza(self, prob_real: float, lae_pct: float,
                            es_bomba: bool) -> float:
        """Confianza 0-100 en la recomendación."""
        base = prob_real * 100
        bonus_bomba = 15 if es_bomba else 0
        penalizacion_masa = max(0, (lae_pct - 60) * 0.3)  # Si masa muy concentrada, menos confianza
        return min(95, max(20, base + bonus_bomba - penalizacion_masa))

    def signo_recomendado(self, p1: float, px: float, p2: float,
                          bomba_tipo: Optional[str]) -> str:
        """Signo recomendado combinando prob_real y señal de bomba."""
        if bomba_tipo:
            # El bomba_tipo ya indica qué signo jugar
            if bomba_tipo.startswith("X"):
                return "X"
            elif bomba_tipo.startswith("2"):
                return "2"
            elif bomba_tipo.startswith("1"):
                return "1"
        # Sin bomba: signo con mayor probabilidad real
        max_prob = max(p1, px, p2)
        if max_prob == p1: return "1"
        if max_prob == px: return "X"
        return "2"

    def analizar_partido(self, partido: PartidoInput) -> PartidoAnalisis:
        """Análisis completo de un partido."""
        # Probabilidades implícitas brutas
        pi_1 = self.calcular_prob_implícita(partido.cuota_1)
        pi_x = self.calcular_prob_implícita(partido.cuota_x)
        pi_2 = self.calcular_prob_implícita(partido.cuota_2)

        # Normalizar (eliminar overround)
        p1, px, p2 = self.normalizar_probs(pi_1, pi_x, pi_2)

        # Valores vs masa
        v1 = self.calcular_valor(p1, partido.lae_pct_1)
        vx = self.calcular_valor(px, partido.lae_pct_x)
        v2 = self.calcular_valor(p2, partido.lae_pct_2)

        # Detección de bomba
        es_bomba, bomba_tipo, rent_esp = self.detectar_bomba(partido, p1, px, p2)

        # Signo y confianza
        signo = self.signo_recomendado(p1, px, p2, bomba_tipo)
        prob_signo = {"1": p1, "X": px, "2": p2}[signo]
        confianza = self.calcular_confianza(prob_signo, partido.lae_pct_1, es_bomba)

        # Notas automáticas
        notas = []
        if v1 > 10:  notas.append(f"Local infravalorado por la masa (+{v1:.1f}pp)")
        if vx > 10:  notas.append(f"Empate infravalorado (+{vx:.1f}pp)")
        if v2 > 10:  notas.append(f"Visitante infravalorado (+{v2:.1f}pp)")
        if partido.lae_pct_1 > 70: notas.append("Masa muy concentrada en local — señal de alerta")
        if partido.es_derbi:       notas.append("Derbi — históricamente más empates de lo esperado")

        return PartidoAnalisis(
            id=partido.id,
            local=partido.local,
            visitante=partido.visitante,
            prob_1=round(p1 * 100, 1),
            prob_x=round(px * 100, 1),
            prob_2=round(p2 * 100, 1),
            lae_pct_1=partido.lae_pct_1,
            lae_pct_x=partido.lae_pct_x,
            lae_pct_2=partido.lae_pct_2,
            signo=signo,
            confianza=round(confianza, 1),
            valor_1=round(v1, 2),
            valor_x=round(vx, 2),
            valor_2=round(v2, 2),
            es_bomba=es_bomba,
            bomba_tipo=bomba_tipo,
            rentabilidad_esperada=round(rent_esp, 2),
            notas=notas,
        )

    def analizar_jornada(self, jornada: int,
                          partidos: list[PartidoInput]) -> AnalisisJornada:
        """Analiza una jornada completa de 15 partidos."""
        analizados = [self.analizar_partido(p) for p in partidos]

        bombas = [p for p in analizados if p.es_bomba]
        rent_total = sum(p.rentabilidad_esperada for p in analizados)
        sistema = [p.signo for p in analizados]

        resumen = (
            f"Jornada {jornada}: {len(bombas)} bombazos detectados. "
            f"Rentabilidad esperada del sistema: +{rent_total:.1f}%. "
            f"{'Jornada con valor alto.' if rent_total > 15 else 'Jornada con valor moderado.'}"
        )

        return AnalisisJornada(
            jornada=jornada,
            partidos=analizados,
            rentabilidad_total=round(rent_total, 2),
            num_bombas=len(bombas),
            resumen=resumen,
            sistema_sugerido=sistema,
        )


# Instancia global del motor (singleton)
motor = QuinielaMotor()
