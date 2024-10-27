FROM python:3.11-slim

# Установка необходимых пакетов
#RUN apt-get update && apt-get install -y \
#    grpcio-tools

# Установка pip пакетов
RUN pip install --upgrade pip
RUN pip install grpcio grpcio-tools


# Создание рабочей директории
WORKDIR /app

# Копирование файлов в рабочую директорию
COPY . /app

# Установка переменных окружения
#ENV PATH=$PATH:/app

# Команда для запуска приложения
#CMD ["python", "-m", "grpc_tools.protoc", "-I protos", "--python_out=.", "--pyi_out=.", "--grpc_python_out=.", "protos/ship.proto"]

CMD ["python", "ship.py"]