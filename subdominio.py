import requests
from os import path
import argparse
import sys


def es_subdominio_valido(subdominio):
    """Valida que un subdominio no tenga caracteres inválidos y no esté vacío."""
    if not subdominio or ".." in subdominio or " " in subdominio:
        return False
    return True


def obtener_banners(headers):
    """Obtiene los banners relevantes de los encabezados HTTP."""
    banners = {}
    claves_interes = ['Server', 'X-Powered-By', 'Content-Type', 'Date', 'Cache-Control', 'Connection']
    
    for clave in claves_interes:
        if clave in headers:
            banners[clave] = headers[clave]
    
    return banners


def detectar_tecnologias(headers, url):
    """Detecta tecnologías usadas en el sitio web basado en los encabezados HTTP y contenido visible."""
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


# Argumentos del script
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', help='Indicar el dominio de la víctima')
args = parser.parse_args()


def main():
    if args.target:
        if path.exists('subdominios.txt'):
            try:
                with open('subdominios.txt', 'r') as wordlist:  # Uso de "with" para manejar archivos
                    subdominios = wordlist.read().splitlines()  # Leer y dividir líneas

                for subdominio in subdominios:
                    if not es_subdominio_valido(subdominio):
                        continue  # Omitir subdominios no válidos

                    url_http = f'http://{subdominio}.{args.target}'
                    url_https = f'https://{subdominio}.{args.target}'

                    for url in [url_http, url_https]:
                        try:
                            # Intentar hacer una solicitud HEAD (solo obtener los headers)
                            response = requests.head(url, timeout=5)

                            # Si el estado es 2xx o 3xx, significa que el subdominio existe
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

                        except requests.exceptions.RequestException as e:
                            pass  # Si ocurre cualquier error en la solicitud, lo ignoramos

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
