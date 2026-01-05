kubectl create configmap app-config --from-env-file=../docker/backend/mysql/.env

kubectl apply -f mysql/pvc.yaml
kubectl apply -f mysql/deployment.yaml
kubectl apply -f mysql/service.yaml

kubectl apply -f redis/deployment.yaml
kubectl apply -f redis/service.yaml

kubectl apply -f frontend/deployment.yaml
kubectl apply -f frontend/service.yaml

kubectl apply -f server/deployment.yaml
kubectl apply -f server/service.yaml

kubectl apply -f rabbitmq/deployment.yaml
kubectl apply -f rabbitmq/service.yaml
