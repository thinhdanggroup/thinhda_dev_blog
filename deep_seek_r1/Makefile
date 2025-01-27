
start:
	@docker run -p 3000:3000 --env-file .env -e HF_TOKEN=HF_TOKEN -v db:/data ghcr.io/huggingface/chat-ui-db:latest

install:
	@ollama run deepseek-r1:7b

my-ip:
	@ipconfig getifaddr en0