def generar_fixture(nombres_equipos: list[str]) -> dict:
    """
    Round-Robin para N equipos (N debe ser par).
    Genera ida (fechas 1..N-1) y vuelta (fechas N..2*(N-1)) invirtiendo local/visita.
    Retorna dict: {fecha_int: [(local, visitante), ...]}
    """
    equipos = list(nombres_equipos)
    if len(equipos) % 2 != 0:
        equipos.append("BYE")          # bye si número impar

    n       = len(equipos)
    rondas  = n - 1
    fixture = {}

    for ronda in range(rondas):
        fecha_ida    = ronda + 1
        fecha_vuelta = rondas + ronda + 1
        fixture[fecha_ida]    = []
        fixture[fecha_vuelta] = []

        for i in range(n // 2):
            local   = equipos[i]
            visita  = equipos[n - 1 - i]
            if "BYE" not in (local, visita):
                fixture[fecha_ida].append((local, visita))
                fixture[fecha_vuelta].append((visita, local))

        # Rotar todos excepto el primero (algoritmo estándar)
        equipos = [equipos[0]] + [equipos[-1]] + equipos[1:-1]

    return fixture


def inicializar_tabla(nombres_equipos: list[str]) -> dict:
    return {
        nombre: {"PJ": 0, "PG": 0, "PE": 0, "PP": 0, "GF": 0, "GC": 0, "DG": 0, "PTS": 0}
        for nombre in nombres_equipos
    }


def actualizar_tabla(
    tabla: dict,
    local: str, goles_local: int,
    visita: str, goles_visita: int,
) -> None:
    tabla[local]["PJ"]  += 1
    tabla[visita]["PJ"] += 1

    tabla[local]["GF"]  += goles_local
    tabla[local]["GC"]  += goles_visita
    tabla[visita]["GF"] += goles_visita
    tabla[visita]["GC"] += goles_local

    tabla[local]["DG"]  = tabla[local]["GF"]  - tabla[local]["GC"]
    tabla[visita]["DG"] = tabla[visita]["GF"] - tabla[visita]["GC"]

    if goles_local > goles_visita:
        tabla[local]["PTS"]  += 3
        tabla[local]["PG"]   += 1
        tabla[visita]["PP"]  += 1
    elif goles_visita > goles_local:
        tabla[visita]["PTS"] += 3
        tabla[visita]["PG"]  += 1
        tabla[local]["PP"]   += 1
    else:
        tabla[local]["PTS"]  += 1
        tabla[visita]["PTS"] += 1
        tabla[local]["PE"]   += 1
        tabla[visita]["PE"]  += 1


def imprimir_tabla(tabla: dict) -> None:
    ordenada = sorted(
        tabla.items(),
        key=lambda x: (x[1]["PTS"], x[1]["DG"]),
        reverse=True,
    )
    print(f"\n  {'#':<4} {'EQUIPO':<28} {'PJ':>4} {'PG':>4} {'PE':>4} {'PP':>4} {'GF':>4} {'GC':>4} {'DG':>4} {'PTS':>4}")
    print("  " + "-" * 64)
    for pos, (nombre, stats) in enumerate(ordenada, start=1):
        print(
            f"  {pos:<4} {nombre:<28} {stats['PJ']:>4} {stats['PG']:>4} "
            f"{stats['PE']:>4} {stats['PP']:>4} {stats['GF']:>4} "
            f"{stats['GC']:>4} {stats['DG']:>+4} {stats['PTS']:>4}"
        )


if __name__ == "__main__":
    # --- Smoke-test tabla ---
    equipos_dummy = ["Barro FC", "Real Mandril", "Boca Jrs"]
    tabla = inicializar_tabla(equipos_dummy)

    actualizar_tabla(tabla, "Barro FC", 3, "Real Mandril", 1)
    actualizar_tabla(tabla, "Boca Jrs", 0, "Barro FC", 0)
    actualizar_tabla(tabla, "Real Mandril", 2, "Boca Jrs", 2)

    imprimir_tabla(tabla)

    # --- Smoke-test fixture ---
    nombres = [
        "Barro FC", "Sporting de Lisboa", "Milan AC", "Real Mandril",
        "Boca Jrs", "Colo Colo Dummy", "U de Chile RC", "Deportivo Conceptivo",
    ]
    fixture = generar_fixture(nombres)
    print()
    for fecha, partidos in sorted(fixture.items()):
        print(f"--- Fecha {fecha} ---")
        for local, visita in partidos:
            print(f"   {local} vs {visita}")
