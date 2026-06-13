import random
from motor_core import Jugador

# ---------------------------------------------------------------------------
# Bases de datos de nombres (parodia fútbol sudamericano)
# ---------------------------------------------------------------------------
NOMBRES = [
    "Lianel", "Arturo", "Chupete", "Ronaldiño", "Marcelho",
    "Robiniho", "Kaká", "Riquelme", "Palermo", "Aimar",
    "Tevéz", "Higuaín", "Varguitas", "Falcao", "Cuadrabo",
]

APELLIDOS = [
    "Messido", "Vidal", "Suárez", "Cavaniño", "Guerrero",
    "Farfánez", "Sánchulo", "Rodriguito", "Herrerita", "Zapatazo",
    "Cuevitas", "Flores", "Ramírez", "Moreno", "Díazco",
]

# ---------------------------------------------------------------------------
# Constantes de rango
# ---------------------------------------------------------------------------
_RANGOS = {
    #                campo_min  campo_max  arq_min  arq_max
    "barro":    dict(campo=(1, 4),   arq=(2, 4)),
    "estrella": dict(campo=(6, 10),  arq=(6, 10)),
}

_PRECIO_FACTOR = 100   # Suma stats * 100


# ---------------------------------------------------------------------------
# Función principal
# ---------------------------------------------------------------------------
def generar_jugador(rango: str) -> Jugador:
    """
    Genera un Jugador aleatorio según el rango indicado.

    rango:
        "barro"    → stats de campo 1-4,  ARQ portero 2-4
        "estrella" → stats de campo 6-10, ARQ portero 6-10
    """
    if rango not in _RANGOS:
        raise ValueError(f"Rango '{rango}' inválido. Usa 'barro' o 'estrella'.")

    cfg = _RANGOS[rango]
    c_min, c_max = cfg["campo"]
    a_min, a_max = cfg["arq"]

    nombre = f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}"
    edad   = random.randint(17, 35)

    # 10% de probabilidad de ser portero
    es_portero = random.random() < 0.10

    if es_portero:
        fis  = 1
        tec  = 1
        defe = 1
        men  = 1
        arq  = float(random.randint(a_min, a_max))
    else:
        fis  = float(random.randint(c_min, c_max))
        tec  = float(random.randint(c_min, c_max))
        defe = float(random.randint(c_min, c_max))
        men  = float(random.randint(c_min, c_max))
        arq  = 1.0   # jugador de campo: ARQ siempre mínimo

    precio = int((fis + tec + defe + men + arq) * _PRECIO_FACTOR)

    return Jugador(
        nombre=nombre,
        fis=fis,
        tec=tec,
        defe=defe,
        men=men,
        arq=arq,
        edad=edad,
        precio=precio,
    )


# ---------------------------------------------------------------------------
# Smoke-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== 5 jugadores BARRO ===")
    for _ in range(5):
        j = generar_jugador("barro")
        print(f"  {j.nombre:30s} edad={j.edad}  FÍS={j.fis} TÉC={j.tec} DEF={j.defe} MEN={j.men} ARQ={j.arq}  precio=${j.precio}")

    print("\n=== 1 jugador ESTRELLA ===")
    j = generar_jugador("estrella")
    print(f"  {j.nombre:30s} edad={j.edad}  FÍS={j.fis} TÉC={j.tec} DEF={j.defe} MEN={j.men} ARQ={j.arq}  precio=${j.precio}")
