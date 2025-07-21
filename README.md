---

##  Autoría

Desarrollado por

DANTE VAZQUEZ (GitHub: https://github.com/DanteDVazquez)

JUAN CRUZ ALMAZAN


---
# Proyecto Clima + IA

Este proyecto combina datos climáticos reales (API de Weather) con respuestas generadas por inteligencia artificial (Gemini), y está desarrollado para ser ejecutado con Python.


---

## Requisitos previos

Antes de ejecutar el proyecto, asegurate de tener:

1. Python **3.10** o superior instalado (Se puede obtener en https://www.python.org/downloads/)
2. Acceso a una terminal y a un editor de texto o IDE
3. Cuenta de Google y de Openweathermap.

---

## Instalación de librerías necesarias

Abrir una terminal y ejecutar lo siguiente:

```
pip install --upgrade pip
pip install -q -U google-genai
pip install pandas
pip install python-dotenv
```

IMPORTANTE:

En caso de hacerlo desde windows y no tener pip o no poder instalar estas librerías, es necesario ejecutarlo desde un entorno virtual con los siguientes comandos (desde powershell, como administrador). En caso contrario, pasar directamente al bloque "Nota sobre las API keys".
```
Set-ExecutionPolicy Unrestricted
```
Este comando (Set-ExecutionPolicy Unrestricted) solo aplica si la computadora tiene restringida la ejecución de comandos desde powershell.
```
py -m venv venv
venv\Scripts\Activate.ps1
pip install --upgrade pip setuptools
pip install -q -U google-genai
pip install pandas
pip install python-dotenv
```
---

## Nota sobre las API keys (Weather y Gemini)

El proyecto necesita dos claves:

- `WEATHER_API_KEY`: clave de tu cuenta en [openweathermap.org/api](https://openweathermap.org/api)
- `GEMINI_API_KEY`: clave del modelo de IA generativa en [aistudio.google.com](https://aistudio.google.com/)

En openweathermap.org hay que crearse una cuenta y luego dirigirse al nombre de usuario del perfil propio. Al hacerle click, se mostrará un listado que permite acceder a la API key.

Una vez obtenidas tus claves, reemplazar:

+La clave de API de Weather y de Gemini en el archivo .env, en el área correspondiente. Asegurase que el archivo sea estrictamente .env y no env u otro. 

Guardar el archivo en el mismo directorio que el código de python.

Esto es indispensiable para el correcto funcionamiento del programa.

---

## ¿Cómo ejecutar la aplicación?

1. Abrir el archivo `GuardianClimaITBA_Grupo129.py` con python una vez instalas las librerías mencionadas anteriormente. En caso de hacerlo desde una terminal o powershell, asegurarse de encontrarse en el mismo directorio donde se encuentra el archivo de python.

Windows:
```
cd "$HOME\Reemplaza_aca_tu_carpeta_del_archivo"
python GuardianClimaITBA_Grupo129.py
```
Linux:
```
cd Reemplaza_aca_tu_carpeta_del_archivo
python3 GuardianClimaITBA_Grupo129.py
```
2. Se mostrará un menú interactivo con las siguientes opciones:

```
1. Iniciar sesión
2. Registrarse
3. Salir
```

- Una vez iniciada la sesión, podrás acceder a todo el programa.
---

##  ¿Qué hace el programa?

| Opción       | Acción                                                                 |
|-------------|-------------------------------------------------------------------------|
| **1**       | Consultar clima actual y guardar en historial global|
| **2**       | Ver mi historial personal de consultas por ciudad   |
| **3**       | Estadísticas globales de uso y exportar historial completo|
| **4**       | Consejo IA: ¿Cómo me visto hoy?
| **5**       | Acerca de...|
| **6**       | Cerrar sesión|                                                                                                                                                                                                               |

Opción 1 --> Permite obtener datos del clima en la ciudad elegida y almacenarlos en el documento correspondiente.

Opción 2 --> Permite ingresar el nombre de una ciudad y ver el historial de consultas para la misma.

Opción 3 --> Muestra ciertos datos estadísticos de uso del programa, como cantidad de consultas para el usuario, ciudad más consultada y temperatura promedio en todas las ciudades, entre otros.

Opción 4 --> Tanto mediante los datos de una consulta previa como un nuevo ingreso de datos, permite consultar información climática de una ciudad y muestra, con IA, un consejo de vestimenta adecuado para ese clima.

Opción 5 --> Muestra información del programa.

Opción 6 --> Cierra la sesión del usuario y va al menú principal.
##  Estructura del proyecto

```
/mi_carpeta
│
├── GuardianClimaITBA_Grupo129.py
├── usuarios_simulados.csv	(se genera automáticamente al ejecutar el programa)              
├── historial_global.csv	(se genera automáticamente al ejecutar el programa)
└── README.md
```



