import requests
from os import path
import argparse
import sys

def es_subdominio_valido(subdominio):
    """
    Valida si un subdominio es válido.

    Un subdominio es válido si no contiene caracteres no permitidos como espacios o dobles puntos,
    y no está vacío.

    Args:
        subdominio (str): Subdominio a validar.

    Returns:
        bool: True si el subdominio es válido, False en caso contrario.
    """
    if not subdominio or ".." in subdominio or " " in subdominio:
        return False
    return True

def obtener_banners(headers):
    """
    Obtiene los banners relevantes de los encabezados HTTP.

    Args:
        headers (dict): Encabezados HTTP de la respuesta.

    Returns:
        dict: Diccionario con los banners relevantes.
    """
    banners = {}
    claves_interes = ['Server', 'X-Powered-By', 'Content-Type', 'Date', 'Cache-Control', 'Connection']

    for clave in claves_interes:
        if clave in headers:
            banners[clave] = headers[clave]

    return banners

def detectar_tecnologias(headers, url):
    """
    Detecta tecnologías utilizadas en el sitio web basado en los encabezados HTTP y el contenido de la página.

    Args:
        headers (dict): Encabezados HTTP de la respuesta.
        url (str): URL del sitio web.

    Returns:
        list: Lista de tecnologías detectadas.
    """
    tecnologias = []

    # Detectar tecnologías en base a encabezados HTTP
    if 'X-Powered-By' in headers:
        tecnologias.append(f"Framework: {headers['X-Powered-By']}")

    if 'Server' in headers:
        tecnologias.append(f"Servidor: {headers['Server']}")

    # Pistas de tecnologías populares
    if 'WordPress' in headers.get('X-Powered-By', ''):
        tecnologias.append("Tecnología detectada: WordPress")
    if 'PHP' in headers.get('X-Powered-By', ''):
        tecnologias.append("Tecnología detectada: PHP")
    if 'ASP.NET' in headers.get('X-Powered-By', ''):
        tecnologias.append("Tecnología detectada: ASP.NET")

    # Comprobar el contenido de la página (opcional)
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            contenido = response.text
            if 'React' in contenido:
                tecnologias.append("Tecnología detectada: React.js")
            if 'Angular' in contenido:
                tecnologias.append("Tecnología detectada: Angular.js")
            if 'Vue' in contenido:
                tecnologias.append("Tecnología detectada: Vue.js")
    except requests.RequestException:
        pass  # Si no se puede obtener el contenido, continuar

    return tecnologias

# Configuración de argumentos del script
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', help='Indicar el dominio de la víctima')
args = parser.parse_args()

def main():
    """
    Función principal del script para enumerar subdominios, extraer encabezados HTTP y detectar tecnologías.

    Requiere un archivo 'subdominios.txt' con una lista de subdominios a probar.
    """
    if args.target:
        if path.exists('subdominios.txt'):
            try:
                with open('subdominios.txt', 'r') as wordlist:
                    subdominios = wordlist.read().splitlines()

                for subdominio in subdominios:
                    if not es_subdominio_valido(subdominio):
                        continue

                    url_http = f'http://{subdominio}.{args.target}'
                    url_https = f'https://{subdominio}.{args.target}'

                    for url in [url_http, url_https]:
                        try:
                            # Intentar hacer una solicitud HEAD para obtener solo los encabezados
                            response = requests.head(url, timeout=5)

                            if response.status_code in range(200, 400):
                                print(f"(+) Subdominio encontrado: {url}")

                                # Obtener banners de servicios
                                banners = obtener_banners(response.headers)
                                if banners:
                                    print("    Banners encontrados:")
                                    for clave, valor in banners.items():
                                        print(f"        {clave}: {valor}")
                                else:
                                    print("    No se encontraron banners relevantes.")

                                # Detectar tecnologías
                                tecnologias = detectar_tecnologias(response.headers, url)
                                if tecnologias:
                                    print("    Tecnologías detectadas:")
                                    for tecnologia in tecnologias:
                                        print(f"        {tecnologia}")
                                else:
                                    print("    No se detectaron tecnologías relevantes.")

                        except requests.exceptions.RequestException:
                            pass

            except FileNotFoundError:
                print("(-) El archivo 'subdominios.txt' no existe.")
        else:
            print("(-) El archivo 'subdominios.txt' no se encuentra.")
    else:
        print("(-) Ingresa un dominio válido con -t o --target")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n(-) Interrumpido por el usuario.")
        sys.exit()