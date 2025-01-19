# in container
broker_url = "redis://:abc123@redis:6379/0"
result_backend = "redis://:abc123@redis:6379/0"

# localhost
# broker_url = "redis://:abc123@localhost:6479/0"
# result_backend= broker_url

broker_transport_options = {
    "visibility_timeout": 3600,  # 1 hour
}

result_backend_transport_options = {
    "retry_on_timeout": True,
}

task_default_queue = "default"

task_queues = {
    "low_priority": {
        "exchange": "low_priority",
        "routing_key": "redis.low_priority",
    },
    "high_priority": {
        "exchange": "high_priority",
        "routing_key": "redis.high_priority",
    },
    "default": {"exchange": "default", "routing_key": "redis.default"},
}
