import socket
import os

# Configurações do servidor TCP
HOST = "0.0.0.0"  # Escuta em todas as interfaces
PORT = 9100       # Porta TCP que será aberta

# Caminho para a impressora compartilhada
PRINTER_NAME = r"\\localhost\COZINHA"

# Inicia o servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Servidor TCP escutando na porta {PORT}...")

    while True:
        conn, addr = server_socket.accept()
        print(f"\nConexão recebida de {addr}")
        try:
            with conn:
                while True:
                    # Recebe os dados diretamente do cliente
                    data = conn.recv(1024)
                    if not data:
                        break  # Sai do loop quando não há mais dados
                    
                    print("Dados recebidos (em hexadecimal):")
                    print(' '.join(f'{b:02X}' for b in data))  # Log dos dados recebidos em hexadecimal

                    # Abre a impressora em modo binário e envia os dados diretamente
                    with open(PRINTER_NAME, "wb") as printer:
                        printer.write(data)
                    print("Dados enviados diretamente para a impressora POS.")
        except Exception as e:
            print(f"Erro: {e}")
