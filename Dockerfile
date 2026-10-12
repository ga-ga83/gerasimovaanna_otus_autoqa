FROM python:3.11-slim-bookworm

# Работаем от root, чтобы ставить пакеты и создавать пользователя
USER root
WORKDIR /app

# ── Системные зависимости для Chrome и Firefox ──
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    ca-certificates \
    curl \
    unzip \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxkbcommon0 \
    libpangocairo-1.0-0 \
    xdg-utils \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# ── Установка Google Chrome ──
RUN wget -q -O /tmp/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y /tmp/google-chrome.deb \
    && rm /tmp/google-chrome.deb \
    && rm -rf /var/lib/apt/lists/*

# ── Python-зависимости ──
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Копируем весь код проекта ──
COPY . .

# ── Создаём непривилегированного пользователя и выставляем права ──
# Сначала создаём пользователя и домашнюю папку
RUN groupadd -r testuser && useradd -r -g testuser -G audio,video testuser \
    && mkdir -p /home/testuser/Downloads

# ВАЖНО: отдаём права на всю рабочую директорию /app (включая все файлы из COPY)
# Это решает PermissionError при записи Allure-результатов
RUN chown -R testuser:testuser /home/testuser /app

# Переключаемся на непривилегированного пользователя
USER testuser

CMD ["pytest", "-v"]
