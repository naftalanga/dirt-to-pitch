import sys
from db_manager import cargar_partida, guardar_partida
from motor_core import simular_partido
from liga import imprimir_tabla, inicializar_tabla, actualizar_tabla

# ---------------------------------------------------------------------------
# Carga de partida
# ---------------------------------------------------------------------------
datos = cargar_partida()

if datos is None:
    print("[ERROR] No hay partida guardada. Ejecuta mercado.py primero para crear una.")
    sys.exit()

equipo_jugador, caja, rivales, fixture, fecha_actual, tabla_guardada = datos

# ---------------------------------------------------------------------------
# Preparación de datos de liga
# ---------------------------------------------------------------------------
todos_los_equipos = [equipo_jugador] + rivales

if tabla_guardada is not None:
    tabla_actual = tabla_guardada
else:
    tabla_actual = inicializar_tabla([e.nombre for e in todos_los_equipos])

# ---------------------------------------------------------------------------
# Bucle principal del Hub del Mánager
# ---------------------------------------------------------------------------
while True:
    print()
    print("--- HUB DEL MÁNAGER ---")
    print(f"Fecha Actual: {fecha_actual} / 14  |  Caja: ${caja}")
    print("1. Ver mi Plantilla")
    print("2. Ver Tabla de Posiciones")
    print(f"3. Jugar Fecha {fecha_actual}")
    print("4. Guardar y Salir")
    print()

    opcion = input(">> Elige una opción: ").strip()

    # --- Opción 1: Ver plantilla ---
    if opcion == "1":
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
        imprimir_tabla(tabla_actual)

    # --- Opción 3: Jugar fecha ---
    elif opcion == "3":
        if fecha_actual > 14:
            print("\n  La temporada ha finalizado. No hay más fechas por jugar.")
        else:
            partidos = fixture[fecha_actual]
            print(f"\n  --- FECHA {fecha_actual} ---")
            for nombre_local, nombre_visita in partidos:
                equipo_l = next(e for e in todos_los_equipos if e.nombre == nombre_local)
                equipo_v = next(e for e in todos_los_equipos if e.nombre == nombre_visita)

                resultado = simular_partido(
                    equipo_l, equipo_v,
                    formacion_l="4-4-2", estilo_l="Equilibrado",
                    formacion_v="4-4-2", estilo_v="Equilibrado",
                )
                goles_l = resultado["local"]
                goles_v = resultado["visita"]

                print(f"  [RESULTADO] {nombre_local} {goles_l} - {goles_v} {nombre_visita}")
                actualizar_tabla(tabla_actual, nombre_local, goles_l, nombre_visita, goles_v)

            fecha_actual += 1

    # --- Opción 4: Guardar y salir ---
    elif opcion == "4":
        guardar_partida(equipo_jugador, caja, rivales, fixture, fecha_actual, tabla_actual)
        print("[INFO] Partida guardada. ¡Hasta la próxima!")
        break

    else:
        print("  [ERROR] Opción inválida. Elige un número entre 1 y 4.")
