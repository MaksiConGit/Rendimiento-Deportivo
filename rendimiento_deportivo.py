import os
import datetime

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


while True:

    print("\n\n¿Qué ejercicio hiciste hoy?")

    opcion = input("\n1. Caminar\n2. Saltar la soga\n3. Consultar datos\n\n")

    if opcion == "1":
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        respuesta = input("\n¿Cuántos pasos hiciste en 60 minutos?\n\n")

        with open(RENDIMIENTO_CAMINAR_DIR, "a", encoding="utf-8") as rendimiento:
            rendimiento.write(respuesta + " - " + fecha_actual + "\n")

    elif opcion == "2":
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        respuesta = input("\n¿Cuántos saltos hiciste en 30 minutos?\n\n")

        with open(RENDIMIENTO_SALTOS_DIR, "a", encoding="utf-8") as rendimiento:
            rendimiento.write(respuesta + " - " + fecha_actual + "\n")

    elif opcion == "3":
        datos_agrupados_caminar = obtener_datos_agrupados(RENDIMIENTO_CAMINAR_DIR)
        print("\nDatos de Caminar:\n")
        for clave, datos in datos_agrupados_caminar.items():
            print(f"{clave}")
            for pasos in datos['pasos_saltos']:
                print(f"{pasos} pasos")
            print()

        # Imprimir total de pasos de caminar
        total_pasos_caminar = sum(sum(datos['pasos_saltos']) for datos in datos_agrupados_caminar.values())
        print(f"Total de pasos: {total_pasos_caminar}\n\n")

        datos_agrupados_saltos = obtener_datos_agrupados(RENDIMIENTO_SALTOS_DIR)
        print("Datos de Saltos:\n")
        for clave, datos in datos_agrupados_saltos.items():
            print(f"{clave}")
            for saltos in datos['pasos_saltos']:
                print(f"{saltos} saltos")
            print()

        # Imprimir total de saltos generales
        total_saltos = sum(sum(datos['pasos_saltos']) for datos in datos_agrupados_saltos.values())
        print(f"Total de saltos: {total_saltos}")
