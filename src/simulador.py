# simulador.py — re-exporta simular_partido desde motor_core (backward-compat)
from motor_core import Jugador, Equipo, simular_partido  # noqa: F401


def _legacy_simular_partido(
    equipo_local: Equipo,
    form_local: str,
    equipo_visita: Equipo,
    form_visita: str,
    presion: int = 5,
    chances_totales: int = 10,
) -> dict:
    # --- Calcular poderes ---
    poder_local   = calcular_poder_zonas(equipo_local,  form_local,  presion)
    poder_visita  = calcular_poder_zonas(equipo_visita, form_visita, presion)

    med_local  = poder_local["mediocampo"]
    med_visita = poder_visita["mediocampo"]

    # --- Repartir chances según dominio del mediocampo ---
    chances_local  = round((med_local / (med_local + med_visita)) * chances_totales)
    chances_visita = chances_totales - chances_local

    print(f"\n== {equipo_local.nombre} vs {equipo_visita.nombre} ==")
    print(f"   Mediocampo  →  {equipo_local.nombre}: {med_local}  |  {equipo_visita.nombre}: {med_visita}")
    print(f"   Chances     →  {equipo_local.nombre}: {chances_local}  |  {equipo_visita.nombre}: {chances_visita}\n")

    goles_local  = 0
    goles_visita = 0

    def resolver_chance(nombre_ata, ataque, defensa, arquero):
        prob_tiro_base  = (ataque / (ataque + defensa)) * 100
        prob_tiro_final = max(5.0, min(95.0, prob_tiro_base))
        dado_tiro       = random.randint(1, 100)

        if dado_tiro <= prob_tiro_final:
            prob_atajada = min(arquero * 8.5, 85.0)
            dado_arq     = random.randint(1, 100)
            if dado_arq <= prob_atajada:
                print(f"  🧤 [{nombre_ata}] Tiro en → Atajado. (dado_tiro={dado_tiro} prob_tiro={prob_tiro_final:.1f}% | dado_arq={dado_arq} prob_atajada={prob_atajada:.1f}%)")
            else:
                print(f"  ⚽ [{nombre_ata}] Tiro en → GOOOL!  (dado_tiro={dado_tiro} prob_tiro={prob_tiro_final:.1f}% | dado_arq={dado_arq} prob_atajada={prob_atajada:.1f}%)")
                return True
        else:
            print(f"  ❌ [{nombre_ata}] Tiro fuera.           (dado_tiro={dado_tiro} prob_tiro={prob_tiro_final:.1f}%)")
        return False

    # --- Chances del local ---
    for _ in range(chances_local):
        if resolver_chance(
            equipo_local.nombre,
            poder_local["ofensivo"],
            poder_visita["defensivo"],
            poder_visita["arquero"],
        ):
            goles_local += 1

    # --- Chances de la visita ---
    for _ in range(chances_visita):
        if resolver_chance(
            equipo_visita.nombre,
            poder_visita["ofensivo"],
            poder_local["defensivo"],
            poder_local["arquero"],
        ):
            goles_visita += 1

    print(f"\n  Resultado Final: {equipo_local.nombre} {goles_local} - {goles_visita} {equipo_visita.nombre}\n")

    return {
        "local":  goles_local,
        "visita": goles_visita,
    }


if __name__ == "__main__":
    def _hacer_equipo(nombre, fis, tec, defe, men, arq_portero):
        portero  = Jugador(nombre=f"{nombre}_POR", fis=fis, tec=tec, defe=defe, men=men, arq=arq_portero)
        campo    = [
            Jugador(nombre=f"{nombre}_J{i}", fis=fis, tec=tec, defe=defe, men=men, arq=1.0)
            for i in range(1, 11)
        ]
        return Equipo(nombre=nombre, jugadores=[portero] + campo)

    local   = _hacer_equipo("Barro FC",      fis=6, tec=7, defe=5, men=5, arq_portero=7)
    visita  = _hacer_equipo("Deportes Conceptivos", fis=5, tec=7, defe=6, men=4, arq_portero=2)

    simular_partido(local, "5-3-2", visita, "4-3-3", presion=5, chances_totales=10)
