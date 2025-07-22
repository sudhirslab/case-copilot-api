install:
	./run.sh

test:
	uvicorn main:app --reload

clean:
	rm -rf .venv
	rm -rf .env
	rm -rf .pytest_cache
	rm -rf __pycache__

