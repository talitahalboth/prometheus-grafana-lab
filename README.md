## Starting Containers

To start Prometheus and Grafana containers you can use `docker compose up -d`. 

## Accessing Grafana and Prometheus

Prometheus:
http://localhost:9090


Grafana:
http://localhost:3000

## Configure grafana: 
Connections > Data Sources

Once Prometheus is scraping your app, add Prometheus as a data source in Grafana
http://prometheus:9090


## Running the python app

`python metrics_app.py`

Checking /metrics endpoint from the app:

http://127.0.0.1:8081/metrics

