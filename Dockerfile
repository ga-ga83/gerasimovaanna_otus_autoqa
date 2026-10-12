FROM python:3.11-slim-bookworm

# Передаём UID и GID из Jenkins (по умолчанию 1000:1000)
ARG UID=1000
ARG GID=1000

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

# ── Создаём непривилегированного пользователя с переданным UID/GID ──
# Важно: сначала создаём группу с нужным GID, потом пользователя с нужным UID
RUN groupadd -r testuser -g ${GID} && \
    useradd -r -u ${UID} -g testuser -G audio,video testuser && \
    mkdir -p /home/testuser/Downloads /app/reports /app/allure-results /app/screenshots

# Выставляем права на все директории под этого пользователя
RUN chown -R testuser:testuser /home/testuser /app

# Переключаемся на непривилегированного пользователя
USER testuser

CMD ["pytest", "-v"]

