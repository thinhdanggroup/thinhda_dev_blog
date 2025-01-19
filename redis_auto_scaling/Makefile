


run-worker:
	@echo "Running worker"
	@celery -A tasks worker -Q low_priority,high_priority --loglevel=info

hpa-events:
	@echo "Running HPA events"
	@kubectl describe hpa keda-hpa-redis-scaledobject --namespace default