import socket
import win32print

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

def main():
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
                print(f"Error: {e}")

if __name__ == '__main__':
    main()
