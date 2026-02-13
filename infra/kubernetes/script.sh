#!/bin/sh

# kubectl create namespace swippter

kubectl create secret generic mysql-secret --from-env-file=../env/.mysql.env
kubectl apply -f mysql/pvc.yaml
kubectl apply -f mysql/deployment.yaml
kubectl apply -f mysql/service.yaml

kubectl apply -f redis/deployment.yaml
kubectl apply -f redis/service.yaml

kubectl create configmap nginx-config --from-file=default.conf=../config/default.conf
kubectl apply -f static-pvc.yaml
kubectl apply -f frontend/deployment.yaml
kubectl apply -f frontend/service.yaml

kubectl create secret generic otel-env-secret --from-env-file=../env/.otel.env
kubectl apply -f server/deployment.yaml
kubectl apply -f server/service.yaml

kubectl apply -f rabbitmq/deployment.yaml
kubectl apply -f rabbitmq/service.yaml

kubectl apply -f observability/otel-collector/config.yaml
kubectl apply -f observability/otel-collector/deployment.yaml
kubectl apply -f observability/otel-collector/service.yaml

kubectl apply -f observability/loki/pvc.yaml
kubectl apply -f observability/loki/deployment.yaml
kubectl apply -f observability/loki/service.yaml

kubectl apply -f observability/tempo/config.yaml
kubectl apply -f observability/tempo/pvc.yaml
kubectl apply -f observability/tempo/deployment.yaml
kubectl apply -f observability/tempo/service.yaml

kubectl apply -f observability/promtail/config.yaml
kubectl apply -f observability/promtail/rbac.yaml
kubectl apply -f observability/promtail/deployment.yaml
kubectl apply -f observability/promtail/service.yaml

kubectl apply -f observability/prometheus/config.yaml
kubectl apply -f observability/prometheus/deployment.yaml
kubectl apply -f observability/prometheus/service.yaml

kubectl apply -f observability/grafana/config.yaml
kubectl apply -f observability/grafana/deployment.yaml
kubectl apply -f observability/grafana/service.yaml