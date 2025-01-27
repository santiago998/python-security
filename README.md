

# Descripción de Scripts

Este repositorio contiene tres scripts diseñados para realizar tareas relacionadas con la validación, exploración y análisis de dominios y subdominios web. A continuación, se detalla la funcionalidad de cada script.

---

## **1. Explorador de Subdominios**
### Descripción
Este script explora posibles subdominios de un dominio objetivo, valida su existencia y detecta tecnologías y encabezados HTTP asociados.

### Funcionalidades principales:
- Valida si un subdominio es válido antes de realizar solicitudes.
- Verifica la existencia de subdominios mediante solicitudes HTTP/HTTPS.
- Obtiene banners de encabezados HTTP como `Server`, `X-Powered-By`, entre otros.
- Detecta tecnologías usadas en el sitio web, como WordPress, PHP, ASP.NET, React.js, Angular.js, Vue.js, etc.
- Manejo de errores en caso de problemas con solicitudes o archivos.

### Uso:
```bash
python subdomain_scanner.py -t <dominio_objetivo>
```

### Requisitos:
- **Archivo necesario:** `subdominios.txt` con la lista de posibles subdominios.
- **Librerías utilizadas:**
  - `requests`
  - `os`
  - `argparse`
  - `sys`

---

## **2. Explorador de Tecnologías con WAD**
### Descripción
Este script utiliza la herramienta `wad` para identificar las tecnologías utilizadas por un sitio web. Registra los resultados en un archivo JSON y permite consultar las URLs analizadas previamente.

### Funcionalidades principales:
- Verifica si la URL proporcionada tiene un formato válido.
- Ejecuta la herramienta `wad` para identificar tecnologías usadas en el sitio web.
- Guarda los resultados en un archivo JSON (`tecnologias.txt`) sin sobrescribir información previa.
- Permite listar las URLs que ya han sido consultadas.

### Uso:
1. **Ejecutar para analizar una URL:**
   ```bash
   python tech_explorer.py -t <url_objetivo>
   ```
2. **Listar URLs ya analizadas:**
   ```bash
   python tech_explorer.py -l
   ```

### Requisitos:
- **Dependencias externas:**
  - Herramienta `wad` (Web Application Detector), disponible en el sistema operativo.
- **Librerías utilizadas:**
  - `subprocess`
  - `argparse`
  - `sys`
  - `json`
  - `urllib.parse`

---

## **3. Analizador de Subdominios (Avanzado)**
### Descripción
Este script avanza en la detección de subdominios realizando solicitudes HTTP y analizando encabezados para detectar posibles tecnologías y servicios.

### Funcionalidades principales:
- Realiza solicitudes `HEAD` para determinar la existencia de subdominios.
- Analiza encabezados HTTP para detectar servicios y tecnologías específicas.
- Proporciona un formato detallado de la información encontrada.
- Registra resultados en la consola para su análisis inmediato.

### Uso:
```bash
python advanced_subdomain_analyzer.py -t <dominio_objetivo>
```

### Requisitos:
- **Archivo necesario:** `subdominios.txt` con una lista de posibles subdominios.
- **Librerías utilizadas:**
  - `requests`
  - `os`
  - `argparse`
  - `sys`

---

## **Instalación de Dependencias**
Se recomienda utilizar un entorno virtual para manejar las dependencias necesarias. Sigue estos pasos para instalarlas:
1. Crear un entorno virtual:
   ```bash
   python -m venv venv
   ```
2. Activar el entorno virtual:
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
3. Instalar las dependencias:
   ```bash
   pip install requests argparse
   ```

---

## **Notas Importantes**
- Asegúrate de tener los permisos adecuados para ejecutar los scripts en tu entorno.
- La herramienta `wad` debe estar correctamente instalada y accesible desde la línea de comandos para el segundo script.

---

## **Autor**
Este proyecto fue desarrollado con el objetivo de facilitar la exploración y análisis de tecnologías y subdominios en entornos web.

Si tienes alguna pregunta o necesitas soporte, no dudes en contactarme
santiyinguz@gmail.com
redes sociales
Linked. 😊

