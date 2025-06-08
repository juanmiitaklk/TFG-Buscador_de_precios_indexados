# 🛒 IndexPrice

Este proyecto forma parte de un Trabajo de Fin de Grado (TFG) y consiste en una aplicación web fullstack que permite **buscar productos en múltiples tiendas online y comparar precios** desde una única interfaz. Utiliza técnicas de scraping, filtros dinámicos y motores de búsqueda personalizados.

---

## 🚀 Funcionalidades principales

- 🔍 **Búsqueda de productos** por nombre clave.
- 🛍️ **Selección de tiendas** mediante checkboxes.
- 📉 **Filtrado de precios** por rango mínimo y máximo.
- ⚙️ **Elección de motor de búsqueda:** Google, Bing o DuckDuckGo.
- 🖼️ Resultados enriquecidos con **título, imagen, descripción y precio**.
- 👤 **Gestión de usuarios**: registro, inicio de sesión, edición y eliminación.
- ⏳ **Animación de carga personalizada** mientras se realiza la búsqueda.
- 🌙 **Diseño responsive y oscuro**, enfocado en usabilidad moderna.

---
## ⚙️ Tecnologías utilizadas

- **Backend:** Flask, SQLAlchemy, SQLite
- **Frontend:** Astro, TailwindCSS, JavaScript
- **Scraping:** Selenium + BeautifulSoup
- **Base de datos:** SQLite 3
- **Extras:** WebDriver Manager, dotenv, logging personalizado

---

## 📝 Instalación local

### Backend (Python 3.11+)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

### Frontend (Node.js 18+)
```cd frontend
npm install
npm run dev
```

#### Accede en http://localhost:3000/


## 🔐 Usuarios y acceso
El sistema permite registrar nuevos usuarios, iniciar sesión, modificar o eliminar su perfil.

### Nota: las contraseñas deben cifrarse en producción (actualmente se almacenan en texto plano por simplicidad de pruebas).


## ✅ Estado del proyecto
Característica	Estado
Proyecto funcional	✔
Búsqueda en múltiples tiendas	✔
Scraping operativo	✔
Interfaz moderna y usable	✔
Persistencia de productos	✘
Autenticación avanzada (JWT)	✘

---
## 📦 Licencia
Este proyecto ha sido desarrollado como parte de un Trabajo de Fin de Grado con fines educativos y no comerciales.
© Juan Manuel González Díaz, 2025. Todos los derechos reservados.
---