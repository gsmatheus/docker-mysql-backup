# Usando uma imagem base do Python
FROM python:3.9-slim

# Definindo o diretório de trabalho
WORKDIR /app

# Instalando o MySQL client e outras dependências do sistema
RUN apt-get update && apt-get install -y \
  default-mysql-client \
  && rm -rf /var/lib/apt/lists/*

# Copiando o requirements.txt e instalando as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o script Python para o contêiner
COPY backup_script.py .

# Definindo o comando padrão para rodar o script
CMD ["python", "backup_script.py"]
