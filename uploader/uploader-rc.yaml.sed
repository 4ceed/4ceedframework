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
        image: t2c2/4ceeduploader
        env:
        - name: "CURATOR_HOME"
          value: "http://$CURATOR_IP:32500/"
        - name: "CURATOR_API_URL"
          value: "http://$CURATOR_IP:32500/api/"
        - name: "UPLOADER_HOME"
          value: "http://$UPLOADER_IP:32000/4ceeduploader/"
        ports:
        - containerPort: 8000
        imagePullPolicy: Always
