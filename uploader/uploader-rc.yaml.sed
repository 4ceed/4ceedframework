apiVersion: v1
kind: ReplicationController
metadata:
  name: t2c2uploader 
  namespace: 4ceed
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: t2c2uploader 
    spec:
      containers:
      - name: t2c2uploader 
        image: t2c2/4ceeduploader:16.10.2
        env:
        - name: "CURATOR_HOME"
          value: "$CURATOR_ADDR/"
        - name: "CURATOR_API_URL"
          value: "$CURATOR_ADDR/api/"
        - name: "UPLOADER_HOME"
          value: "$UPLOADER_ADDR"
        ports:
        - containerPort: 8000
        imagePullPolicy: Always
