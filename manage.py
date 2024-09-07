import os
import subprocess
import sys


def run():
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["ENV"] = "dev"
    env["POSTGRES_URL"] = "postgresql+asyncpg://user:password@localhost:5433/db"
    env["REDIS_PWD"] = "password"
    env["SESSION_TIMEOUT_SECONDS"] = "600"
    subprocess.run(["uvicorn", "app.main:app", "--reload"], env=env)


def test():
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["ENV"] = "test"
    env["POSTGRES_URL"] = "postgresql+asyncpg://user:password@localhost:5433/db"
    env["REDIS_PWD"] = "password"
    env["SESSION_TIMEOUT_SECONDS"] = "600"
    subprocess.run(["pytest", "tests", "-s"], env=env)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Unknown command")
    elif sys.argv[1] == "run":
        run()
    elif sys.argv[1] == "test":
        test()
    else:
        print("Unknown command")
