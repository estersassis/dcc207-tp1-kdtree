# Instalar dependências
install:
	pip install -r requirements.txt

# Rodar o app
run:
	PORT=8000 python -m app.server

# Rodar testes
test:
	pytest -v tests

scrape:
	python scripts/scrape_buteco.py

# Rodar testes e depois o app
all: install test run
