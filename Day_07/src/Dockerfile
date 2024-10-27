# Используем официальный образ Sphinx
FROM sphinxdoc/sphinx

# Создаём общую папку для проекта
RUN mkdir -p /app

# Копируем текущую директорию в общую папку
COPY . /app/

# Переходим в общую папку
WORKDIR /app

# Устанавливаем зависимости
RUN pip install sphinx && pip install pytest
