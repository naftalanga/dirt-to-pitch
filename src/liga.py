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


if __name__ == "__main__":
    nombres = [
        "Barro FC", "Sporting de Lisboa", "Milán AC", "Real Mandril",
        "Boca Jrs", "Colo Colo Dummy", "U de Chile RC", "Deportivo Conceptivo",
    ]
    fixture = generar_fixture(nombres)
    for fecha, partidos in fixture.items():
        print(f"\n--- Fecha {fecha} ---")
        for local, visita in partidos:
            print(f"   {local} vs {visita}")
