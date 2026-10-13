import socket
import time

HOST = '127.0.0.1'
PORT = 1022

def start_dummy_plc():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[*] Virtual Siemens S7-300 PLC is ONLINE on {HOST}:{PORT}")
    print("[*] Waiting for heartbeat inquiries from OT SBC Gateway...")
    try:
        while True:
            conn, addr = s.accept()
            conn.sendall(b"ACK_S7_OK")
            time.sleep(0.05)
            conn.close()
    except KeyboardInterrupt:
        print("\n[*] PLC Station Powered Down.")
    finally:
        s.close()

if __name__ == "__main__":
    start_dummy_plc()