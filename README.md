# WORK IN PROGRESS

# Observability Stack Docker Compose Setup

A turnkey, all-in-one observability stack using Docker Compose combining **NATS**, **Vector**, **Loki**, **MinIO**, **Grafana**, **Grafana Tempo**, **OpenTelemetry Collector**, **Prometheus**, **Mimir**, and **HAProxy** as a reverse proxy.

This stack provides centralized logs, metrics, and tracing with minimal setup, configurable via a `.env` file for easy customization.

---

## Features

- **NATS** as a lightweight message queue for logs and telemetry
- **Vector** as log collector/forwarder with NATS source and Loki sink
- **Loki** for scalable log storage on MinIO S3-compatible object storage
- **MinIO** as S3-compatible object storage backend used by Loki, Tempo, and Mimir
- **Grafana** as unified dashboard for logs, metrics, tracing
- **Grafana Tempo** for distributed tracing storage and querying
- **OpenTelemetry Collector** to receive, process, and export telemetry data
- **Prometheus** with autodiscovery for scraping metrics and Mimir backend for long-term storage
- **Mimir** scalable time-series storage backend for Prometheus
- **HAProxy** to expose and route all endpoints via path-based reverse proxy
- Debug containers included for troubleshooting network and connectivity

---

## Quickstart

1. **Clone the repository**
git clone <https://github.com/your-org/observability-stack.git>
cd observability-stack
text

2. **Create and configure `.env`**
cp .env.example .env
text

Edit `.env` as necessary. At minimum, set MinIO credentials:
MINIO_ACCESS_KEY_ID=minioadmin
MINIO_SECRET_ACCESS_KEY=minioadmin
text

3. **Create MinIO Buckets**

Buckets required by the stack (create via MinIO web UI or script):

- `mimir-blocks`
- `mimir-ruler`
- `tempo`
- `loki-chunks`
- `loki-ruler`

Example using a startup init service or manual via MinIO Console at `http://localhost:9001`.

4. **Start the stack**

docker compose up -d
text

5. **Access the services**

- Grafana: `http://localhost/grafana`
  - Default login: `admin` / `admin` (change after first login)
- Prometheus: `http://localhost/prometheus`
- Loki API: `http://localhost/loki`
- Tempo (tracing): `http://localhost/tempo`
- Mimir (metrics backend): `http://localhost/mimir`
- Vector API: `http://localhost/vector`
- OpenTelemetry Collector endpoints (exposed under `/otelcol`)

---

## Directory Structure

observability-stack/
├── .env.example
├── docker-compose.yml
├── haproxy/
│ ├── haproxy.cfg
│ └── certs/ # Optional TLS certs
├── loki/
│ └── local-config.yaml
├── mimir/
│ └── mimir.yaml
├── minio/
│ └── [optional scripts, data]
├── opentelemetry-collector/
│ └── otelcol-config.yaml
├── prometheus/
│ └── prometheus.yml
├── tempo/
│ └── tempo.yaml
├── vector/
│ └── vector.toml
├── grafana/
│ ├── provisioning/
│ │ ├── datasources/datasources.yaml
│ │ └── dashboards/
│ │ ├── dashboards.yaml
│ │ └── sample-dashboards/
│ └── [dashboards and configs]
├── scripts/
│ └── minio-init.sh # Optional bucket creation script
└── README.md # This file
text

---

## Configuration Details

### Environment Variables

Set in `.env` and passed to services for credentials and config. Required:

- `MINIO_ACCESS_KEY_ID` and `MINIO_SECRET_ACCESS_KEY` — credentials for MinIO and S3-compatible storage used by Loki, Tempo, Mimir.

Modify others as needed for your environment.

### MinIO Buckets

Ensure the following buckets exist before starting the stack:

- `mimir-blocks`
- `mimir-ruler`
- `tempo`
- `loki-chunks`
- `loki-ruler`

---

## HAProxy Reverse Proxy

HAProxy routes all the services behind a single endpoint with the following path prefixes:

| Path Prefix | Service                       | Port (internal) |
|-------------|-------------------------------|-----------------|
| `/grafana`  | Grafana                       | 3000            |
| `/prometheus`| Prometheus                   | 9090            |
| `/loki`     | Loki API                      | 3100            |
| `/tempo`    | Grafana Tempo                 | 3200            |
| `/mimir`    | Mimir                        | 9009            |
| `/vector`   | Vector API                   | 8686            |
| `/otelcol`  | OpenTelemetry Collector       | 4317 (gRPC)     |

Path rewriting is handled so services see requests at root `/`.

---

## Grafana Configuration & Dashboards

- **Persistent storage** in Docker volume `grafana_data` persists dashboards and settings.
- Preconfigured data sources for Prometheus, Mimir, Loki, and Tempo under `/etc/grafana/provisioning/`.
- Sample dashboards preloaded via provisioning with relevant JSON files under `grafana/provisioning/dashboards/`.
- Access at `http://localhost/grafana` with default credentials `admin/admin` (change after first login).

---

## Debugging and Utilities

- Debug containers (`alpine-debug`, `netshoot`, `busybox-debug`) for network troubleshooting can be started with Docker Compose profiles.
- Use them to run `curl`, `wget`, `ping` etc., inside the Docker network.

---

## Troubleshooting Tips

- Bucket Not Found Errors: Create all required MinIO buckets before starting Loki, Mimir, Tempo.
- Vector Healthcheck Failures: Adjust healthcheck commands or increase startup wait times.
- HAProxy - DNS Issues: Confirm backend service names match Docker Compose service names.
- Logs: Inspect each container’s logs with `docker compose logs <service>`.

---

## Contributing & License

Contributions are welcome! Please open issues or pull requests.  
This project is licensed under the MIT License (or your preferred license).

---

## References

- [Grafana Loki](https://grafana.com/oss/loki/)
- [Grafana Tempo](https://grafana.com/oss/tempo/)
- [Vector](https://vector.dev/)
- [MinIO](https://min.io/)
- [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)
- [Prometheus](https://prometheus.io/)
- [Grafana Mimir](https://grafana.com/oss/mimir/)
- [HAProxy](https://www.haproxy.org/)
