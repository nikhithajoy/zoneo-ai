.PHONY: install dev backend frontend

install:
	pip3 install -e backend/
	npm install --prefix frontend

dev: ## Start both servers concurrently
	@trap 'kill 0' INT; \
	uvicorn app.main:app --reload --port 8001 --app-dir backend & \
	npm run dev --prefix frontend & \
	wait

backend:
	uvicorn app.main:app --reload --port 8001 --app-dir backend

frontend:
	npm run dev --prefix frontend
