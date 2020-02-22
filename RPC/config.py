#RabbitMQ Settings
RABBIT_MQ_QUEUE_NAME = 'predictions'
RABBIT_MQ_SERVER = 'localhost'
RABBIT_MQ_PORT = 5672
RABBIT_MQ_USERNAME = 'user'
RABBIT_MQ_PASSWORD = 'bitnami'
RABBIT_MQ_VIRTUAL_HOST= '/'
RABBIT_MQ_ROUTING_KEY = 'response_queue'
RABBIT_MQ_EXCHANGE = ''

#Prediction url from app.py and app_kinda_ab_testing.py
PREDICTION_URL_DEV = 'http://localhost:5001/results'
PREDICTION_URL_PROD = 'http://localhost:5000/results'

#DB settings
DB_NAME = 'presencedb'
DB_USER_NAME = 'root'
DB_PASSWORD = '@Entelect'
DB_PROD_TABLE = "predictions_production"
DB_DEV_TABLE = "predictions_ab_tests"


