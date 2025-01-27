import subprocess
import argparse
import sys
import json
from urllib.parse import urlparse


class Colores:
    """Clase para agregar colores al texto en consola."""
    VERDE = '\033[92m'
    ROJO = '\033[91m'
    FIN = '\033[0m'


def es_url_valida(url):
    """Verifica si la URL proporcionada tiene un formato válido."""
    try:
        resultado = urlparse(url)
        return all([resultado.scheme, resultado.netloc])
    except ValueError:
        return False


def guardar_en_archivo(datos, archivo="tecnologias.txt"):
    """
    Guarda datos en formato JSON en un archivo.
    Si el archivo no existe, lo crea. Si ya existe, agrega los datos sin sobrescribir el contenido previo.
    """
    try:
        # Leer el contenido existente del archivo, si lo hay
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Si el archivo no existe o tiene formato incorrecto, inicializar una lista vacía
        contenido = []

    # Agregar los nuevos datos
    contenido.append(datos)

    # Sobrescribir el archivo con los datos actualizados
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(contenido, f, indent=4, ensure_ascii=False)


def ya_consultado(url, archivo="tecnologias.txt"):
    """Verifica si la URL ya fue consultada previamente y está en el archivo."""
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = json.load(f)
            # Buscar si la URL ya existe en el contenido
            for item in contenido:
                if url in item:
                    return True
    except (FileNotFoundError, json.JSONDecodeError):
        return False
    return False


def main():
    """Función principal del programa."""
    if parser.target:
        # Validar que la URL tenga un formato correcto
        if not es_url_valida(parser.target):
            print(f"{Colores.ROJO}(-) La URL ingresada no es válida. Por favor, ingresa una URL correcta.{Colores.FIN}")
            return

        # Verificar si la URL ya ha sido consultada
        if ya_consultado(parser.target):
            print(f"{Colores.VERDE}(+) La URL ya fue consultada previamente y está registrada en el archivo.{Colores.FIN}")
            return

        # Ejecutar el comando con subprocess
        comando = f"wad -u {parser.target}"
        try:
            resultado = subprocess.check_output(comando, shell=True, text=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            print(f"{Colores.ROJO}(-) Error al ejecutar el comando: {e.output.strip()}{Colores.FIN}")
            return

        # Convertir el resultado a formato JSON si es posible
        try:
            resultado_json = json.loads(resultado)
        except json.JSONDecodeError:
            print(f"{Colores.ROJO}(-) No se pudo decodificar el resultado como JSON.{Colores.FIN}")
            return

        # Guardar el resultado en el archivo
        guardar_en_archivo({parser.target: resultado_json})
        print(f"{Colores.VERDE}(+) Resultados añadidos al archivo 'tecnologias.txt'{Colores.FIN}")

    else:
        print(f"{Colores.ROJO}(-) Ingresa una URL con el argumento '-t' o '--target'.{Colores.FIN}")


if __name__ == '__main__':
    # Configurar los argumentos de línea de comandos
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', help='Indicar la URL \n(e.g https://ejemplo.com)')
    parser.add_argument('-l', '--list', action='store_true', help='Listar las URLs ya consultadas')
    parser = parser.parse_args()

    try:
        # Opción para listar las consultas previas
        if parser.list:
            try:
                with open("tecnologias.txt", "r", encoding="utf-8") as f:
                    contenido = json.load(f)
                    print(f"{Colores.VERDE}(+) Consultas almacenadas:{Colores.FIN}")
                    for consulta in contenido:
                        print(json.dumps(consulta, indent=4, ensure_ascii=False))
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"{Colores.ROJO}(-) No hay datos registrados o el archivo está vacío.{Colores.FIN}")
            sys.exit()

        # Ejecutar la función principal
        main()
    except KeyboardInterrupt:
        print(f"\n{Colores.ROJO}(-) Ejecución interrumpida por el usuario.{Colores.FIN}")
        sys.exit()
