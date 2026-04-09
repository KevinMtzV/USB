import socket
import pyautogui
import keyboard
import os
import subprocess
import threading
import sys

# Configuración
HOST = '127.0.0.1' 
PORT = 5000
EXIT_COMBINATION = 'ctrl+q'

# Optimización de PyAutoGUI
pyautogui.FAILSAFE = False

def cierre_de_emergencia():
    """Función que corre en un hilo separado para cerrar todo."""
    keyboard.wait(EXIT_COMBINATION)
    print("\n[!] Cierre de emergencia detectado. Finalizando procesos...")
    os._exit(0)

def configurar_adb():
    user_profile = os.environ.get('USERPROFILE')
    adb_path = os.path.join(user_profile, 'AppData', 'Local', 'Android', 'Sdk', 'platform-tools', 'adb.exe')
    
    try:
        print("Configurando túnel ADB...")
        if os.path.exists(adb_path):
            subprocess.run([adb_path, "reverse", "tcp:5000", "tcp:5000"], shell=True)
            print("Configuración ADB Exitosa.")
        else:
            # Intento por comando global si no está en la ruta de Android Studio
            os.system("adb reverse tcp:5000 tcp:5000")
            print("Conexión Completada (vía Global ADB)")
    except Exception as e:
        print(f"Error al configurar ADB: {e}")

def iniciar_servidor():
    # Iniciamos el hilo de escucha de teclado
    monitor_teclado = threading.Thread(target=cierre_de_emergencia, daemon=True)
    monitor_teclado.start()

    configurar_adb()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"\n>>> SERVIDOR ACTIVO EN PUERTO {PORT}")
        print(f">>> Presiona {EXIT_COMBINATION} para cerrar totalmente.")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Celular conectado desde: {addr}")
                while True:
                    try:
                        # Recibimos los datos brutos
                        raw_data = conn.recv(1024).decode('utf-8')
                        if not raw_data: break
                        
                        # IMPORTANTE: Separamos por saltos de línea por si llegan varios comandos juntos
                        messages = raw_data.strip().split('\n')
                        
                        for data in messages:
                            data = data.strip()
                            if not data: continue

                            # --- PROCESAMIENTO ROBUSTO DE COMANDOS ---
                            try:
                                if data.startswith("SCROLL,"):
                                    _, val = data.split(',')
                                    # Multiplicamos por -2 o 2 según la dirección del scroll
                                    pyautogui.scroll(int(val) * 2)
                                
                                elif data == "CLICK":
                                    pyautogui.click()
                                
                                elif data == "MOUSEDOWN":
                                    pyautogui.mouseDown()
                                    print("Arrastre iniciado")
                                
                                elif data == "MOUSEUP":
                                    pyautogui.mouseUp()
                                    print("Arrastre finalizado")
                                
                                elif "," in data:
                                    dx, dy = map(int, data.split(','))
                                    # _pause=False es clave para la fluidez
                                    pyautogui.moveRel(dx, dy, _pause=False)
                            
                            except (ValueError, IndexError):
                                
                                continue
                                
                    except Exception as e:
                        print(f"Conexión perdida o error: {e}")
                        break
                print("Esperando nueva conexión...")

if __name__ == "__main__":
    iniciar_servidor()

    #python USB.py
    # & "C:\Users\USER\AppData\Local\Android\Sdk\platform-tools\adb.exe" reverse tcp:5000 tcp:5000