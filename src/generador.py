import random
from motor_core import Jugador, Equipo

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
# Pool de nombres de equipos rivales (parodia global)
# ---------------------------------------------------------------------------
NOMBRES_EQUIPOS = [
    "Manchester Sinti",
    "Inter de Melón",
    "Bayern de Múnich",
    "Paris San-Germán",
    "Pumas de la UNAM",
    "River Plateado",
    "Flamenco SC",
    "Kashima Anthers",
    "Juventud FC",
    "Real Mandril",
    "Boca Jrs",
    "Colo Colo Dummy",
    "U de Chile RC",
    "Deportivo Conceptivo",
    "Sporting de Lisboa",
    "Milán AC",
    "Atético de Madriz",
    "Tottenham Hotspurt",
    "Liverpool FC Lite",
    "Galatasaray Picante",
    "Ajax de Ámsterdan",
    "Porto Alegre CF",
    "São Paulinho FC",
    "Tigres BUAP",
    "Chacarita Juniors",
    "Olimpia Asunción",
    "Nacional de Urugüay",
    "Estudiantes de La Patria",
    "Defensa y Juicio",
    "Godoy Cruz Minus",
]

# ---------------------------------------------------------------------------
# Constantes de rango y división
# ---------------------------------------------------------------------------
_RANGOS = {
    #                campo_min  campo_max  arq_min  arq_max
    "barro":    dict(campo=(1, 4),   arq=(2, 4)),
    "estrella": dict(campo=(6, 10),  arq=(6, 10)),
}

# Offset de calidad por división.
# Stats base (escala 1-10) + offset → rangos aproximados:
#   Div 3: base 1-4  + offset 29  → 30-33  ... hasta base 4 + 29 = 33 (zona 30-50 con spread)
#   Div 2: base 1-4  + offset 49  → 50-53  ... (zona 50-70)
#   Div 1: base 1-4  + offset 69  → 70-73  ... (zona 70-90)
# El spread total dentro de cada división viene del rango de dados (1-20 para campo).
_DIV_OFFSET = {
    1: 69,   # élite:   stats campo 70-90
    2: 49,   # semi:    stats campo 50-70
    3: 29,   # amateur: stats campo 30-50
}
_DIV_CAMPO_RANGO  = 20   # spread de dado para jugadores de campo por div.
_DIV_ARQ_BASE     = {1: 7, 2: 5, 3: 2}   # ARQ mín portero por div.
_DIV_ARQ_RANGO    = {1: 3, 2: 3, 3: 3}   # spread de ARQ portero

_PRECIO_FACTOR = 100   # Suma stats * 100


# ---------------------------------------------------------------------------
# Función principal
# ---------------------------------------------------------------------------
def generar_jugador(rango: str) -> Jugador:
    """
    Genera un Jugador aleatorio según el rango indicado.
    Conservado para el draft del mercado inicial (Div 3 por defecto).

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
        fis  = 1.0
        tec  = 1.0
        defe = 1.0
        men  = 1.0
        arq  = float(random.randint(a_min, a_max))
    else:
        fis  = float(random.randint(c_min, c_max))
        tec  = float(random.randint(c_min, c_max))
        defe = float(random.randint(c_min, c_max))
        men  = float(random.randint(c_min, c_max))
        arq  = 1.0

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
# Generador de jugador individual con calidad por división (para el draft)
# ---------------------------------------------------------------------------
def generar_jugador_por_division(division: int = 3) -> Jugador:
    """
    Genera un Jugador individual con atributos acordes a la división.
    Usado en el mercado de draft para que los jugadores disponibles
    tengan el mismo rango que los rivales generados en esa división.

    division:
        1 → stats campo ~70-90  (elite)
        2 → stats campo ~50-70  (semi-pro)
        3 → stats campo ~30-50  (amateur)
    """
    division   = max(1, min(3, division))
    offset     = _DIV_OFFSET[division]
    spread     = _DIV_CAMPO_RANGO
    arq_base   = _DIV_ARQ_BASE[division]
    arq_spread = _DIV_ARQ_RANGO[division]

    nombre     = f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}"
    edad       = random.randint(17, 35)
    es_portero = random.random() < 0.10

    if es_portero:
        fis  = 1.0
        tec  = 1.0
        defe = 1.0
        men  = 1.0
        arq  = float(arq_base + random.randint(0, arq_spread))
    else:
        fis  = float(offset + random.randint(1, spread))
        tec  = float(offset + random.randint(1, spread))
        defe = float(offset + random.randint(1, spread))
        men  = float(offset + random.randint(1, spread))
        arq  = 1.0

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
# Generador de equipo rival con calidad por división
# ---------------------------------------------------------------------------
def generar_equipo_rival(nombre: str, division: int = 3) -> Equipo:
    """
    Genera un Equipo de 11 jugadores con calidad acorde a la división.

    division:
        1 → stats campo ~70-90  (elite)
        2 → stats campo ~50-70  (semi-pro)
        3 → stats campo ~30-50  (amateur)
    """
    division = max(1, min(3, division))   # clamp 1-3

    offset     = _DIV_OFFSET[division]
    spread     = _DIV_CAMPO_RANGO
    arq_base   = _DIV_ARQ_BASE[division]
    arq_spread = _DIV_ARQ_RANGO[division]

    def _stat_campo() -> float:
        return float(offset + random.randint(1, spread))

    def _stat_arq() -> float:
        return float(arq_base + random.randint(0, arq_spread))

    # --- Portero forzado ---
    portero = Jugador(
        nombre=f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}",
        fis=1.0,
        tec=1.0,
        defe=1.0,
        men=1.0,
        arq=_stat_arq(),
        edad=random.randint(17, 35),
        precio=0,
    )
    portero.precio = int(
        (portero.fis + portero.tec + portero.defe + portero.men + portero.arq)
        * _PRECIO_FACTOR
    )

    # --- 10 jugadores de campo forzados ---
    campo = []
    for _ in range(10):
        j = Jugador(
            nombre=f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}",
            fis=_stat_campo(),
            tec=_stat_campo(),
            defe=_stat_campo(),
            men=_stat_campo(),
            arq=1.0,
            edad=random.randint(17, 35),
            precio=0,
        )
        j.precio = int((j.fis + j.tec + j.defe + j.men + j.arq) * _PRECIO_FACTOR)
        campo.append(j)

    return Equipo(nombre=nombre, jugadores=[portero] + campo)


# ---------------------------------------------------------------------------
# Paso del tiempo: envejecimiento y retiro
# ---------------------------------------------------------------------------
def envejecer_plantilla(jugadores: list) -> list[str]:
    """
    Recibe una lista de objetos Jugador (mutable, in-place).
    - Suma 1 año a cada jugador.
    - Jóvenes (<23): 30% de probabilidad de subir FÍS o TÉC +1.
    - Veteranos (>31): 40% de probabilidad de bajar FÍS -1 (mín 1).
    - Muy mayores (>35): 50% de probabilidad de retiro (eliminado de la lista).
    Retorna lista de nombres de los jugadores retirados.
    """
    retirados = []

    for i in range(len(jugadores) - 1, -1, -1):
        j = jugadores[i]
        j.edad += 1
        j.nota_evolucion = None

        # Retiro por vejez (>35)
        if j.edad > 35 and random.random() < 0.50:
            retirados.append(j.nombre)
            jugadores.pop(i)
            continue

        # Declive veterano (>31)
        if j.edad > 31 and random.random() < 0.40:
            j.fis = max(1.0, j.fis - 1.0)
            j.nota_evolucion = "empeoró"

        # Mejora juvenil (<23)
        elif j.edad < 23 and random.random() < 0.30:
            if random.random() < 0.50:
                j.fis += 1.0
            else:
                j.tec += 1.0
            j.nota_evolucion = "mejoró"

        # Recalcular precio
        j.precio = int((j.fis + j.tec + j.defe + j.men + j.arq) * _PRECIO_FACTOR)

    return retirados


# ---------------------------------------------------------------------------
# Juvenil de emergencia (stats paupérrimos)
# ---------------------------------------------------------------------------
def generar_jugador_penca(es_arquero: bool = False) -> Jugador:
    """
    Genera un jugador de 16 años con stats mínimos.
    Usado como parche cuando la plantilla cae por debajo de 11.
    """
    nombre = f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)} Jr."

    if es_arquero:
        j = Jugador(
            nombre=nombre,
            fis=1.0, tec=1.0, defe=1.0, men=1.0,
            arq=3.0,
            edad=16,
            precio=100,
        )
    else:
        j = Jugador(
            nombre=nombre,
            fis=2.0, tec=2.0, defe=2.0, men=2.0,
            arq=1.0,
            edad=16,
            precio=100,
        )

    return j


# ---------------------------------------------------------------------------
# Smoke-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    for div in (1, 2, 3):
        eq = generar_equipo_rival(f"Test Div{div}", division=div)
        j0 = eq.jugadores[1]   # primer jugador de campo
        print(f"  Div {div} | {eq.nombre} | ejemplo campo: "
              f"FIS={j0.fis:.0f} TEC={j0.tec:.0f} DEF={j0.defe:.0f} MEN={j0.men:.0f}")

    print("\n=== 5 jugadores BARRO (draft) ===")
    for _ in range(5):
        j = generar_jugador("barro")
        print(f"  {j.nombre:30s} edad={j.edad}  "
              f"FÍS={j.fis} TÉC={j.tec} DEF={j.defe} MEN={j.men} ARQ={j.arq}  precio=${j.precio}")
