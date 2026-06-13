from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple


@dataclass
class Jugador:
    nombre: str
    fis: float = 1.0   # Físico: velocidad y resistencia
    tec: float = 1.0   # Técnica: pase, definición y control
    defe: float = 1.0  # Defensa: recuperación y posicionamiento
    men: float = 1.0   # Mentalidad: resistencia a la presión
    arq: float = 1.0   # Arquero: exclusivo para guardametas (mínimo 1)
    edad: int = 20     # Edad del jugador
    precio: int = 0    # Valor de mercado calculado dinámicamente


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
