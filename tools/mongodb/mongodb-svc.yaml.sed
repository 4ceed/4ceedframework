apiVersion: v1
kind: Service
metadata:
  labels:
    name: mongo
  name: mongodb
  namespace: 4ceed
spec:
  ports:
    - port: 27017
      targetPort: 27017
  selector:
    name: mongo
  clusterIP: $MONGODB_IP
