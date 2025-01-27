import sys
import socket
import subprocess
from datetime import datetime

def escanear_puertos(target):
    """Escanea los puertos comunes en el objetivo especificado."""
    print(f"\n[+] Iniciando escaneo de puertos en {target}")
    print(f"Hora de inicio: {datetime.now()}\n")

    try:
        # Escanea los puertos del 1 al 1024 (puertos comunes)
        for puerto in range(1, 1025):
            # Crea un socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Tiempo de espera
                s.settimeout(0.5)
                # Intenta conectarse al puerto
                resultado = s.connect_ex((target, puerto))
                if resultado == 0:
                    print(f"[+] Puerto {puerto} está abierto")

    except KeyboardInterrupt:
        print("\n[-] Interrupción del usuario.")
        sys.exit()

    except socket.gaierror:
        print("\n[-] No se pudo resolver la dirección. Verifica el dominio o IP.")
        sys.exit()

    except socket.error:
        print("\n[-] Error al intentar conectar al servidor.")
        sys.exit()

    print(f"\n[+] Escaneo de puertos completado.")
    print(f"Hora de finalización: {datetime.now()}")


def escanear_vulnerabilidades(target):
    """Escanea vulnerabilidades usando Nmap."""
    print(f"\n[+] Iniciando escaneo de vulnerabilidades en {target}")
    print(f"Hora de inicio: {datetime.now()}\n")

    try:
        # Comando para ejecutar Nmap con un script de vulnerabilidades
        comando = f"nmap -sV --script=vuln {target}"
        resultado = subprocess.check_output(comando, shell=True, text=True)
        print(resultado)
    except FileNotFoundError:
        print("\n[-] Nmap no está instalado o no está disponible en tu sistema. Por favor, instálalo y asegúrate de que esté en el PATH.")
    except subprocess.CalledProcessError as e:
        print(f"\n[-] Error al ejecutar Nmap: {e}")
    except KeyboardInterrupt:
        print("\n[-] Interrupción del usuario.")
        sys.exit()

    print(f"\n[+] Escaneo de vulnerabilidades completado.")
    print(f"Hora de finalización: {datetime.now()}")


def main():
    print("\n*** Bienvenido al Escáner de Seguridad ***\n")
    print("1. Escaneo de puertos abiertos")
    print("2. Escaneo de vulnerabilidades (usando Nmap)")
    print("3. Salir\n")

    opcion = input("Selecciona una opción: ").strip()

    if opcion == "1":
        target = input("Ingresa la dirección IP o dominio a escanear: ").strip()
        if target:
            escanear_puertos(target)
        else:
            print("[-] Por favor, ingresa un objetivo válido.")

    elif opcion == "2":
        target = input("Ingresa la dirección IP o dominio a escanear: ").strip()
        if target:
            escanear_vulnerabilidades(target)
        else:
            print("[-] Por favor, ingresa un objetivo válido.")

    elif opcion == "3":
        print("\nSaliendo del programa. ¡Hasta luego!")
        sys.exit()

    else:
        print("\n[-] Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaliendo del programa.")
        sys.exit()
