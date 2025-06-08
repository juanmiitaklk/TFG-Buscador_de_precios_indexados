# 🛒 Buscador de Precios Indexados

Este proyecto es un TFG que consiste en una aplicación web que permite **buscar productos en varias tiendas online** y comparar sus precios de forma centralizada. Utiliza técnicas de scraping, procesamiento dinámico y filtros personalizados para mostrar resultados útiles al usuario.

## 📌 Funcionalidades

- 🔍 Búsqueda de productos por palabra clave.
- 🛍️ Selección de múltiples tiendas (checkboxes personalizados).
- 📉 Filtros por precio mínimo y máximo.
- ⚙️ Elección de motor de búsqueda (Google, Bing, DuckDuckGo).
- 🖼️ Resultados con título, descripción, precio e imagen.
- ✅ Sistema de usuarios: registro, login, edición y eliminación.
- ⏳ Loader animado mientras se realiza la búsqueda.
- ⚠️ Detección automática de CAPTCHA y aviso al usuario.
- 🌙 Diseño adaptado a fondo oscuro con estética moderna.

## 🧱 Estructura del proyecto

📦 TFG/
├── backend/
│   ├── app.py                # Punto de entrada del servidor Flask
│   ├── config.py             # Configuración principal (SQLite, claves, etc.)
│   ├── extensions.py         # Inicialización de SQLAlchemy y migraciones
│   ├── requirements.txt      # Dependencias Python
│   ├── modelos/              # Modelos de base de datos (Usuario, Producto)
│   ├── rutas/                # Rutas API REST (login, registro, búsqueda)
│   ├── utils/                # Scraper con Selenium y logger
│   └── migrations/           # (opcional) Control de versiones para la DB

├── frontend/
│   ├── public/               # Imágenes, favicon, fondos
│   ├── src/
│   │   ├── assets/           # Recursos estáticos (si los hubiera)
│   │   ├── components/       # Componentes como Header, Filtros, etc.
│   │   ├── layouts/          # Layouts compartidos (p.ej. base HTML)
│   │   ├── pages/            # Páginas Astro (index, login, register, ayuda)
│   │   └── styles/           # Estilos globales y personalizados
│   ├── astro.config.mjs      # Configuración Astro
│   ├── tailwind.config.js    # Configuración TailwindCSS
│   └── package.json          # Dependencias y scripts del frontend

├── instance/
│   └── db.sqlite3            # Base de datos local SQLite

├── logs/
│   ├── scraper.log           # Log del scraper
│   ├── ReiniciarIP.txt       # Registro/manual sobre IPs
│   └── run_backend.txt       # Script o instrucciones de backend

├── .gitignore
└── README.md