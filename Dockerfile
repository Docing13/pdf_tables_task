# FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-runtime


# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libgl1 \
#     libglib2.0-0 \
#  && rm -rf /var/lib/apt/lists/*

#  WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 8000

# ENV NAME Table-Dect-API

# CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]



# Базовый образ с PyTorch и CUDA
FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-runtime

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /app
# Добавляем /app в PYTHONPATH
ENV PYTHONPATH=/app
# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Проверяем, что api.py существует
RUN ls -la /app

# Запуск uvicorn через python -m, чтобы точно из окружения
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

