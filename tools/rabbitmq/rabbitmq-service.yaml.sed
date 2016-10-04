apiVersion: v1
kind: Service
metadata:
  labels:
    component: rabbitmq
  name: rabbitmq-service
  namespace: 4ceed
spec:
  ports:
  - port: 5672
  selector:
    app: taskQueue
    component: rabbitmq
  clusterIP: $RABBITMQ_IP
