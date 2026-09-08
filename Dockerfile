FROM python:3.13-slim-trixie

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
    # Firefox ESR — доступен в репозиториях Debian Trixie
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# ── Установка Google Chrome ──
RUN wget -q -O /tmp/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y /tmp/google-chrome.deb \
    && rm /tmp/google-chrome.deb \
    && rm -rf /var/lib/apt/lists/*

# ── Python-зависимости ──
RUN pip install --no-cache-dir pytest requests selenium allure-pytest

COPY . .

# ── Создание непривилегированного пользователя ──
# Chrome отказывается работать от root
RUN groupadd -r testuser && useradd -r -g testuser -G audio,video testuser \
    && mkdir -p /home/testuser/Downloads \
    && chown -R testuser:testuser /home/testuser \
    && chown -R testuser:testuser /app

USER testuser

CMD ["pytest", "-v"]