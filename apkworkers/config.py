from kombu import Queue

# TASKS
task_acks_late = True
task_serializer = "json"
task_compression = "bzip2"
task_ignore_result = True
task_store_errors_even_if_ignored = True

# RESULTS
result_persist = True
result_serializer = "json"
result_compression = "bzip2"
result_backend = "elasticsearch://localhost:9200/celery/tasks"

# ROUTING
task_default_queue = "default"
task_queues = [
    Queue("default"),
    Queue("apklyze"),
    Queue("analysis"),
    Queue("virustotal"),
]
task_routes = {"apkworkers.actions.vt*": {"queue": "virustotal"}}

# BROKER
broker_user = "celery"
broker_password = "[BROKER_PASSWORD]"
broker_server = "localhost"
broker_vhost = "apkworkers"
broker_port = "5672"
broker_url = "amqp://{0}:{1}@{2}:{3}/{4}".format(
    broker_user, broker_password, broker_server, broker_port, broker_vhost
)
# COUCH
couch_endpoint = "http://localhost:5984/"

# ELASTIC
elastic_urls = "localhost"

# ANDROZOO
androzoo_apiurl = "https://androzoo.uni.lu/api/"
androzoo_apikey = "[ANDROZOO_APIKEY]"

# VIRUSTOTAL
virustotal_apikey = "[VIRUSTOTAL_APIKEY]"
