import sys
from db_manager import cargar_partida, guardar_partida
from motor_core import simular_partido
from liga import imprimir_tabla, inicializar_tabla, actualizar_tabla

# ---------------------------------------------------------------------------
# Constantes de táctica
# ---------------------------------------------------------------------------
FORMACIONES_DISPONIBLES = [
    "4-3-3", "4-4-2", "4-2-3-1", "4-2-4",
    "3-5-2", "5-3-2", "4-5-1", "3-4-3",
]
ESTILOS_DISPONIBLES = ["Defensivo", "Equilibrado", "Ofensivo"]

# ---------------------------------------------------------------------------
# Escala de premios por posición final (1° a 8°)
# ---------------------------------------------------------------------------
PREMIOS_POSICION = {
    1: 2000,
    2: 1500,
    3: 1000,
    4:  800,
    5:  600,
    6:  400,
    7:  200,
    8:  100,
}

# ---------------------------------------------------------------------------
# Carga de partida
# ---------------------------------------------------------------------------
partida = cargar_partida()

if partida is None:
    print("[ERROR] No hay partida guardada. Ejecuta mercado.py primero para crear una.")
    sys.exit()

# ---------------------------------------------------------------------------
# Preparación de datos de liga
# ---------------------------------------------------------------------------
todos_los_equipos = [partida["equipo"]] + partida["rivales"]

if partida["tabla"] is not None:
    partida["tabla"] = partida["tabla"]
else:
    partida["tabla"] = inicializar_tabla([e.nombre for e in todos_los_equipos])

# ---------------------------------------------------------------------------
# Bucle principal del Hub del Mánager
# ---------------------------------------------------------------------------
while True:
    formacion_actual = partida["formacion_actual"]
    estilo_actual    = partida["estilo_actual"]

    fecha_actual     = partida["fecha_actual"]
    temporada_actual = partida["temporada_actual"]
    division_actual  = partida["division_actual"]

    label_opcion_3 = (
        f"Jugar Fecha {fecha_actual}"
        if fecha_actual <= 14
        else "Finalizar Temporada"
    )

    print()
    print(f"=== HUB DEL MÁNAGER | Temp: {temporada_actual} - Div: {division_actual} ===")
    print(f"Fecha Actual: {fecha_actual} / 14  |  Caja: ${partida['caja']}")
    print("1. Ver mi Plantilla")
    print("2. Ver Tabla de Posiciones")
    print(f"3. {label_opcion_3}")
    print(f"4. Cambiar Táctica          [Táctica actual: {formacion_actual} | {estilo_actual}]")
    print("5. Guardar y Salir")
    print()

    opcion = input(">> Elige una opción: ").strip()

    # --- Opción 1: Ver plantilla ---
    if opcion == "1":
        equipo_jugador = partida["equipo"]
        print()
        print(f"  PLANTILLA: {equipo_jugador.nombre}")
        print(f"  {'NOMBRE':<28} {'EDAD':>4} {'FÍS':>4} {'TÉC':>4} {'DEF':>4} {'MEN':>4} {'ARQ':>4}  {'PRECIO':>7}")
        print("  " + "-" * 65)
        for j in equipo_jugador.jugadores:
            portero_tag = " [POR]" if j.arq > 1.0 else ""
            print(
                f"  {j.nombre:<28} {j.edad:>4} {j.fis:>4.0f} {j.tec:>4.0f} "
                f"{j.defe:>4.0f} {j.men:>4.0f} {j.arq:>4.0f}  ${j.precio:>6}{portero_tag}"
            )

    # --- Opción 2: Ver tabla ---
    elif opcion == "2":
        imprimir_tabla(partida["tabla"])

    # --- Opción 3: Jugar Fecha / Finalizar Temporada ---
    elif opcion == "3":
        if partida["fecha_actual"] <= 14:
            # ---- Jugar la fecha ----
            partidos_fecha = partida["fixture"][partida["fecha_actual"]]
            print(f"\n  --- FECHA {partida['fecha_actual']} ---")

            nombre_jugador = partida["equipo"].nombre

            for nombre_local, nombre_visita in partidos_fecha:
                equipo_l = next(e for e in todos_los_equipos if e.nombre == nombre_local)
                equipo_v = next(e for e in todos_los_equipos if e.nombre == nombre_visita)

                # Inyectar táctica del jugador según si es local o visita
                if nombre_local == nombre_jugador:
                    f_l, e_l = formacion_actual, estilo_actual
                    f_v, e_v = "4-4-2", "Equilibrado"
                elif nombre_visita == nombre_jugador:
                    f_l, e_l = "4-4-2", "Equilibrado"
                    f_v, e_v = formacion_actual, estilo_actual
                else:
                    f_l, e_l = "4-4-2", "Equilibrado"
                    f_v, e_v = "4-4-2", "Equilibrado"

                resultado = simular_partido(
                    equipo_l, equipo_v,
                    formacion_l=f_l, estilo_l=e_l,
                    formacion_v=f_v, estilo_v=e_v,
                )
                goles_l = resultado["local"]
                goles_v = resultado["visita"]

                print(f"  [RESULTADO] {nombre_local} {goles_l} - {goles_v} {nombre_visita}")
                actualizar_tabla(partida["tabla"], nombre_local, goles_l, nombre_visita, goles_v)

            partida["fecha_actual"] += 1

        else:
            # ---- Finalizar Temporada ----
            tabla_ordenada = sorted(
                partida["tabla"].items(),
                key=lambda x: (x[1]["PTS"], x[1]["DG"]),
                reverse=True,
            )

            nombre_jugador = partida["equipo"].nombre
            posicion_final = next(
                (pos for pos, (nombre, _) in enumerate(tabla_ordenada, start=1)
                 if nombre == nombre_jugador),
                len(tabla_ordenada),
            )
            premio = PREMIOS_POSICION.get(posicion_final, 0)
            partida["caja"] += premio

            print()
            print("=" * 56)
            print("       *** FIN DE TEMPORADA ***")
            print("=" * 56)
            print(f"  Equipo   : {nombre_jugador}")
            print(f"  Temporada: {partida['temporada_actual']}  |  División: {partida['division_actual']}")
            print()
            print("  CLASIFICACIÓN FINAL:")
            for pos, (nombre, stats) in enumerate(tabla_ordenada, start=1):
                marcador = " <<" if nombre == nombre_jugador else ""
                print(
                    f"  {pos:>2}. {nombre:<28} "
                    f"PTS: {stats['PTS']:>3}  DG: {stats['DG']:>+4}{marcador}"
                )
            print()
            print(f"  Posición obtenida : {posicion_final}°")
            print(f"  Premio económico  : +${premio}")
            print(f"  Caja tras premio  : ${partida['caja']}")
            print("=" * 56)

            # --- Placeholder próximo sprint: reinicio de temporada ---
            partida["temporada_actual"] += 1
            partida["fecha_actual"]      = 1
            for stats in partida["tabla"].values():
                for clave in ("PJ", "PG", "PE", "PP", "GF", "GC", "DG", "PTS"):
                    stats[clave] = 0

            guardar_partida(partida)
            print(f"\n  [INFO] Temporada {partida['temporada_actual'] - 1} archivada. "
                  f"Comenzando Temporada {partida['temporada_actual']}...")
            print("=" * 56)

    # --- Opción 4: Cambiar táctica ---
    elif opcion == "4":
        print()
        print("  --- PIZARRA TÁCTICA ---")
        print("  Elige tu Formación:")
        for i, f in enumerate(FORMACIONES_DISPONIBLES, start=1):
            print(f"    {i}. {f}")
        print()

        raw_f = input("  >> Formación (número): ").strip()
        if raw_f.isdigit() and 1 <= int(raw_f) <= len(FORMACIONES_DISPONIBLES):
            partida["formacion_actual"] = FORMACIONES_DISPONIBLES[int(raw_f) - 1]
        else:
            print("  [ERROR] Opción inválida. Formación no cambiada.")

        print()
        print("  Elige tu Estilo:")
        for i, e in enumerate(ESTILOS_DISPONIBLES, start=1):
            print(f"    {i}. {e}")
        print()

        raw_e = input("  >> Estilo (número): ").strip()
        if raw_e.isdigit() and 1 <= int(raw_e) <= len(ESTILOS_DISPONIBLES):
            partida["estilo_actual"] = ESTILOS_DISPONIBLES[int(raw_e) - 1]
        else:
            print("  [ERROR] Opción inválida. Estilo no cambiado.")

        guardar_partida(partida)
        print(
            f"  [OK] Táctica actualizada: "
            f"{partida['formacion_actual']} | {partida['estilo_actual']}"
        )

    # --- Opción 5: Guardar y salir ---
    elif opcion == "5":
        guardar_partida(partida)
        print("[INFO] Partida guardada. ¡Hasta la próxima!")
        break

    else:
        print("  [ERROR] Opción inválida. Elige un número entre 1 y 5.")
