"""
Test básico del motor QuinielaAI.
Ejecutar: python -m pytest tests/ -v
"""
import sys
sys.path.insert(0, '..')

from app.services.motor_quiniela import QuinielaMotor, PartidoInput


def get_motor():
    return QuinielaMotor()


def test_probabilidades_implícitas():
    m = get_motor()
    # Cuota 2.0 → 50% probabilidad
    assert abs(m.calcular_prob_implícita(2.0) - 0.50) < 0.001
    # Cuota 4.0 → 25% probabilidad
    assert abs(m.calcular_prob_implícita(4.0) - 0.25) < 0.001


def test_normalizacion_elimina_overround():
    m = get_motor()
    # Con overround del 10%, la suma de probs implícitas sería 1.10
    p1, px, p2 = m.normalizar_probs(0.40, 0.35, 0.35)
    assert abs(p1 + px + p2 - 1.0) < 0.001


def test_detección_bomba_x_infravalorada():
    """La masa ignora el empate cuando debería estar al 30%+"""
    m = get_motor()
    partido = PartidoInput(
        id=1,
        local="Atlético",
        visitante="Betis",
        cuota_1=2.50,   # ~40% prob real
        cuota_x=3.10,   # ~32% prob real ← la masa solo marca 12%
        cuota_2=2.80,
        lae_pct_1=58.0,
        lae_pct_x=12.0,  # Masa ignora el empate
        lae_pct_2=30.0,
    )
    es_bomba, tipo, rent = m.detectar_bomba(
        partido, 0.385, 0.308, 0.307
    )
    assert es_bomba == True
    assert tipo is not None and "X" in tipo


def test_analisis_partido_completo():
    m = get_motor()
    partido = PartidoInput(
        id=5,
        local="Osasuna",
        visitante="Getafe",
        cuota_1=2.20,
        cuota_x=3.20,
        cuota_2=3.40,
        lae_pct_1=44.0,
        lae_pct_x=30.0,
        lae_pct_2=26.0,
    )
    resultado = m.analizar_partido(partido)
    assert resultado.signo in ["1", "X", "2"]
    assert 0 <= resultado.confianza <= 100
    assert abs(resultado.prob_1 + resultado.prob_x + resultado.prob_2 - 100.0) < 0.5


def test_analisis_jornada_15_partidos():
    m = get_motor()
    partidos = [
        PartidoInput(
            id=i, local=f"Local {i}", visitante=f"Visitante {i}",
            cuota_1=2.10, cuota_x=3.30, cuota_2=3.50,
            lae_pct_1=50.0, lae_pct_x=28.0, lae_pct_2=22.0,
        )
        for i in range(1, 16)
    ]
    resultado = m.analizar_jornada(65, partidos)
    assert resultado.jornada == 65
    assert len(resultado.partidos) == 15
    assert len(resultado.sistema_sugerido) == 15


if __name__ == "__main__":
    print("Ejecutando tests del motor QuinielaAI...\n")
    test_probabilidades_implícitas()
    print("✓ Probabilidades implícitas")
    test_normalizacion_elimina_overround()
    print("✓ Normalización overround")
    test_detección_bomba_x_infravalorada()
    print("✓ Detección bomba X infravalorada")
    test_analisis_partido_completo()
    print("✓ Análisis partido completo")
    test_analisis_jornada_15_partidos()
    print("✓ Análisis jornada 15 partidos")
    print("\n✅ Todos los tests pasan. Motor operativo.")
