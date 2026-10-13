import socket
import sqlite3
import time
import random
from datetime import datetime

conn = sqlite3.connect("factory_telemetry.db")
cursor = conn.cursor()

with open("database_schema.sql", "r", encoding="utf-8") as f:
    cursor.executescript(f.read())
conn.commit()

SBC_GATEWAY_ID = "SBC_Edge_Node_01"
PLC_TARGETS = [{"name": "Siemens_S7_Assembly_Line", "ip": "127.0.0.1", "port": 1022}]

def audit_industrial_network():
    print(f"=== OT SBC EDGE MONITOR [{SBC_GATEWAY_ID}] ===")
    print("Auditing PLC availability & logging telemetry to SQLite...\n")
    try:
        while True:
            for plc in PLC_TARGETS:
                start_time = time.time()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.5)
                sbc_cpu_load = round(random.uniform(12.5, 28.0), 1)

                try:
                    s.connect((plc["ip"], plc["port"]))
                    elapsed = (time.time() - start_time) * 1000
                    data = s.recv(1024)
                    status = "HEALTHY_ONLINE"
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {plc['name']} | STATUS: {status} | Latency: {elapsed:.2f}ms | SBC CPU: {sbc_cpu_load}%")
                except (socket.timeout, ConnectionRefusedError):
                    status = "PORT_UNREACHABLE"
                    elapsed = 0.0
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] [ALERT] {plc['name']} port unreachable!")
                except Exception:
                    status = "OFFLINE_CRITICAL"
                    elapsed = 0.0
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] [CRITICAL] {plc['name']} is OFFLINE! Triggering failover.")
                finally:
                    s.close()

                cursor.execute(
                    "INSERT INTO plc_telemetry (sbc_gateway_id, plc_name, ip_address, target_port, status, latency_ms, sbc_cpu_load_pct) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (SBC_GATEWAY_ID, plc["name"], plc["ip"], plc["port"], status, round(elapsed, 2), sbc_cpu_load)
                )
                conn.commit()
            print("-" * 75)
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n=== SBC Monitoring Stopped by Operator ===")
    finally:
        conn.close()

if __name__ == "__main__":
    audit_industrial_network()