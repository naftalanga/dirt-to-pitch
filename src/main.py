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

    print()
    print("--- HUB DEL MÁNAGER ---")
    print(f"Fecha Actual: {partida['fecha_actual']} / 14  |  Caja: ${partida['caja']}")
    print("1. Ver mi Plantilla")
    print("2. Ver Tabla de Posiciones")
    print(f"3. Jugar Fecha {partida['fecha_actual']}")
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

    # --- Opción 3: Jugar fecha ---
    elif opcion == "3":
        if partida["fecha_actual"] > 14:
            print("\n  La temporada ha finalizado. No hay más fechas por jugar.")
        else:
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
