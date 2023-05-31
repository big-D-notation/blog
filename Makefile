# Інсталяція Python та збірка проекту
setup:
    sudo apt-get install python3
    pip install -r requirements.txt

# Запуск сервера Flask
run:
    python3 app.py

# Видалення залежностей
clean:
    rm -rf venv
    rm -rf __pycache__
    rm -f *.pyc

# Загальна задача для зборки та запуску
all: setup run

.PHONY: setup run clean all
