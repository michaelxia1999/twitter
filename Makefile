export PYTHONDONTWRITEBYTECODE=1
export ENV=dev
export POSTGRES_URL=postgresql+asyncpg://user:password@localhost:5433/db
export REDIS_PWD=password
export SESSION_TIMEOUT_SECONDS=600

run:
	uvicorn app.main:app --reload

test:
	pytest -p no:cacheprovider -s
