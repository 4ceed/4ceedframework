apiVersion: v1
kind: ReplicationController
metadata:
  name: dm3-extractor
spec:
  replicas: 1
  selector:
    app: dm3-extractor 
  template:
    metadata:
      labels:
        app: dm3-extractor 
    spec:
      containers:
      - name: dm3-extractor
        image: t2c2/dm3-extractor
        env:
        - name: "RABBITMQ_URL"
          value: "$RABBITMQ_IP"
        imagePullPolicy: Always
