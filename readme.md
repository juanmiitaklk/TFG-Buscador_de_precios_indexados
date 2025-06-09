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
cd ..
set FLASK_APP=backend.app:create_app
set FLASK_ENV=development
flask run
```

### Frontend (Node.js 18+)
```cd frontend
npm install
npm run dev
```

#### Accede en http://localhost:4321/


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


## Presentación
https://view.genially.com/6845e6479ac5b8c8009942c1/presentation-tfg-juan-manuel-gonzalez-diaz

## 📄 Licencia

Este proyecto está licenciado bajo los términos de la **MIT License**.  
Consulta el archivo [LICENSE](./LICENSE) para más detalles.

---