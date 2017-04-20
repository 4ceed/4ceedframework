apiVersion: v1
kind: ReplicationController
metadata:
  name: t2c2curator
  namespace: 4ceed
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: t2c2curator
    spec:
      containers:
      - name: t2c2curator
        image: t2c2/4ceedcurator:17.04
        env:
        # Environmental variables for container
        - name: "CLOWDER_CONTEXT"
          value: "/"
        - name: "CLOWDER_ADMINS"
          value: "$ADMIN_EMAIL"
        - name: "MONGO_URI"
          value: "mongodb://$MONGODB_IP:27017/clowder"
        - name: "SMTP_HOST"
          value: "$SMTP_SERVER"
        - name: "RABBITMQ_EXCHANGE"
          value: "clowder"
        - name: "RABBITMQ_VHOST"
          value: "%2F"
        - name: "RABBITMQ_URI"
          value: "amqp://guest:guest@$RABBITMQ_IP:5672/%2f"
        - name: "RABBITMQ_MGMT_PORT"
          value: "15672"
        - name: "ELASTICSEARCH_SERVICE_CLUSTERNAME"
          value: "myesdb"
        - name: "ELASTICSEARCH_SERVICE_SERVER"
          value: "$ELASTICSEARCH_IP"
        - name: "ELASTICSEARCH_SERVICE_PORT"
          value: "9300"
        - name: "UPDATE_MONGODB"
          value: "true"
        - name: "TOOLMANAGER_URI"
          value: ""
        ports:
        - containerPort: 9000
        stdin: true
        imagePullPolicy: Always
