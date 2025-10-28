import csv
from pathlib import Path
from datetime import datetime
import os 
import json

# === 1. Leer el archivo ===
ruta_csv = Path('/Users/valentinobustamante/Downloads/actividad_2.csv')

fechas = []           # lista para guardar las fechas
contador_dias = {}    # diccionario vacio para contar entrenamientos por día
contador_campeones = {} #diccionario vacio para contar campeones
contador_findesemana = {} #diccionario vacio para contar solo los fines de semana



with open(ruta_csv, encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo) #leo las filas como diccionarios

    # ===  Procesar cada fila ===
    for fila in lector:
        texto = fila['timestamp'] #Obtengo la fecha (en formato str)
        fecha = datetime.strptime(texto, "%Y-%m-%d %H:%M") #La convierto en un objeto
        dia = fecha.strftime("%A") #Me quedo con el nombre del dia

        # Si el día no existe en el diccionario, lo inicializo
        if dia not in contador_dias:
            contador_dias[dia] = 0

        # Sumamos 1 cada vez que aparece ese día
        contador_dias[dia] += 1

        #Contamos los campeones 
        campeon = fila['campeon']
        if campeon not in contador_campeones:
            contador_campeones[campeon] = 0
        contador_campeones[campeon] += 1

        #Contamos por fin de semana 
        if dia in ["Saturday", "Sunday"]:
            campeon = fila['campeon']

            if campeon not in contador_findesemana:
                contador_findesemana[campeon] = 0

            contador_findesemana[campeon] += 1

        # Guardamos la fecha para calcular el rango luego
        fechas.append(fecha)



# === 2. Mostrar cantidad de entrenamientos por día ===
print("\n2. Entrenamientos por día de la semana:")
for dia, cantidad in contador_dias.items():
    print(f"  {dia}: {cantidad}")

# === 3. Día(s) con más entrenamientos ===
maximo = max(contador_dias.values())
dias_maximos = [dia for dia, cant in contador_dias.items() if cant == maximo]

print(f"\n3. Máximo de entrenamientos en un día: {maximo}")
print("Día(s) con más entrenamientos:")
for dia in dias_maximos:
    print(f"  - {dia}")

# === 4. Diferencia entre primer y último entrenamiento ===
primero = min(fechas)
ultimo = max(fechas)
diferencia = (ultimo - primero).days #el days nos ayuda para 

print(f"\n4. Días entre el primer y último entrenamiento: {diferencia}")

# === 5. Campeón con más entrenamientos ===
max_entrenamientos = max(contador_campeones.values()) #Obtenemos el valor mas grande del diccionario 
campeones_top = [c for c, n in contador_campeones.items() if n == max_entrenamientos] #Usamos el concepto de list comprehension, donde recorremos el diccionario y creamos una nueva lista
#c corresponde al campeor que seria la clave y n al valor que seria los dias que entreno, si hay mas de un campeon con la misma cantidad de entrenamientos los mostramos igual
print("\n5. Campeón(es) que más entrenó:")
for campeon in campeones_top:
    print(f"  - {campeon} ({max_entrenamientos} entrenamientos)")

# === 6. Promedio de entrenamientos por día ===
total_entrenamientos = sum(contador_dias.values())     # suma total de entrenamientos, aprovecho que ya tengo el contador de dias   
cantidad_dias = len(contador_dias)                     # cuántos días distintos hubo
promedio = total_entrenamientos / cantidad_dias

print(f"\n6. Promedio de entrenamientos por día de la semana: {promedio:.2f}") #muestro resultado con 2 decimales

# === 7. Entrenamiento fin de semana ===
if contador_findesemana:  # para evitar error si no hay registros
    max_finde = max(contador_findesemana.values())
    campeones_finde = [c for c, n in contador_findesemana.items() if n == max_finde]

    print("\n7. Campeón(es) que más entrena los fines de semana:")
    for c in campeones_finde:
        print(f"  - {c} ({max_finde} entrenamientos)")
else:
    print("\n7. No hay entrenamientos registrados en fin de semana.")

# === 8. Crear archivo CSV con cantidad de entrenamientos por campeón ===
carpeta_salida = Path("salida")                          # carpeta de salida
carpeta_salida.mkdir(exist_ok=True)                      # la crea si no existe

ruta_salida_csv = carpeta_salida / "entrenamientos_por_campeon.csv"

with open(ruta_salida_csv, "w", newline='', encoding='utf-8') as salida:
    escritor = csv.writer(salida)
    escritor.writerow(["campeon", "cantidad"])            # encabezado del archivo

    for campeon, cantidad in contador_campeones.items():
        escritor.writerow([campeon, cantidad])             # escribimos cada fila

print(f"\n8. Archivo CSV creado en: {ruta_salida_csv}")

# === 9. Crear archivo JSON con resumen general ===
carpeta_salida = Path("salida")
carpeta_salida.mkdir(exist_ok=True)

ruta_json = carpeta_salida / "resumen_entrenamientos.json"

# Estructura de datos para el JSON
resumen = {
    "total_registros": sum(contador_dias.values()),
    "dias": {}
}

# Volvemos a leer el archivo para generar el detalle por día y campeón
with open(ruta_csv, newline='', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        texto = fila['timestamp']
        fecha = datetime.strptime(texto, "%Y-%m-%d %H:%M")
        dia = fecha.strftime("%A")
        campeon = fila['campeon']

        # Si el día no está lo creamos
        if dia not in resumen["dias"]:
            resumen["dias"][dia] = {}

        # Sumamos 1 al contador de ese campeón en ese día
        if campeon not in resumen["dias"][dia]:
            resumen["dias"][dia][campeon] = 0
        resumen["dias"][dia][campeon] += 1

# Guardamos el archivo JSON
with open(ruta_json, "w", encoding='utf-8') as salida_json:
    json.dump(resumen, salida_json, indent=4, ensure_ascii=False)

print(f"\n9. Archivo JSON creado en: {ruta_json}")