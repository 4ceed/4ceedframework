apiVersion: v1
kind: ReplicationController
metadata:
  name: xray-extractor
spec:
  replicas: 1
  selector:
    app: xray-extractor 
  template:
    metadata:
      labels:
        app: xray-extractor 
    spec:
      containers:
      - name: xray-extractor
        image: t2c2/xray-extractor
        env:
        - name: "RABBITMQ_URL"
          value: "amqp://guest:guest@$RABBITMQ_IP:5672/%2f"
        imagePullPolicy: Always
