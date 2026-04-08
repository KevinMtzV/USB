import socket
import pyautogui

# Configuración del servidor
HOST = '127.0.0.1' 
PORT = 5000

# Desactivar el "Fail-Safe"
pyautogui.FAILSAFE = False

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Esperando conexión del celular en el puerto {PORT}...")
        conn, addr = s.accept()
        with conn:
            print(f"Conectado por {addr}")
            while True:
                data = conn.recv(1024).decode('utf-8').strip()
                if not data:
                    break
                
                # --- LÓGICA DE COMANDOS ---

                elif data == "CLICK":
                    pyautogui.click()
                    print("Click")
                
                elif data == "MOUSEDOWN":
                    pyautogui.mouseDown()
                    print("PC: Botón presionado") 
                elif data == "MOUSEUP":
                    pyautogui.mouseUp()
                    print("PC: Botón soltado")
                else:
                    try:
                        # Si contiene una coma, es movimiento
                        if "," in data:
                            dx, dy = map(int, data.split(','))
                            # _pause=False mantiene la fluidez perfecta
                            pyautogui.moveRel(dx, dy, _pause=False) 
                    except ValueError:
                        pass

if __name__ == "__main__":
    iniciar_servidor()

    #python USB.py
    # & "C:\Users\USER\AppData\Local\Android\Sdk\platform-tools\adb.exe" reverse tcp:5000 tcp:5000