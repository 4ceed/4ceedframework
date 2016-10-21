apiVersion: v1
kind: ReplicationController
metadata:
  name: sem-extractor
  namespace: 4ceed
spec:
  replicas: 1
  selector:
    app: sem-extractor 
  template:
    metadata:
      labels:
        app: sem-extractor 
    spec:
      containers:
      - name: sem-extractor
        image: t2c2/sem-extractor
        env:
        - name: "RABBITMQ_URL"
          value: "$RABBITMQ_IP"
        - name: "CLOWDER_URL"
          value: "$CURATOR_ADDR"
        - name: "CLOWDER_PORT"
          value: "32500"
        - name: "CRED_NAME"
          value: "guest"
        - name: "CRED_PASS"
          value: "guest"
        - name: "SERVER_KEY"
          value: "phuong-test"
        - name: "EXCHANGE_NAME"
          value: "clowder"
        - name: "USE_SSL"
          value: "false"
        - name: "MESSAGE_TYPE"
          value: "*.dataset.file.added"
        imagePullPolicy: Always
