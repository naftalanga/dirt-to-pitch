from motor_core import Equipo
from generador import generar_jugador, generar_equipo_rival
from db_manager import guardar_partida
from liga import generar_fixture


def draft_inicial(presupuesto: int = 15000) -> tuple:
    mercado  = [generar_jugador("barro") for _ in range(20)]
    plantilla = []
    caja      = presupuesto

    while len(plantilla) < 11:
        print("\n" + "=" * 60)
        print(f"  CAJA: ${caja}   |   CUPOS RESTANTES: {11 - len(plantilla)}")
        print("=" * 60)
        print(f"  {'ID':<4} {'NOMBRE':<28} {'EDAD':>4} {'FÍS':>4} {'TÉC':>4} {'DEF':>4} {'MEN':>4} {'ARQ':>4}  {'PRECIO':>7}")
        print("  " + "-" * 62)
        for i, j in enumerate(mercado):
            portero_tag = " [POR]" if j.arq > 1.0 else ""
            print(
                f"  {i:<4} {j.nombre:<28} {j.edad:>4} {j.fis:>4.0f} {j.tec:>4.0f} "
                f"{j.defe:>4.0f} {j.men:>4.0f} {j.arq:>4.0f}  ${j.precio:>6}{portero_tag}"
            )
        print()

        raw = input("  >> Ingresa el ID del jugador a fichar: ").strip()

        # --- Validar que sea un número ---
        if not raw.isdigit():
            print("  [ERROR] ID inválido. Ingresa un número de la lista.")
            continue

        idx = int(raw)

        # --- Validar que el índice exista ---
        if idx < 0 or idx >= len(mercado):
            print(f"  [ERROR] ID {idx} no existe en el mercado.")
            continue

        jugador = mercado[idx]

        # --- Validar fondos ---
        if jugador.precio > caja:
            print(f"  [ERROR] Fondos insuficientes. Necesitas ${jugador.precio}, tienes ${caja}.")
            continue

        # --- Compra válida ---
        caja  -= jugador.precio
        plantilla.append(jugador)
        mercado.pop(idx)
        print(f"  [OK] ¡Fichado! {jugador.nombre}  (precio: ${jugador.precio} | caja restante: ${caja})")

        # --- Regla de cierre: al completar el cupo 11, verificar portero ---
        if len(plantilla) == 11:
            tiene_portero = any(j.arq > 1.0 for j in plantilla)
            if not tiene_portero:
                ultimo = plantilla.pop()
                caja  += ultimo.precio
                mercado.append(ultimo)
                print()
                print("  [¡¡ERROR GRAVE!!] No hay ningún portero en tu plantilla.")
                print(f"  Se devolvió a {ultimo.nombre} al mercado y se reembolsaron ${ultimo.precio}.")
                print("  Debes fichar un portero (marcado con [POR]) para el último cupo.")

    # --- Nombre del equipo ---
    print("\n" + "=" * 60)
    nombre_equipo = input("  >> ¿Cómo se llama tu equipo? ").strip()
    if not nombre_equipo:
        nombre_equipo = "Equipo Sin Nombre"

    equipo_final = Equipo(nombre=nombre_equipo, jugadores=plantilla)

    print()
    print(f"  ¡Equipo '{equipo_final.nombre}' armado! Caja final: ${caja}")
    print("=" * 60)

    return (equipo_final, caja)


if __name__ == "__main__":
    equipo, caja = draft_inicial()

    nombres_rivales = [
        "Sporting de Lisboa",
        "Milán AC",
        "Real Mandril",
        "Boca Jrs",
        "Colo Colo Dummy",
        "U de Chile RC",
        "Deportivo Conceptivo",
    ]
    lista_rivales = [generar_equipo_rival(n) for n in nombres_rivales]

    todos_los_nombres = [equipo.nombre] + nombres_rivales
    fixture = generar_fixture(todos_los_nombres)

    guardar_partida({
        "equipo":           equipo,
        "caja":             caja,
        "rivales":          lista_rivales,
        "fixture":          fixture,
        "fecha_actual":     1,
        "tabla":            None,
        "formacion_actual": "4-4-2",
        "estilo_actual":    "Equilibrado",
    })
    print("[SAVE] ¡Tu equipo ha sido registrado en la base de datos!")
    print(f"\nRESUMEN FINAL: {equipo.nombre}  |  Caja: ${caja}")
    print(f"{'NOMBRE':<28} {'FÍS':>4} {'TÉC':>4} {'DEF':>4} {'MEN':>4} {'ARQ':>4}  {'EDAD':>4}  {'PRECIO':>7}")
    print("-" * 62)
    for j in equipo.jugadores:
        portero_tag = " [POR]" if j.arq > 1.0 else ""
        print(
            f"{j.nombre:<28} {j.fis:>4.0f} {j.tec:>4.0f} {j.defe:>4.0f} "
            f"{j.men:>4.0f} {j.arq:>4.0f}  {j.edad:>4}  ${j.precio:>6}{portero_tag}"
        )
