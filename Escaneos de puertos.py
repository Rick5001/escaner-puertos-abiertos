import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Desconocido"
            return f"[+] Puerto abierto: {port} ({service})"
    except:
        return None
    finally:
        sock.close()

def scan_ports_fast(target, start_port, end_port, max_threads=100):
    print(f"\n Escaneando host: {target}")
    print(f" Rango de puertos: {start_port}-{end_port}")
    print(" Inicio:", datetime.now().strftime("%I:%M %p"))
    print("-" * 40)

    open_ports = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(scan_port, target, port): port for port in range(start_port, end_port + 1)}
        for future in as_completed(futures):
            result = future.result()
            if result:
                print(result)
                open_ports.append(futures[future])

    if not open_ports:
        print("❌ No se encontraron puertos abiertos.")
    
    print("-" * 40)
    print(" Fin:", datetime.now().strftime("%I:%M %p"))

# --- MAIN ---
if __name__ == "__main__":
    objetivo = input("Ingresa la IP o dominio a escanear: ")
    inicio = int(input("Puerto inicial: "))
    fin = int(input("Puerto final: "))
    scan_ports_fast(objetivo, inicio, fin)