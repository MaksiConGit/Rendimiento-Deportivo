import os
import datetime
import sys

RENDIMIENTO_SALTOS_DIR = os.getcwd() + "\\config\\RENDIMIENTO_SALTOS.txt"
RENDIMIENTO_CAMINAR_DIR = os.getcwd() + "\\config\\RENDIMIENTO_CAMINAR.txt"

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

fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
respuesta = input("\n¿Cuántos pasos hiciste ayer en 60 minutos?\n\n")

with open(RENDIMIENTO_CAMINAR_DIR, "a", encoding="utf-8") as rendimiento:
    rendimiento.write(respuesta + " - " + fecha_actual + "\n")

print("\nDatos almacenados.\n")

fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
respuesta = input("\n¿Cuántos saltos hiciste hoy en 30 minutos?\n\n")

with open(RENDIMIENTO_SALTOS_DIR, "a", encoding="utf-8") as rendimiento:
    rendimiento.write(respuesta + " - " + fecha_actual + "\n")

print("\nDatos almacenados.\n")

while True:

    opcion = input("\n\n¿Quieres consultar los datos? (y/n)\n\n")

    if opcion == "y":

        datos_agrupados_caminar = obtener_datos_agrupados(RENDIMIENTO_CAMINAR_DIR)
        print("\n\nDatos de Caminar:\n")
        for clave, datos in datos_agrupados_caminar.items():
            print(f"{clave}")
            for pasos in datos['pasos_saltos']:
                print(f"{pasos} pasos")
            total_pasos_semana = sum(datos['pasos_saltos'])
            print(f"\nTotal de pasos en la semana: {total_pasos_semana}\n")

        # Imprimir total de pasos de caminar
        total_pasos_caminar = sum(sum(datos['pasos_saltos']) for datos in datos_agrupados_caminar.values())
        print(f"\nTotal de pasos: {total_pasos_caminar}\n")

        datos_agrupados_saltos = obtener_datos_agrupados(RENDIMIENTO_SALTOS_DIR)
        print("Datos de Saltos:\n")
        for clave, datos in datos_agrupados_saltos.items():
            print(f"{clave}")
            for saltos in datos['pasos_saltos']:
                print(f"{saltos} saltos")
            total_saltos_semana = sum(datos['pasos_saltos'])
            print(f"\nTotal de saltos en la semana: {total_saltos_semana}\n")

            # Calcular y mostrar el porcentaje de mejora
            if clave != "Semana 1":
                semana_anterior = f"Semana {int(clave.split()[1]) - 1}"
                if semana_anterior in datos_agrupados_saltos:
                    saltos_semana_anterior = sum(datos_agrupados_saltos[semana_anterior]["pasos_saltos"])
                    porcentaje_mejora = ((total_saltos_semana - saltos_semana_anterior) / saltos_semana_anterior) * 100
                    print(f"Porcentaje de mejora: {porcentaje_mejora:.2f}%\n")

        # Imprimir total de saltos generales
        total_saltos = sum(sum(datos['pasos_saltos']) for datos in datos_agrupados_saltos.values())
        print(f"\nTotal de saltos: {total_saltos}")

        input("\n\nPresione ENTER para salir")
        sys.exit()

    elif opcion == "n":
        sys.exit()