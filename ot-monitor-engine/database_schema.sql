CREATE TABLE IF NOT EXISTS plc_telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    sbc_gateway_id VARCHAR(30),
    plc_name VARCHAR(50),
    ip_address VARCHAR(15),
    target_port INTEGER,
    status VARCHAR(20),
    latency_ms REAL,
    sbc_cpu_load_pct REAL
);