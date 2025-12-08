kubectl create configmap nginx-config --from-file=default.conf=../config/default.conf

kubectl apply -f static-pvc.yaml

kubectl create secret generic mysql-secret --from-env-file=../env/.mysql.env
kubectl apply -f mysql/pvc.yaml
kubectl apply -f mysql/deployment.yaml
kubectl apply -f mysql/service.yaml

kubectl apply -f redis/deployment.yaml
kubectl apply -f redis/service.yaml

kubectl apply -f nginx/deployment.yaml
kubectl apply -f nginx/service.yaml

kubectl apply -f server/deployment.yaml
kubectl apply -f server/service.yaml

kubectl apply -f rabbitmq/deployment.yaml
kubectl apply -f rabbitmq/service.yaml