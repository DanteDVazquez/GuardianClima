import csv
import pandas as pd
from collections import Counter
from google import genai
import os
import requests
import hashlib
from dotenv import load_dotenv
from datetime import datetime
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) #Esto ignora los avisos de depreciación de librerías, no son relevantes aqui
load_dotenv()

## Hashea las contraseñas antes de guardarlas en el csv. 
## Cuando inicias sesion, hashea la contraseña ingresada por el usuario y la compara con la contraseña ya hasheada guardada en el .csv
def passwordhasher(password):
    return hashlib.sha256(password.encode('cp1252')).hexdigest()
## Aca se muestran las opciones y se espera un input, el menu funciona derivandote a las otras funciones dependiendo lo que elijas y verificando que toques una opcion valida
def Pre_Login():
    if not os.path.exists("usuarios_simulados.csv"):
        with open("usuarios_simulados.csv", "w", newline='') as archivo: ## Aca se verifica si estan creados o no el archivo .csv y si no lo esta, lo crea para continuar el flujo del programa
            archivo.write("usuario,contrasena\n")
    with open("usuarios_simulados.csv", "r", encoding='cp1252') as archivo:
        print("\nBienvenido/a al sistema!\n")
        print("Por favor, inicia sesión o registrate.")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")

        input_1 = input("Su elección: ")

        if input_1 == "1":
            iniciar_sesion()
        elif input_1 == "2":
            registrarse()
        elif input_1 == "3":
            salir()
        else:
            print("Elija una opción válida\n")
            Pre_Login()

## Este menu funciona de manera practicamente igual al de Pre_Login
##
def iniciar_sesion():
    print("Iniciar sesión")
    nombre_usuario = input("Ingresa tu nombre de usuario: ") 
    encontrado = False
    with open("usuarios_simulados.csv", "r", newline='') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
           if len(fila) >= 2:
                usuario, contrasena_correcta = fila[0], fila[1]
                if usuario == nombre_usuario:
                    encontrado = True
                    break
        if not encontrado:
            print("Usuario no encontrado, por favor, ¿desea intentar de nuevo?")
            def intento():
                intento = input("s/n: ").lower()
                if intento == "s":
                    iniciar_sesion()
                elif intento == "n":
                    Pre_Login()
                else:
                    print("Por favor, selecciona una opcion valida")
                    iniciar_sesion()
            intento()
        else:
            contrasena = input("Ingresa tu contrasena: ")
            if passwordhasher(contrasena) == contrasena_correcta:  ## Aca se llama a la funcion passwordhasher justamente para hashear las contras y que tenga mayor seguridad 
                print("Bienvenido/a", nombre_usuario, "!")
                menu_principal(nombre_usuario)
            else:
                print("Contraseña incorrecta")
                eleccion = input("¿Deseas intentarlo de nuevo? (s/n): ").strip().lower()
                if eleccion == "s":
                    iniciar_sesion()
                elif eleccion == "n":
                    Pre_Login()
                else:
                    intento_invalido()

def registrarse():
    nombre_usuario = input("Ingresa tu nombre de usuario: ")
    encontrado = False
    
    if os.path.exists("usuarios_simulados.csv"):
        with open("usuarios_simulados.csv", "r", newline='', encoding='cp1252') as f:
            lector = csv.reader(f)
            for fila in lector:
                if fila and fila[0] == nombre_usuario:
                    encontrado = True
                    break
    
    if not encontrado:
        with open("usuarios_simulados.csv", "a", newline='', encoding='cp1252') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([nombre_usuario, ""])
        
        print("Bienvenido/a", nombre_usuario, "!")
        crear_contrasena(nombre_usuario) ##Una vez creado correctamente el nombre de usuario te lleva a la funcion de crear contraseña
    else:
        print("El usuario ya existe")
        repeat = input("Deseas intentarlo de nuevo? (s/n): ").strip().lower()
        if repeat.lower() == "s":
            registrarse()
        else:
            Pre_Login()

def crear_contrasena(nombre_usuario):
    while True:
        print("Es altamente recomendable no utilizar datos personales como nombres o fechas.")
        print("tambien se recomienda combinar tanto numeros como letras.")
        contrasena = input("Ingresa una contraseña con al menos una mayuscula, mas de 8 caracteres y un caracter especial: ")
        tiene_mayuscula = any(c.isupper() for c in contrasena)
        numero_caracteres = len(contrasena) >= 8
        tiene_caracter_especial = any(c in "!@#$%^&*()_+{}|:\"<>?[]" for c in contrasena)
        
        if tiene_caracter_especial and tiene_mayuscula and numero_caracteres:
            break
        else:
            print("Contraseña inválida:")
            if not tiene_mayuscula:
                print("- Debe contener al menos una mayúscula.")
            if not numero_caracteres:
                print("- Debe tener al menos 8 caracteres.")
            if not tiene_caracter_especial:
                print("- Debe contener al menos un caracter especial.")
    
    lineas = [] ## Esto es importantisimo. Gracias a esto podemos comprobar que la contraseña pertenezca al usuario y no a otro.
    with open("usuarios_simulados.csv", "r", encoding='cp1252') as archivo:
        lector = csv.reader(archivo)
        lineas = list(lector)
    
    for linea in lineas:
        if linea[0] == nombre_usuario:
            if len(linea) > 1:
                linea[1] = passwordhasher(contrasena)
            else:
                linea.append(passwordhasher(contrasena))
    
    with open("usuarios_simulados.csv", "w", newline='', encoding='cp1252') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(lineas)
    
    
    Pre_Login()

def intento_invalido():
    print("Entrada incorrecta")
    eleccion = input("Deseas intentarlo de nuevo? (s/n): ").strip().lower()
    if eleccion == "s":
        iniciar_sesion()
    elif eleccion == "n":
        Pre_Login()
    else:
        intento_invalido()
        return

def consultar_clima(nombre_usuario):
    if not os.path.exists("historial_global.csv"):
        with open("historial_global.csv", "w", newline='', encoding='cp1252') as archivo:
            archivo.write("nombre_usuario,ciudad,temperatura,condicion_clima,humedad,viento_kmh,fecha_hora\n")
    print("Consultar Clima Actual y guardar en historial global")
    while True:
        ciudad = input("Ingresa el nombre de la ciudad: ").strip().lower()
        if not ciudad:
            print("El nombre de la ciudad no puede estar vacío. Inténtalo de nuevo.")
            continue
        break
    #Reemplazar por tu API KEY de OpenWeatherMap en el archivo .env
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"

    try:
        respuesta = requests.get(url)
        datos = respuesta.json()

        if respuesta.status_code == 200:
            temperatura = datos["main"].get("temp", "N/A")
            humedad = datos["main"].get("humidity", "N/A")
            condicion_clima = datos["weather"][0].get("description", "N/A") if datos.get("weather") else "N/A"
            viento_kmh = datos["wind"].get("speed", 0) * 3.6
            fecha_hora = (datetime.utcnow() + __import__('datetime').timedelta(hours=-3)).strftime("%Y-%m-%d %H:%M:%S")

            print(f"Ciudad: {ciudad}")
            print(f"Temperatura: {temperatura}°C")
            print(f"Humedad: {humedad}%")
            print(f"Descripción del Clima: {condicion_clima}")
            print(f"Velocidad del Viento: {viento_kmh:.2f} km/h")
            print(f"Fecha y Hora: {fecha_hora}")

            guardar_en_historial(nombre_usuario, ciudad, temperatura, condicion_clima, humedad, viento_kmh, fecha_hora)
            return temperatura, condicion_clima
        else:
            print(f"\nError al consultar el clima: {datos.get('message', 'Error desconocido')}\n")

    except requests.exceptions.RequestException as e: ##Usamos "e" como variable para cualquier error que nos pueda llegar a dar el programa, asi lo mostramos al usuario
        print(f"Error de conexión: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

def guardar_en_historial(nombre_usuario, ciudad, temperatura, condicion_clima, humedad, viento_kmh, fecha_hora):
    try:
        with open("historial_global.csv", "a", newline='', encoding='cp1252') as archivo:
            escritor = csv.writer(archivo)
            if archivo.tell() == 0:
                escritor.writerow(["nombre_usuario", "ciudad", "temperatura", "condicion_clima", "humedad", "viento_kmh", "fecha_hora"])
            escritor.writerow([nombre_usuario, ciudad, temperatura, condicion_clima, humedad, viento_kmh, fecha_hora])
    except Exception as e:
        print(f"Error al guardar en el historial: {e}")

def ver_historial_personal(nombre_usuario):
    print("Ver Mi Historial Personal de Consultas por Ciudad")
    ciudad = input("Ingresa el nombre de la ciudad: ").strip().lower()

    try:
        with open("historial_global.csv", "r", encoding='cp1252') as archivo:
            lector = csv.reader(archivo)
            encabezados = next(lector, None)

            historial_filtrado = []

            for fila in lector:
                if len(fila) >= 7:
                    usuario, ciudad_fila, temperatura, condicion_clima, humedad, viento_kmh, fecha_hora = fila
                    if usuario == nombre_usuario and ciudad_fila.lower() == ciudad.lower():
                        historial_filtrado.append((fecha_hora, temperatura, condicion_clima))

            if historial_filtrado:
                print(f"Historial de consultas para la ciudad '{ciudad}' del usuario '{nombre_usuario}':")
                print("Fecha y hora | Temperatura | Condición del clima")
                print("------------------------------------------------")
                for entrada in historial_filtrado:
                    print(f"{entrada[0]} | {entrada[1]}°C | {entrada[2]}")
            else:
                print(f"No se encontraron registros para la ciudad '{ciudad}' del usuario '{nombre_usuario}'.")

    except FileNotFoundError:
        print("\nAún no has realizado consultas\n")
    except Exception as e:
        print(f"Error al leer el historial: {e}")

def estadisticas_globales():
    print("Estadísticas Globales de Uso y Exportar Historial Completo")

    try:
        with open("historial_global.csv", "r", encoding='cp1252') as archivo:
            lector = csv.reader(archivo)
            encabezados = next(lector, None)

            if encabezados:
                total_consultas = 0
                suma_temperaturas = 0.0
                ciudades_contador = Counter()

                for fila in lector:
                    if len(fila) >= 7:
                        _, ciudad, temperatura, _, _, _, _ = fila
                        temperatura = float(temperatura)

                        ciudades_contador[ciudad] += 1
                        total_consultas += 1
                        suma_temperaturas += temperatura

                ciudad_mas_consultada = ciudades_contador.most_common(1)[0][0] if ciudades_contador else "N/A"
                temperatura_promedio = suma_temperaturas / total_consultas if total_consultas > 0 else 0.0

                print(f"Ciudad más consultada: {ciudad_mas_consultada}")
                print(f"Número total de consultas realizadas para todas las ciudades: {total_consultas}")
                print(f"Número total de consultas para {ciudad_mas_consultada}: {ciudades_contador[ciudad_mas_consultada]}")
                print(f"Temperatura promedio registrada: {temperatura_promedio:.2f}°C")

    except FileNotFoundError:
        print("\nAún no has realizado consultas\n")
    except Exception as e:
        print(f"Error al leer las estadísticas: {e}")
    #Reemplaza tu API KEY de gemini en el archivo .env
def nueva_consulta_ia(nombre_usuario):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    datoclima1= consultar_clima(nombre_usuario)
    
    prompt = (
        f"Considerando la temperatura y la condición climática especificadas en {datoclima1}, indica brevemente cómo debería vestirse una persona. La recomendación debe ser lógica, clara y útil. Usá un lenguaje natural pero formal y académico. No utilices negritas, asteriscos ni ningún formato especial."
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    
    print("\n" + response.text + "\n")
    return menu_principal(nombre_usuario)

def consulta_historial_ia(nombre_usuario):
    ruta = "historial_global.csv"
    if not os.path.exists(ruta):
        print(f"El usuario {nombre_usuario} aún no ha realizado consultas de clima.")
        choice = input("¿Desea hacer una nueva consulta? (s/n): ").strip().lower()
        if choice == "s":
            return nueva_consulta_ia(nombre_usuario)
        return menu_principal(nombre_usuario)

    df = pd.read_csv(ruta)
    df_user = df[df["nombre_usuario"] == nombre_usuario]
    if df_user.empty:
        print(f"No se encontraron datos para el usuario {nombre_usuario}.")
        choice = input("¿Quiere realizar una nueva consulta? (s/n): ").strip().lower()
        if choice == "s":
            return nueva_consulta_ia(nombre_usuario)
        return menu_principal(nombre_usuario)

    ultima = df_user.iloc[-1]
    temp, hum, condi = ultima["temperatura"], ultima["humedad"], ultima["condicion_clima"]
    print(f"Temperatura: {temp}°C\nHumedad: {hum}%\nCondición climática: {condi}\n")
    #Reemplaza tu API KEY de gemini en el archivo .env
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = (
        f"En base a {temp} grados Celsius, {condi} y {hum}% de humedad, indica brevemente cómo debería vestirse una persona. La recomendación debe ser lógica, clara y útil. Usá un lenguaje natural pero formal y académico. No utilices negritas, asteriscos ni ningún formato especial."
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    print(response.text + "\n")
    return menu_principal(nombre_usuario)

def consejo_ia_como_me_visto_hoy(nombre_usuario):
    while True:
        print("¿Qué deseas hacer?")
        print(" 1. Realizar una nueva consulta de clima")
        print(" 2. Usar los datos de mi última consulta")
        opcion = input("Ingrese una opción (1-2): ").strip()

        if opcion == "1":
            try:
                return nueva_consulta_ia(nombre_usuario)
            except Exception as e:
                print(f"Ocurrio el siguiente error: {e}") ##Muestra el error correspondiente para dar correcto feedback
                mostrar_menu()
        elif opcion == "2":
            try:
                return consulta_historial_ia(nombre_usuario)
            except Exception as e:
                print(f"Error de conexión: {e}") 
                mostrar_menu()
def creditos():
    print("""
********************************************************************
*                       GUARDIÁN CLIMA                             *
********************************************************************

GuardianClima es una aplicación que se desarrolló con el propósito
de proveer información del clima al Usuario. Su función se basa en asesorar
al usuario dependiendo las consultas realizadas, brindando información del
clima en la zona geográfica solicitada la cual queda registrada para
también realizar estadísticas globales y consejos de vestimenta mediante IA.

********************************************************************
*                       MANUAL DE USO                              *
********************************************************************

Una vez iniciada la sesión, se presentaran las siguientes opciones:

- OPCIÓN 1: Escribir la ciudad en mente para realizar consulta climática de la misma.
- OPCIÓN 2: Escribir una ciudad previamente consultada para obtener información del historial.
- OPCIÓN 3: Permite obtener las estadísticas globales de las consultas.
- OPCIÓN 4: Brinda una recomendación de vestimenta ofrecida por IA basándose en la última consulta.
- OPCIÓN 5: Acceder a este mismo texto descriptivo.
- OPCIÓN 6: Cerrar sesión y volver al menú de acceso.

********************************************************************
*               INTERACCIÓN CON EL MENÚ DE ACCESO                  *
********************************************************************

- REGISTRARSE (para nuevos usuarios): 
  Colocar nombre no registrado por otro usuario. Si es válido,
  ingresar contraseña que cumpla con los caracteres pedidos.
  
- INICIAR SESIÓN: 
  Colocar credenciales previamente registradas por el usuario.
  
- SALIR: 
  Termina la ejecución del programa.

********************************************************************
*         REGISTRO DE USUARIOS Y VALIDACIÓN DE CONTRASEÑAS         *
********************************************************************

El sistema permite registrar nuevos usuarios simulando el almacenamiento
en un archivo CSV. Las contraseñas ingresadas son evaluadas por una
función de validación que verifica que cumplan con al menos tres
criterios de seguridad (longitud mínima, caracteres especiales y uso de
mayúsculas), fomentando buenas prácticas en ciberseguridad.

********************************************************************
*       ADVERTENCIA SOBRE EL ALMACENAMIENTO DE CREDENCIALES        *
********************************************************************

A diferencia de un almacenamiento sin encriptado, en este proyecto se
implementó hashing con SHA-256 para proteger las contraseñas de los
usuarios. De esta forma, las contraseñas no se guardan directamente, sino
como un valor encriptado, lo que mejora significativamente la seguridad.

********************************************************************
*         CONSULTA DEL CLIMA Y GUARDADO DE HISTORIAL               *
********************************************************************

Tras crearse una cuenta e iniciar sesión, el usuario puede consultar
el clima actual de cualquier ciudad. Para esto, la aplicación se conecta
a la API de OpenWeatherMap, tomando datos como temperatura, humedad,
viento y descripción del clima. Cada consulta se guarda automáticamente
en el archivo historial_global.csv, incluyendo usuario, ciudad, fecha y
condiciones climáticas.

********************************************************************
*       ESTADÍSTICAS GLOBALES Y PREPARACIÓN PARA GRÁFICOS          *
********************************************************************

La aplicación procesa el archivo global de historial para calcular
estadísticas útiles como la ciudad más consultada, la temperatura
promedio y la cantidad total de consultas. Estos datos pueden exportarse
y visualizarse mediante gráficos (barras, líneas, torta) usando
herramientas externas como Excel o Google Sheets.

********************************************************************
*       INTERACCIÓN CON IA PARA CONSEJOS DE VESTIMENTA             *
********************************************************************

Utilizando los datos de clima recientes, la aplicación puede enviar un
prompt a una API de Inteligencia Artificial generativa (como Google Gemini).
La IA devuelve un consejo personalizado sobre cómo vestirse según el clima
actual, mejorando la experiencia del usuario.

********************************************************************
*                   INTEGRANTES DEL EQUIPO                         *
********************************************************************
- JUAN CRUZ ALMAZÁN
- DANTE VAZQUEZ

def mostrar_menu():
    print("")
    print("============MENU PRINCIPAL=============")
    print("1.Consultar clima actual y guardar en historial global")
    print("2.Ver mi historial personal de consultas por ciudad")
    print("3.Estadísticas globales de uso y exportar historial completo")
    print("4.Consejo IA: ¿Cómo me visto hoy? ")
    print("5.Acerca de...")
    print("6.Cerrar sesión")

def menu_principal(nombre_usuario):
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-6): ")

        if opcion == '1':
            consultar_clima(nombre_usuario) 
        elif opcion == '2':
            ver_historial_personal(nombre_usuario)
        elif opcion == '3':
            estadisticas_globales()
        elif opcion == '4':
            consejo_ia_como_me_visto_hoy(nombre_usuario)
        elif opcion == '5':
            creditos()
        elif opcion == '6':
            cerrar_sesion()
        else:
            print("Opción no válida. Por favor, selecciona entre 1 y 6.")

def salir():
    print("Saliendo...")
    exit()

def cerrar_sesion():
    print("Cerrando sesión")
    Pre_Login()

Pre_Login()
