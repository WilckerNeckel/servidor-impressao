import socket
import win32print
import subprocess
# Configuration
TCP_IP = '0.0.0.0'      # Listen on all interfaces
TCP_PORT = 9100         # Port to listen on
BUFFER_SIZE = 1024      # Buffer size for incoming data

# Replace with the exact printer name as it appears in Windows
PRINTER_NAME = 'COZINHA'

def send_to_printer(data, printer_name):
    """Send raw data to the specified printer using Windows printing APIs."""
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        # Prepare the document info: (doc name, output file, data type)
        doc_info = ("Python Print Job", None, "RAW")
        hJob = win32print.StartDocPrinter(hPrinter, 1, doc_info)
        try:
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, data)
            win32print.EndPagePrinter(hPrinter)
        finally:
            win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)

def handle_client(conn, addr):
    print(f"Connection established from {addr}")
    data_buffer = b""
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            data_buffer += data
        if data_buffer:
            send_to_printer(data_buffer, PRINTER_NAME)
            print("Data sent to printer.")
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection closed from {addr}")

def open_firewall_port():
    """Opens TCP port 9100 in the Windows firewall, removing existing rule if present."""
    reabriu = False
    rule_name = f"wnk_abrir_porta_{TCP_PORT}"
    delete_command = [
        "netsh", "advfirewall", "firewall", "delete", "rule",
        f"name={rule_name}"
    ]
    add_command = [
        "netsh", "advfirewall", "firewall", "add", "rule",
        f"name={rule_name}",
        "dir=in",
        "action=allow",
        "protocol=TCP",
        f"localport={TCP_PORT}"
    ]
    try:
        # Delete the existing rule (if it exists)
        subprocess.run(delete_command, check=True)
        print(f"Aviso: regra já existente, removendo regra da porta {TCP_PORT}")
        reabriu = True
    except subprocess.CalledProcessError:
        # If deletion fails, it might be because the rule didn't exist.
        pass

    try:
        # Now add the new rule.
        subprocess.run(add_command, check=True)
        if reabriu:
            print(f"Sucesso: porta {TCP_PORT} reaberta.")
        else:
            print(f"Sucesso: porta {TCP_PORT} aberta.")
    except subprocess.CalledProcessError as e:
        print(f"Erro: falha ao abrir porta {TCP_PORT}", e)

def main():
    open_firewall_port()

        
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((TCP_IP, TCP_PORT))
        server_socket.listen(5)
        print(f"Listening on {TCP_IP}:{TCP_PORT}...")
        while True:
            try:
                conn, addr = server_socket.accept()
                handle_client(conn, addr)
            except KeyboardInterrupt:
                print("Server is shutting down.")
                break
            except Exception as e:
                print(f"Erro: {e}")

if __name__ == '__main__':
    main()
