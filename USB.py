import socket
import pyautogui
import keyboard
import os
import subprocess
import threading

# Configuración
HOST = '127.0.0.1' 
PORT = 5000
EXIT_COMBINATION = 'ctrl+q'

pyautogui.FAILSAFE = False

def cierre_de_emergencia():
    """Función que corre en un hilo separado para cerrar todo."""
    keyboard.wait(EXIT_COMBINATION)
    print("\n[!] Cierre de emergencia detectado. Finalizando procesos...")
    # os._exit(0) mata el proceso y cierra el CMD de golpe
    os._exit(0)

def configurar_adb():
    user_profile = os.environ.get('USERPROFILE')
    adb_path = os.path.join(user_profile, 'AppData', 'Local', 'Android', 'Sdk', 'platform-tools', 'adb.exe')
    
    try:
        if os.path.exists(adb_path):
            subprocess.run([adb_path, "reverse", "tcp:5000", "tcp:5000"], shell=True)
            print("Configuración ADB Exitosa.")
            print("Conexion Completada")
        else:
            os.system("adb reverse tcp:5000 tcp:5000")
            print("Conexion Completada")
    except Exception as e:
        print(f"Error al configurar ADB: {e}")

def iniciar_servidor():
    # Iniciamos el hilo de escucha de teclado antes que nada
    monitor_teclado = threading.Thread(target=cierre_de_emergencia, daemon=True)
    monitor_teclado.start()

    configurar_adb()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor Activo en puerto {PORT}")
        print(f"Presiona {EXIT_COMBINATION} para cerrar totalmente.")

        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    try:
                        data = conn.recv(1024).decode('utf-8').strip()
                        if not data: break
                        
                        # --- LÓGICA DE COMANDOS ---
                        if data.startswith("SCROLL,"):
                            _, val = data.split(',')
                            pyautogui.scroll(int(val) * 2)
                        elif data == "CLICK":
                            pyautogui.click()
                        elif data == "MOUSEDOWN":
                            pyautogui.mouseDown()
                        elif data == "MOUSEUP":
                            pyautogui.mouseUp()
                        elif "," in data:
                            dx, dy = map(int, data.split(','))
                            pyautogui.moveRel(dx, dy, _pause=False)
                    except:
                        break

if __name__ == "__main__":
    iniciar_servidor()

    #python USB.py
    # & "C:\Users\USER\AppData\Local\Android\Sdk\platform-tools\adb.exe" reverse tcp:5000 tcp:5000