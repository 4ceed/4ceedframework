apiVersion: v1
kind: ReplicationController
metadata:
  name: image-preview-extractor
  namespace: 4ceed
spec:
  replicas: 1
  selector:
    app: image-preview-extractor
  template:
    metadata:
      labels:
        app: image-preview-extractor
    spec:
      containers:
      - name: image-preview-extractor
        image: t2c2/image-preview-extractor
        env:
        - name: "RABBITMQ_URL"
          value: "amqp://guest:guest@$RABBITMQ_IP:5672/%2f"
        imagePullPolicy: Always
