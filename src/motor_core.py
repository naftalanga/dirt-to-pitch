import random
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple


# ---------------------------------------------------------------------------
# Multiplicadores de estilo táctico
# ---------------------------------------------------------------------------
ESTILOS = {
    "Ofensivo":    {"tec_fis": 1.2, "def_arq": 0.8},
    "Defensivo":   {"tec_fis": 0.8, "def_arq": 1.2},
    "Equilibrado": {"tec_fis": 1.0, "def_arq": 1.0},
}


@dataclass
class Jugador:
    nombre: str
    fis: float = 1.0           # Físico: velocidad y resistencia
    tec: float = 1.0           # Técnica: pase, definición y control
    defe: float = 1.0          # Defensa: recuperación y posicionamiento
    men: float = 1.0           # Mentalidad: resistencia a la presión
    arq: float = 1.0           # Arquero: exclusivo para guardametas (mínimo 1)
    edad: int = 20             # Edad del jugador
    precio: int = 0            # Valor de mercado calculado dinámicamente
    nota_evolucion: Optional[str] = field(default=None, repr=False)  # Uso temporal, no se persiste


@dataclass
class Equipo:
    nombre: str
    jugadores: List[Jugador]

    def __post_init__(self):
        if len(self.jugadores) != 11:
            raise ValueError(f"El equipo debe tener exactamente 11 jugadores, se recibieron {len(self.jugadores)}.")


# Pesos de línea por formación: jugadores de campo asignados a cada zona (total = 10)
FORMACIONES = {
    "4-4-2": {"def": 4, "med": 4, "ata": 2},
    "4-3-3": {"def": 4, "med": 3, "ata": 3},
    "3-5-2": {"def": 3, "med": 5, "ata": 2},
    "5-3-2": {"def": 5, "med": 3, "ata": 2},
    "4-5-1": {"def": 4, "med": 5, "ata": 1},
}

CHANCES_TOTALES = 10


# ---------------------------------------------------------------------------
# Distribución táctica de plantilla
# ---------------------------------------------------------------------------
def distribuir_plantilla(equipo: "Equipo", formacion: str = "4-4-2") -> Dict[str, object]:
    if formacion not in FORMACIONES:
        raise ValueError(f"Formación '{formacion}' no existe en FORMACIONES.")

    pesos = FORMACIONES[formacion]

    # --- Arquero: jugador con mayor stat ARQ ---
    arquero = max(equipo.jugadores, key=lambda j: j.arq)
    campo   = [j for j in equipo.jugadores if j is not arquero]

    # --- Defensas: los D jugadores con mayor DEF ---
    n_def = pesos["def"]
    n_ata = pesos["ata"]

    campo_por_def = sorted(campo, key=lambda j: j.defe, reverse=True)
    defensas      = campo_por_def[:n_def]
    resto         = campo_por_def[n_def:]

    # --- Delanteros: los A jugadores con mayor TÉC + FÍS del resto ---
    resto_por_ata = sorted(resto, key=lambda j: j.tec + j.fis, reverse=True)
    delanteros    = resto_por_ata[:n_ata]

    # --- Mediocampistas: lo que sobra ---
    mediocampistas = resto_por_ata[n_ata:]

    return {
        "arquero":        arquero,
        "defensas":       defensas,
        "mediocampistas": mediocampistas,
        "delanteros":     delanteros,
    }


# ---------------------------------------------------------------------------
# Motor de simulación de partido
# ---------------------------------------------------------------------------
def simular_partido(
    equipo_l: "Equipo",
    equipo_v: "Equipo",
    formacion_l: str = "4-4-2",
    estilo_l:    str = "Equilibrado",
    formacion_v: str = "4-4-2",
    estilo_v:    str = "Equilibrado",
) -> dict:
    if estilo_l not in ESTILOS:
        raise ValueError(f"Estilo '{estilo_l}' no existe en ESTILOS.")
    if estilo_v not in ESTILOS:
        raise ValueError(f"Estilo '{estilo_v}' no existe en ESTILOS.")

    # --- Distribuir plantillas ---
    lineas_l = distribuir_plantilla(equipo_l, formacion_l)
    lineas_v = distribuir_plantilla(equipo_v, formacion_v)

    mul_l = ESTILOS[estilo_l]
    mul_v = ESTILOS[estilo_v]

    # --- Poder de mediocampo: suma (FÍS + TÉC + MEN) * tec_fis del estilo ---
    def poder_medio(mediocampistas: list, tec_fis: float) -> float:
        return sum((j.fis + j.tec + j.men) for j in mediocampistas) * tec_fis

    med_l = poder_medio(lineas_l["mediocampistas"], mul_l["tec_fis"])
    med_v = poder_medio(lineas_v["mediocampistas"], mul_v["tec_fis"])

    total_med = med_l + med_v if (med_l + med_v) > 0 else 1.0
    chances_l = round((med_l / total_med) * CHANCES_TOTALES)
    chances_v = CHANCES_TOTALES - chances_l

    print(f"\n== {equipo_l.nombre} vs {equipo_v.nombre} ==")
    print(f"   Mediocampo  →  {equipo_l.nombre}: {med_l:.1f}  |  {equipo_v.nombre}: {med_v:.1f}")
    print(f"   Chances     →  {equipo_l.nombre}: {chances_l}  |  {equipo_v.nombre}: {chances_v}\n")

    goles_l = 0
    goles_v = 0

    def resolver_chance(
        nombre_ata: str,
        delanteros: list,
        tec_fis: float,
        defensas_rival: list,
        def_arq_rival: float,
        arquero_rival: "Jugador",
        def_arq_arq_rival: float,
    ) -> bool:
        # Elegir delantero al azar
        delantero   = random.choice(delanteros)
        poder_tiro  = (delantero.tec + delantero.fis + delantero.men) * tec_fis

        # Muro defensivo: suma DEF de defensas * def_arq
        muro        = sum(j.defe for j in defensas_rival) * def_arq_rival
        total_blq   = poder_tiro + muro if (poder_tiro + muro) > 0 else 1.0
        prob_supera = max(5.0, min(95.0, (poder_tiro / total_blq) * 100))
        dado_blq    = random.randint(1, 100)

        if dado_blq > prob_supera:
            print(
                f"  🛡️  [{nombre_ata} - {delantero.nombre}] Bloqueado por defensa. "
                f"(dado={dado_blq} prob_supera={prob_supera:.1f}%)"
            )
            return False

        # Atajada: ARQ * def_arq
        poder_arq   = arquero_rival.arq * def_arq_arq_rival
        prob_atajada = min(poder_arq * 8.5, 85.0)
        dado_arq    = random.randint(1, 100)

        if dado_arq <= prob_atajada:
            print(
                f"  🧤 [{nombre_ata} - {delantero.nombre}] Superó defensa → Atajado. "
                f"(dado_blq={dado_blq} prob_supera={prob_supera:.1f}% | "
                f"dado_arq={dado_arq} prob_atajada={prob_atajada:.1f}%)"
            )
            return False

        print(
            f"  ⚽ [{nombre_ata} - {delantero.nombre}] Superó defensa → GOOOL! "
            f"(dado_blq={dado_blq} prob_supera={prob_supera:.1f}% | "
            f"dado_arq={dado_arq} prob_atajada={prob_atajada:.1f}%)"
        )
        return True

    # --- Chances del local ---
    for _ in range(chances_l):
        if resolver_chance(
            equipo_l.nombre,
            lineas_l["delanteros"],
            mul_l["tec_fis"],
            lineas_v["defensas"],
            mul_v["def_arq"],
            lineas_v["arquero"],
            mul_v["def_arq"],
        ):
            goles_l += 1

    # --- Chances de la visita ---
    for _ in range(chances_v):
        if resolver_chance(
            equipo_v.nombre,
            lineas_v["delanteros"],
            mul_v["tec_fis"],
            lineas_l["defensas"],
            mul_l["def_arq"],
            lineas_l["arquero"],
            mul_l["def_arq"],
        ):
            goles_v += 1

    print(f"\n  Resultado Final: {equipo_l.nombre} {goles_l} - {goles_v} {equipo_v.nombre}\n")

    return {"local": goles_l, "visita": goles_v}


# ---------------------------------------------------------------------------
# Función legacy — conservada para compatibilidad interna
# ---------------------------------------------------------------------------
def calcular_poder_zonas(
    equipo: Equipo,
    formacion: str,
    presion_partido: int,
) -> Dict[str, float]:
    if formacion not in FORMACIONES:
        raise ValueError(f"Formación '{formacion}' no existe en FORMACIONES.")

    pesos = FORMACIONES[formacion]

    # --- Paso 1: separar portero (arq más alto) ---
    portero = max(equipo.jugadores, key=lambda j: j.arq)
    campo   = [j for j in equipo.jugadores if j is not portero]

    # --- Paso 2: poder bruto de los 10 jugadores de campo (PRD 4.1) ---
    bruto_def = 0.0
    bruto_med = 0.0
    bruto_ata = 0.0

    for jugador in campo:
        # Presión Escénica (PRD 4.2)
        if jugador.men < presion_partido:
            mod = 0.70
        elif jugador.men > presion_partido:
            mod = 1.10
        else:
            mod = 1.00

        fis  = jugador.fis  * mod
        tec  = jugador.tec  * mod
        defe = jugador.defe * mod

        bruto_def += defe * 1.5 + fis * 0.5
        bruto_med += tec  * 1.0 + fis * 1.0
        bruto_ata += tec  * 1.5 + fis * 0.5

    # --- Paso 3: aplicar multiplicador de formación (peso / 10) ---
    return {
        "defensivo":  round(bruto_def * (pesos["def"] / 10), 2),
        "mediocampo": round(bruto_med * (pesos["med"] / 10), 2),
        "ofensivo":   round(bruto_ata * (pesos["ata"] / 10), 2),
        "arquero":    round(portero.arq, 2),
    }
