.PHONY: up donw app mcp mcpd

up:
	docker compose up -d
down:
	docker-compose down
app:
	source app/.venv/bin/activate && cd app && python app.py
mcp:
	npx @playwright/mcp  --port 8931 --host 0.0.0.0 --allowed-hosts '*'
mcpd:
	pkill -f playwright