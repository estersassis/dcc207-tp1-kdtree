# Instalar dependências
install:
	pip install -r requirements.txt

# Rodar o app
run:
	python -m app.server

# Rodar testes
test:
	pytest -v tests

scrape:
	python scripts/scrape_buteco.py

# Rodar testes e depois o app
all: install test run
