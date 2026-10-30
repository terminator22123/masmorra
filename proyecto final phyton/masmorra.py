import random

nombres_monstruos = ["Slime", "Murciélago", "Esqueleto", "Goblin", "Orco", "cofre trampa"]
vidas_monstruos = [20, 25, 35, 40, 55, 30]
ataques_monstruos = [4, 6, 8, 9, 12, 10]
objetos_posibles = ["Poción", "Espada", "pocima de ataque", "Llave", "Moneda"]


class Heroe:
    def __init__(self, nombre):
        self.nombre = nombre
        self.__vida = 100
        self.ataque = 15
        self.inventario = ["Poción", "Poción", "pocima de ataque"]

    def obtener_vida(self):
        return self.__vida

    def recibir_danio(self, cantidad):
        self.__vida = max(0, self.__vida - cantidad)

    def curar(self, cantidad):
        self.__vida = min(100, self.__vida + cantidad)

    def esta_vivo(self):
        return self.__vida > 0


class Monstruo:
    def __init__(self, nombre, vida, ataque):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque

    def atacar(self):
        return random.randint(1, self.ataque)

    def recibir_danio(self, cantidad):
        self.vida = max(0, self.vida - cantidad)

    def esta_vivo(self):
        return self.vida > 0


class Dragon(Monstruo):
    def __init__(self):
        super().__init__("Dragón", 80, 15)

    def aliento_de_fuego(self):
        return self.atacar() * 2


def pedir_nombre():
    while True:
        nombre = input("¿Cómo se llama tu héroe? ").strip()
        if 2 <= len(nombre) <= 12:
            return nombre
        print("El nombre debe tener entre 2 y 12 caracteres. Probá otra vez.")


def crear_monstruo():
    indice = random.randint(0, len(nombres_monstruos) - 1)
    return Monstruo(
        nombres_monstruos[indice],
        vidas_monstruos[indice],
        ataques_monstruos[indice]
    )


def mostrar_estado(heroe, monstruo):
    print(f"\n{heroe.nombre}: {heroe.obtener_vida()}/100")
    print(f"Ataque del héroe: {heroe.ataque}")
    print(f"{monstruo.nombre}: {monstruo.vida} de vida")


def usar_pocion(heroe):
    if "Poción" not in heroe.inventario:
        print("No te quedan pociones de curación.")
        return False

    if heroe.obtener_vida() == 100:
        print("Ya tenés la vida al máximo. Guardá la poción.")
        return False

    heroe.inventario.remove("Poción")
    vida_anterior = heroe.obtener_vida()
    heroe.curar(25)
    recuperada = heroe.obtener_vida() - vida_anterior

    print(f"Usaste una poción y recuperaste {recuperada} puntos de vida.")
    return True


def usar_pocion_ataque(heroe):
    if "pocima de ataque" not in heroe.inventario:
        print("No tenés ninguna poción de ataque.")
        return False

    heroe.inventario.remove("pocima de ataque")
    heroe.ataque *= 2

    print("¡Usaste la poción de ataque!")
    print(f"¡Tu ataque ahora es de {heroe.ataque}!")
    print("El efecto dura durante el resto de la partida.")
    return True


def combate(heroe, monstruo, es_dragon=False):
    articulo = "el" if es_dragon else "un"
    print(f"\n¡Apareció {articulo} {monstruo.nombre}!")
    turnos = 0

    while heroe.esta_vivo() and monstruo.esta_vivo():
        mostrar_estado(heroe, monstruo)
        print("Inventario:", ", ".join(heroe.inventario) or "Vacío")

        accion = input(
            "\n¿Qué hacés? (atacar / curar / usar / huir): "
        ).strip().lower()

        if accion == "atacar":
            turnos += 1
            danio = random.randint(1, heroe.ataque)
            monstruo.recibir_danio(danio)
            print(
                f"{heroe.nombre} golpea a {monstruo.nombre} "
                f"y le saca {danio} de vida."
            )

            if monstruo.esta_vivo():
                if es_dragon and random.randint(1, 2) == 1:
                    danio_monstruo = monstruo.aliento_de_fuego()
                    print("¡El Dragón usa su aliento de fuego!")
                else:
                    danio_monstruo = monstruo.atacar()

                heroe.recibir_danio(danio_monstruo)
                print(
                    f"{monstruo.nombre} te ataca "
                    f"y te saca {danio_monstruo} de vida."
                )

        elif accion == "curar":
            if usar_pocion(heroe):
                turnos += 1

                if monstruo.esta_vivo():
                    danio_monstruo = monstruo.atacar()
                    heroe.recibir_danio(danio_monstruo)
                    print(
                        f"{monstruo.nombre} te ataca "
                        f"y te saca {danio_monstruo} de vida."
                    )

        elif accion == "usar":
            if usar_pocion_ataque(heroe):
                turnos += 1

                if monstruo.esta_vivo():
                    if es_dragon and random.randint(1, 2) == 1:
                        danio_monstruo = monstruo.aliento_de_fuego()
                        print("¡El Dragón usa su aliento de fuego!")
                    else:
                        danio_monstruo = monstruo.atacar()

                    heroe.recibir_danio(danio_monstruo)
                    print(
                        f"{monstruo.nombre} te ataca "
                        f"y te saca {danio_monstruo} de vida."
                    )

        elif accion == "huir":
            if es_dragon:
                print("¡No podés huir del Dragón!")
                turnos += 1

                danio_monstruo = monstruo.atacar()
                heroe.recibir_danio(danio_monstruo)
                print(
                    f"{monstruo.nombre} aprovecha tu intento de huida "
                    f"y te saca {danio_monstruo} de vida."
                )

            elif random.randint(1, 2) == 1:
                print("¡Lograste escapar! Pasás a la siguiente sala sin premio.")
                return "huida", turnos

            else:
                print("No pudiste escapar.")
                turnos += 1

                danio_monstruo = monstruo.atacar()
                heroe.recibir_danio(danio_monstruo)
                print(
                    f"{monstruo.nombre} te ataca "
                    f"y te saca {danio_monstruo} de vida."
                )

        else:
            print("Esa acción no existe. Probá otra vez.")

    if not heroe.esta_vivo():
        print(f"\n{heroe.nombre} fue derrotado...")
        return "derrota", turnos

    print(f"\n¡Venciste a {monstruo.nombre}!")
    return "victoria", turnos


def obtener_objeto(heroe):
    if random.randint(1, 2) == 1:
        objeto = random.choice(objetos_posibles)
        heroe.inventario.append(objeto)
        print(f"¡Encontraste un objeto: {objeto}!")

        if objeto == "Espada":
            heroe.ataque += 2
            print("La espada aumenta tu ataque en 2.")

        elif objeto == "pocima de ataque":
            print("Guardaste una poción de ataque.")
            print("Escribí 'usar' durante un combate para activarla.")

        elif objeto == "Poción":
            print("Guardaste una poción para recuperar vida.")

        elif objeto == "Llave":
            print("Guardaste una llave misteriosa.")

        elif objeto == "Moneda":
            print("Guardaste una moneda.")

    else:
        print("Esta vez no encontraste ningún objeto.")

def jugar(historial_resultados, historial_turnos,monstruos_vencidos, ultimo_inventario):
    heroe = Heroe(pedir_nombre())
    turnos_partida = 0
    resultado_final = "Derrota"

    for sala in range(1, 6):
        if not heroe.esta_vivo():
            break

        print(f"\n{'=' * 12} SALA {sala} de 5 {'=' * 12}")

        if sala == 5:
            monstruo = Dragon()
        else:
            monstruo = crear_monstruo()

        resultado, turnos = combate(heroe, monstruo, sala == 5)
        turnos_partida += turnos

        if resultado == "derrota":
            resultado_final = "Derrota"
            break

        elif resultado == "huida":
            continue

        else:
            monstruos_vencidos.append(monstruo.nombre)

            if sala == 5:
                resultado_final = "Victoria"
                print("\n¡GANASTE! ¡Derrotaste al Dragón y rescataste el tesoro!")
            else:
                obtener_objeto(heroe)

    historial_resultados.append(resultado_final)
    historial_turnos.append(turnos_partida)

    ultimo_inventario.clear()
    ultimo_inventario.extend(heroe.inventario)

    print(f"\nResultado de la partida: {resultado_final}")
    print("Inventario final:", heroe.inventario)


def mostrar_bestiario():
    bestiario = sorted(nombres_monstruos)

    print("\n--- BESTIARIO ---")
    for nombre in bestiario:
        print("-", nombre)

    print("- Dragón")


def mostrar_inventario(ultimo_inventario):
    print("\n--- INVENTARIO DE LA ÚLTIMA PARTIDA ---")

    if ultimo_inventario is None:
        print("Todavía no jugaste ninguna partida.")
    elif not ultimo_inventario:
        print("El inventario está vacío.")
    else:
        print(", ".join(ultimo_inventario))


def mostrar_estadisticas(historial_resultados, historial_turnos,
                    monstruos_vencidos):
    print("\n--- ESTADÍSTICAS ---")

    if not historial_resultados:
        print("Todavía no jugaste ninguna partida.")
        return

    victorias = historial_resultados.count("Victoria")
    derrotas = historial_resultados.count("Derrota")
    promedio = sum(historial_turnos) / len(historial_turnos)

    print(f"Partidas ganadas: {victorias}")
    print(f"Partidas perdidas: {derrotas}")
    print(f"Promedio de turnos por partida: {promedio:.2f}")

    indice_mayor_ataque = ataques_monstruos.index(max(ataques_monstruos))
    print(
        "Monstruo con más ataque: "
        f"{nombres_monstruos[indice_mayor_ataque]} "
        f"({ataques_monstruos[indice_mayor_ataque]} de ataque)"
    )

    unicos = []
    for nombre in monstruos_vencidos:
        if nombre not in unicos:
            unicos.append(nombre)

    if unicos:
        print("Monstruos vencidos alguna vez:", ", ".join(unicos))
    else:
        print("Todavía no venciste ningún monstruo.")


def menu():
    historial_resultados = []
    historial_turnos = []
    monstruos_vencidos = []
    ultimo_inventario = None

    while True:
        print("\n===== LA MAZMORRA DEL DRAGÓN =====")
        print("1. Jugar")
        print("2. Ver bestiario")
        print("3. Ver inventario de la última partida")
        print("4. Estadísticas")
        print("5. Salir")

        opcion = input("Elegí una opción: ").strip()

        if not opcion.isdigit():
            print("Ingresá un número del 1 al 5.")
            continue

        opcion = int(opcion)

        if opcion == 1:
            if ultimo_inventario is None:
                ultimo_inventario = []

            jugar(
                historial_resultados,
                historial_turnos,
                monstruos_vencidos,
                ultimo_inventario
            )

        elif opcion == 2:
            mostrar_bestiario()

        elif opcion == 3:
            mostrar_inventario(ultimo_inventario)

        elif opcion == 4:
            mostrar_estadisticas(
                historial_resultados,
                historial_turnos,
                monstruos_vencidos
            )

        elif opcion == 5:
            print("¡Gracias por jugar a La Mazmorra del Dragón!")
            break

        else:
            print("Opción inválida. Elegí un número del 1 al 5.")


if __name__ == "__main__":
    menu()
