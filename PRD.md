# PRD: Proyecto "Dirt to Pitch - El Camino desde Barro"

## 1. Visión del Producto
* **Qué es:** Un videojuego *roguelite* de gestión de fútbol hiper-rápido enfocado en la toma de decisiones estratégicas y económicas sin microgestión pesada.
* **Inspiración y Tono:** La agilidad de *7a0*, el gameplay loop de *Super Auto Pets*, y la progresión orgánica de *Kairosoft*. Tono de humor y sátira basado en el folclore del fútbol, usando parodias de jugadores, clubes y estadios (ej. jugar en el "Claro Arena").
* **Objetivo del Jugador:** Llevar a un equipo de muertos de hambre desde la división más baja hasta la gloria, balanceando la táctica, la billetera y la infraestructura.

## 2. El Ciclo de Juego (Game Loop)
1.  **Pre-Temporada (Draft):** Presupuesto acotado y tiradas aleatorias (rolls) para fichar el 11 inicial.
2.  **Temporada Regular:** Calendario rápido. Eventos de texto semanales (decisión de 5 seg). Partidos auto-simulados en 10 seg.
3.  **Post-Temporada (Mercado):** Ascensos/Descensos. Compra/venta de jugadores. Envejecimiento de la plantilla.

## 3. Sistema de Jugadores (Atributos, Edad y Rasgos)

### 3.1 Atributos Core (Escala 1 a 10)
* **FÍS (Físico):** Velocidad y resistencia.
* **TÉC (Técnica):** Pase, definición y control.
* **DEF (Defensa):** Recuperación y posicionamiento.
* **MEN (Mentalidad):** Resistencia a la presión ambiental.
* **ARQ (Arquero):** Exclusivo para guardametas.

### 3.2 Curva de Progresión por Edad
* **Juvenil (17-21):** Stats bajos, MEN baja. Probabilidad de buff anual si juegan.
* **Plenitud (22-29):** Rendimiento máximo y estable.
* **Veterano (30-34):** FÍS decae anualmente, pero MEN aumenta.
* **Retiro (35+):** Probabilidad incremental de retiro a fin de temporada.

### 3.3 Rasgos (Traits - El Factor Humor/Táctico)
* *De Cristal:* Stats brutales, pero 20% de probabilidad de lesión en simulaciones de alta tensión.
* *Regalón de la Casa:* Atributos +20% de Local, -20% de Visita.
* *Especialista:* +3 en TÉC solo si el equipo juega con su formación favorita (ej. 4-3-3).

## 4. Motor Táctico y de Partidos (La Simulación)

### 4.1 Zonas y Formación
* $Poder\ Defensivo = \sum (DEF \times 1.5 + FÍS \times 0.5)$
* $Poder\ Mediocampo = \sum (TÉC \times 1.0 + FÍS \times 1.0)$
* $Poder\ Ofensivo = \sum (TÉC \times 1.5 + FÍS \times 0.5)$

### 4.2 El Choque Táctico
1.  **Presión Escénica:** Compara MEN del jugador vs Nivel de Presión del partido (Local/Visita + Importancia). Si MEN es menor, debuff del -30%. Si es mayor, buff del +10%.
2.  **Chances:** Quien gana el mediocampo genera más volumen de ataques.
3.  **Resolución (RNG):** Probabilidad de gol basada en $Ofensiva\ vs\ Defensa$. Tirada de dados. El ARQ rival tiene tirada de salvación.

## 5. Economía, Bases de Datos e Infraestructura
* **Bases de Datos Estáticas:** El juego contará con diccionarios de Equipos (parodias de primera y ascenso) y Estadios (nombres parodia con capacidad/nivel asignado).
* **Bloqueo Blando (Infraestructura):** Puedes ascender sin buen estadio, pero la mala infraestructura limita la "Caja" generada y espanta a los fichajes de nivel, llevándote a la quiebra orgánica en primera división.

## 6. Reglas de Desarrollo (Para la IA)
* **Entorno:** VS Code + Continue.dev.
* **Lenguaje:** [A DEFINIR - Python sugerido para el motor, Godot/GDScript para el juego final].
* **Regla Estricta:** Modificaciones quirúrgicas. Prohibido refactorizar sin preguntar. Separar lógica matemática de las bases de datos.