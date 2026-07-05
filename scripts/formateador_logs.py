#!/usr/bin/env python3
import sys
import re
import csv

# Expresion regular basica para parsear logs en formato Apache/Common Log Format
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<date>.*?)\]\s+"(?P<method>\S+)\s+(?P<url>\S+)\s+HTTP/\d\.\d"\s+(?P<status>\d+)\s+(?P<size>\S+)'
)

def parsear_archivo(ruta_log):
    eventos = []
    with open(ruta_log, 'r', encoding='utf-8') as f:
        for linea in f:
            match = LOG_PATTERN.match(linea)
            if match:
                datos = match.groupdict()
                if datos['size'] == '-':
                    datos['size'] = '0'
                eventos.append(datos)
    return eventos

def guardar_csv(eventos, ruta_salida):
    if not eventos:
        print("No hay eventos para guardar.")
        return
    
    campos = ['ip', 'date', 'method', 'url', 'status', 'size']
    with open(ruta_salida, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(eventos)
    print(f"[+] Se exportaron {len(eventos)} eventos a {ruta_salida}")

def main():
    if len(sys.argv) < 3:
        print("Uso: python formateador_logs.py <archivo_log> <archivo_salida.csv>")
        sys.exit(1)
        
    log_in = sys.argv[1]
    csv_out = sys.argv[2]
    
    try:
        eventos = parsear_archivo(log_in)
        guardar_csv(eventos, csv_out)
    except FileNotFoundError:
        print(f"[-] Error: No se encontro el archivo {log_in}")
    except Exception as e:
        print(f"[-] Ocurrio un error inesperado: {e}")

if __name__ == '__main__':
    main()
