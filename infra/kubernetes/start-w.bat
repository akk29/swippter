kubectl create namespace swippter

kubectl create secret generic mysql-secret --from-env-file=../env/.mysql.env -n swippter
kubectl apply -f mysql/pvc.yaml -n swippter
kubectl apply -f mysql/deployment.yaml -n swippter
kubectl apply -f mysql/service.yaml -n swippter

kubectl apply -f redis/deployment.yaml -n swippter
kubectl apply -f redis/service.yaml -n swippter

kubectl create configmap nginx-config --from-file=default.conf=../config/default.conf -n swippter
kubectl apply -f static-pvc.yaml -n swippter
kubectl apply -f frontend/deployment.yaml -n swippter
kubectl apply -f frontend/service.yaml -n swippter

kubectl create secret generic otel-env-secret --from-env-file=../env/.otel.env -n swippter
kubectl apply -f server/deployment.yaml -n swippter
kubectl apply -f server/service.yaml -n swippter

kubectl apply -f rabbitmq/deployment.yaml -n swippter
kubectl apply -f rabbitmq/service.yaml -n swippter

kubectl apply -f observability/otel-collector/config.yaml -n swippter
kubectl apply -f observability/otel-collector/deployment.yaml -n swippter
kubectl apply -f observability/otel-collector/service.yaml -n swippter

kubectl apply -f observability/loki/pvc.yaml -n swippter
kubectl apply -f observability/loki/deployment.yaml -n swippter
kubectl apply -f observability/loki/service.yaml -n swippter

kubectl apply -f observability/tempo/config.yaml -n swippter
kubectl apply -f observability/tempo/pvc.yaml -n swippter
kubectl apply -f observability/tempo/deployment.yaml -n swippter
kubectl apply -f observability/tempo/service.yaml -n swippter

kubectl apply -f observability/promtail/config.yaml -n swippter
kubectl apply -f observability/promtail/rbac.yaml -n swippter
kubectl apply -f observability/promtail/deployment.yaml -n swippter
kubectl apply -f observability/promtail/service.yaml -n swippter

kubectl apply -f observability/prometheus/config.yaml -n swippter
kubectl apply -f observability/prometheus/deployment.yaml -n swippter
kubectl apply -f observability/prometheus/service.yaml -n swippter

kubectl apply -f observability/grafana/config.yaml -n swippter
kubectl apply -f observability/grafana/deployment.yaml -n swippter
kubectl apply -f observability/grafana/service.yaml -n swippter