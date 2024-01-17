import os
import datetime
import sys
from colorama import Fore, Back, Style, init

if not os.path.exists("D:\\Maksi\\Escritorio\\Scripts automatizados\\Rendimiento Deportivo\\config\\"):
    os.makedirs("config")

RENDIMIENTO_SALTOS_DIR = os.getcwd() + "D:\\Maksi\\Escritorio\\Scripts automatizados\\Rendimiento Deportivo\\config\\RENDIMIENTO_SALTOS.txt"
RENDIMIENTO_CAMINAR_DIR = os.getcwd() + "D:\\Maksi\\Escritorio\\Scripts automatizados\\Rendimiento Deportivo\\config\\RENDIMIENTO_CAMINAR.txt"

def obtener_datos_agrupados(rendimiento_path):
    with open(rendimiento_path, "r", encoding="utf-8") as rendimiento:
        lineas = rendimiento.readlines()

    datos_agrupados = {}
    primer_registro = True
    primer_dia = None

    for linea in lineas:
        partes = linea.strip().split(" - ")
        if len(partes) == 2:
            fecha_registro = datetime.datetime.strptime(partes[1], "%Y-%m-%d %H:%M:%S")

            if primer_registro:
                primer_dia = fecha_registro
                primer_registro = False

            dias_pasados = (fecha_registro - primer_dia).days
            semana_actual = dias_pasados // 7 + 1  # Agrupar en semanas

            clave = f"Semana {semana_actual}"
            pasos_saltos = int(partes[0])

            if clave in datos_agrupados:
                datos_agrupados[clave]["pasos_saltos"].append(pasos_saltos)
            else:
                datos_agrupados[clave] = {"pasos_saltos": [pasos_saltos]}

    return datos_agrupados

init()

print(Fore.YELLOW + "\n\nBuen día" + Fore.BLUE + "\n\nRegistra tu rendimiento deportivo\n\n" + Fore.RESET)

fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
respuesta = input("\n¿Cuántos pasos hiciste ayer?\n\n")

with open(RENDIMIENTO_CAMINAR_DIR, "a", encoding="utf-8") as rendimiento:
    rendimiento.write(respuesta + " - " + fecha_actual + "\n")

print(Fore.GREEN + "\nDatos almacenados.\n" + Fore.RESET)

fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
respuesta = input("\n¿Cuántos saltos hiciste hoy en 30 minutos?\n\n")

with open(RENDIMIENTO_SALTOS_DIR, "a", encoding="utf-8") as rendimiento:
    rendimiento.write(respuesta + " - " + fecha_actual + "\n")

print(Fore.GREEN + "\nDatos almacenados.\n" + Fore.RESET)

while True:

    opcion = input("\n\n¿Quieres consultar los datos? (" + Fore.GREEN + Style.BRIGHT + "y"
                   + Fore.RESET + Style.RESET_ALL + "/" + Fore.RED + Style.BRIGHT + "n"
                   + Fore.RESET + Style.RESET_ALL + ")\n\n")

    if opcion == "y":

        datos_agrupados_caminar = obtener_datos_agrupados(RENDIMIENTO_CAMINAR_DIR)
        print(Fore.MAGENTA + "\n\nDatos de Caminar:\n" + Fore.RESET)
        for clave, datos in datos_agrupados_caminar.items():
            print(Fore.BLACK + Style.BRIGHT + f"{clave}" + Fore.RESET + Style.RESET_ALL)

            # Enumerar los pasos en la semana
            for i, pasos in enumerate(datos['pasos_saltos'], start=1):
                print(Fore.MAGENTA + f"{i}. " + Fore.RESET + f"{pasos:,} pasos")  # Utilizar el formato de cadena con comas

            total_pasos_semana = sum(datos['pasos_saltos'])
            print(Fore.LIGHTMAGENTA_EX + f"\nTotal de pasos en la semana: {total_pasos_semana:,}\n" + Fore.LIGHTMAGENTA_EX)

        # Imprimir total de pasos de caminar
        total_pasos_caminar = sum(sum(datos['pasos_saltos']) for datos in datos_agrupados_caminar.values())
        print(Fore.LIGHTYELLOW_EX + f"\nTotal de pasos: {total_pasos_caminar:,}\n")

        datos_agrupados_saltos = obtener_datos_agrupados(RENDIMIENTO_SALTOS_DIR)
        print(Fore.CYAN + "Datos de Saltos:\n" + Fore.RESET)
        for clave, datos in datos_agrupados_saltos.items():
            print(Fore.BLACK + Style.BRIGHT + f"{clave}" + Fore.RESET + Style.RESET_ALL)

            # Enumerar los saltos en la semana
            for i, saltos in enumerate(datos['pasos_saltos'], start=1):
                print(Fore.CYAN + f"{i}. " + Fore.RESET + f"{saltos:,} saltos")  # Utilizar el formato de cadena con comas

            total_saltos_semana = sum(datos['pasos_saltos'])
            print(Fore.CYAN + f"\nTotal de saltos en la semana: {total_saltos_semana:,}\n" + Fore.RESET)

            # Calcular y mostrar el porcentaje de mejora
            if clave != "Semana 1":
                    semana_anterior = f"Semana {int(clave.split()[1]) - 1}"
                    if semana_anterior in datos_agrupados_saltos:
                        saltos_semana_anterior = sum(datos_agrupados_saltos[semana_anterior]["pasos_saltos"])
                        porcentaje_mejora = ((total_saltos_semana - saltos_semana_anterior) / saltos_semana_anterior) * 100

                        # Seleccionar el color en función del signo del porcentaje
                        color_porcentaje = Fore.RED if porcentaje_mejora < 0 else Fore.GREEN

                        print(f"Porcentaje de mejora: {color_porcentaje}{porcentaje_mejora:.2f}%{Fore.RESET}\n")
                    

        # Imprimir total de saltos generales
        total_saltos = sum(sum(datos['pasos_saltos']) for datos in datos_agrupados_saltos.values())
        print(Fore.LIGHTYELLOW_EX + f"\nTotal de saltos: {total_saltos:,}" + Fore.RESET)

        input("\n\nPresione ENTER para salir")
        sys.exit()

    elif opcion == "n":
        sys.exit()