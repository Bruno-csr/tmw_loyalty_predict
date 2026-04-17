CONDA_ENV=loyalty-predict
ENGINEERING_DIR=src/engineering
ANALYTICS_DIR=src/analytics
VENV_DIR=.venv

.PHONY: setup
setup:
	@echo "Criando ambiente virtual..."
	if exist $(VENV_DIR) rmdir /s /q $(VENV_DIR)

	python -m venv $(VENV_DIR)

	@echo "Instalando pipreqs..."
	$(VENV_DIR)\Scripts\pip.exe install pipreqs

	if exist requirements.txt del /f /q requirements.txt

	@echo "Atualizando requirements.txt..."
	$(VENV_DIR)\Scripts\pipreqs.exe src/ --force --savepath requirements.txt --encoding utf-8

	@echo "Corrigindo versão do pandas..."
	$(VENV_DIR)\Scripts\python.exe -c "import re; content=open('requirements.txt','r',encoding='utf-8').read(); open('requirements.txt','w',encoding='utf-8').write(re.sub(r'pandas==[\d.]+', 'pandas==2.2.3', content))"

	@echo "Instalando dependências..."
	$(VENV_DIR)\Scripts\pip.exe install -r requirements.txt

.PHONY: run
run:
	@echo "Executando pipeline..."
	cd src\engineering && python get_data.py
	cd src\analytics && python pipeline_analytics.py

all: setup run