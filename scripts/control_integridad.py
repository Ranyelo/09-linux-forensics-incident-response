#!/usr/bin/env python3
import sys
import hashlib
import os

def calcular_sha256(ruta_archivo):
    sha256_hash = hashlib.sha256()
    with open(ruta_archivo, "rb") as f:
        # Lectura en bloques para no saturar memoria
        for bloque in iter(lambda: f.read(4096), b""):
            sha256_hash.update(bloque)
    return sha256_hash.hexdigest()

def generar_reporte(directorio_o_archivo, ruta_salida):
    if os.path.isfile(directorio_o_archivo):
        archivos = [directorio_o_archivo]
    elif os.path.isdir(directorio_o_archivo):
        archivos = [
            os.path.join(directorio_o_archivo, f) 
            for f in os.listdir(directorio_o_archivo) 
            if os.path.isfile(os.path.join(directorio_o_archivo, f))
        ]
    else:
        print(f"[-] La ruta '{directorio_o_archivo}' no es valida.")
        return

    with open(ruta_salida, 'w', encoding='utf-8') as f_out:
        f_out.write("REPORTE DE INTEGRIDAD DE EVIDENCIAS\n")
        f_out.write("===================================\n\n")
        for ruta in archivos:
            nombre = os.path.basename(ruta)
            try:
                hash_val = calcular_sha256(ruta)
                f_out.write(f"Archivo: {nombre}\n")
                f_out.write(f"SHA-256: {hash_val}\n")
                f_out.write("-" * 50 + "\n")
                print(f"[+] Hashed: {nombre}")
            except Exception as e:
                f_out.write(f"Archivo: {nombre}\n")
                f_out.write(f"Error al procesar: {e}\n")
                f_out.write("-" * 50 + "\n")
                print(f"[-] Error en: {nombre}")

def main():
    if len(sys.argv) < 3:
        print("Uso: python control_integridad.py <ruta_evidencia> <reporte_salida.txt>")
        sys.exit(1)
        
    ruta_evidencia = sys.argv[1]
    ruta_reporte = sys.argv[2]
    
    generar_reporte(ruta_evidencia, ruta_reporte)
    print(f"[+] Reporte guardado en {ruta_reporte}")

if __name__ == '__main__':
    main()
