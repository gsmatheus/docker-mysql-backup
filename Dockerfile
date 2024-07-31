# Usando uma imagem base do Python
FROM python:3.9-slim

# Definindo o diretório de trabalho
WORKDIR /app

# Instalando o MySQL client, cron e outras dependências do sistema
RUN apt-get update && apt-get install -y \
  default-mysql-client \
  cron \
  && rm -rf /var/lib/apt/lists/*

# Copiando o requirements.txt e instalando as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o script Python e o arquivo de configuração do cron para o contêiner
COPY backup_script.py .
COPY crontab /etc/cron.d/backup-cron

# Dando permissões corretas ao arquivo de configuração do cron
RUN chmod 0644 /etc/cron.d/backup-cron

# Aplicando o arquivo de configuração do cron
RUN crontab /etc/cron.d/backup-cron

# Adicionando o cron para rodar em foreground e garantir que o contêiner continue rodando
CMD ["cron", "-f"]
