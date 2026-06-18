import json
import os
from dataclasses import asdict, fields
from motor_core import Jugador, Equipo

RUTA_DB = "db/partida.json"


def guardar_partida(partida: dict) -> None:
    """
    Recibe el dict de estado completo de la partida y lo persiste en el JSON.
    Claves esperadas: equipo (Equipo), caja, rivales, fixture, fecha_actual,
                      tabla, formacion_actual, estilo_actual,
                      temporada_actual, division_actual.
    """
    os.makedirs("db", exist_ok=True)
    # Las claves del fixture son int en memoria pero JSON las convierte a str; se guardan como str.
    # Campos de Jugador que no deben persistirse (uso solo en memoria)
    _EXCLUIR_JUGADOR = {"nota_evolucion"}

    def _jugador_serializable(j: "Jugador") -> dict:
        return {k: v for k, v in asdict(j).items() if k not in _EXCLUIR_JUGADOR}

    def _equipo_serializable(e: "Equipo") -> dict:
        return {"nombre": e.nombre, "jugadores": [_jugador_serializable(j) for j in e.jugadores]}

    datos = {
        "equipo":            _equipo_serializable(partida["equipo"]),
        "caja":              partida["caja"],
        "rivales":           [_equipo_serializable(r) for r in partida["rivales"]],
        "fixture":           {str(k): v for k, v in partida["fixture"].items()},
        "fecha_actual":      partida["fecha_actual"],
        "tabla":             partida.get("tabla"),
        "formacion_actual":  partida.get("formacion_actual",  "4-4-2"),
        "estilo_actual":     partida.get("estilo_actual",     "Equilibrado"),
        "temporada_actual":  partida.get("temporada_actual",  1),
        "division_actual":   partida.get("division_actual",   3),
    }
    with open(RUTA_DB, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f"[SAVE] Partida guardada en '{RUTA_DB}'.")


def cargar_partida() -> dict | None:
    if not os.path.exists(RUTA_DB):
        return None

    with open(RUTA_DB, "r", encoding="utf-8") as f:
        datos = json.load(f)

    jugadores = [Jugador(**j) for j in datos["equipo"]["jugadores"]]
    equipo    = Equipo(nombre=datos["equipo"]["nombre"], jugadores=jugadores)
    caja      = datos["caja"]
    rivales   = [
        Equipo(
            nombre=r["nombre"],
            jugadores=[Jugador(**j) for j in r["jugadores"]],
        )
        for r in datos.get("rivales", [])
    ]

    # Fixture: claves vienen como str desde JSON, se convierten a int
    fixture_raw  = datos.get("fixture", {})
    fixture      = {int(k): [tuple(p) for p in v] for k, v in fixture_raw.items()}
    fecha_actual = datos.get("fecha_actual", 1)

    tabla             = datos.get("tabla")
    formacion_actual  = datos.get("formacion_actual",  "4-4-2")
    estilo_actual     = datos.get("estilo_actual",     "Equilibrado")
    temporada_actual  = datos.get("temporada_actual",  1)
    division_actual   = datos.get("division_actual",   3)
    caja              = datos.get("caja",              0)

    print(f"[LOAD] Partida cargada: '{equipo.nombre}'  |  Caja: ${caja}  |  Rivales: {len(rivales)}  |  Fecha: {fecha_actual}")

    return {
        "equipo":           equipo,
        "caja":             caja,
        "rivales":          rivales,
        "fixture":          fixture,
        "fecha_actual":     fecha_actual,
        "tabla":            tabla,
        "formacion_actual": formacion_actual,
        "estilo_actual":    estilo_actual,
        "temporada_actual": temporada_actual,
        "division_actual":  division_actual,
    }


# if __name__ == "__main__":
#     from motor_core import Jugador, Equipo

#     # --- Equipo dummy de prueba (11 jugadores) ---
#     portero = Jugador(nombre="Lianel Messido",  fis=1.0, tec=1.0, defe=1.0, men=1.0, arq=4.0, edad=28, precio=800)
#     campo   = [
#         Jugador(nombre=f"Barro J{i}", fis=2.0, tec=2.0, defe=2.0, men=2.0, arq=1.0, edad=22, precio=900)
#         for i in range(1, 11)
#     ]
#     equipo_dummy = Equipo(nombre="Barro FC Dummy", jugadores=[portero] + campo)

#     # --- Guardar ---
#     guardar_partida(equipo_dummy, caja=5000)

#     # --- Cargar y verificar ---
#     resultado = cargar_partida()
#     if resultado:
#         equipo_cargado, caja_cargada = resultado
#         print(f"\nEquipo: {equipo_cargado.nombre}  |  Caja: ${caja_cargada}")
#         print(f"{'NOMBRE':<28} {'FÍS':>4} {'TÉC':>4} {'DEF':>4} {'MEN':>4} {'ARQ':>4}  {'EDAD':>4}  {'PRECIO':>7}")
#         print("-" * 62)
#         for j in equipo_cargado.jugadores:
#             portero_tag = " [POR]" if j.arq > 1.0 else ""
#             print(
#                 f"{j.nombre:<28} {j.fis:>4.0f} {j.tec:>4.0f} {j.defe:>4.0f} "
#                 f"{j.men:>4.0f} {j.arq:>4.0f}  {j.edad:>4}  ${j.precio:>6}{portero_tag}"
#             )
