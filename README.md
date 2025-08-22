
# Flask Expenses Manager (Render + Neon)

Pequeña app web para gestionar **gastos**, **servicios del hogar** y ver **estadísticas**, hecha con **Flask + PostgreSQL**. Lista para desplegar en **Render** y usar **Neon** como base de datos.

## Características
- Registro e inicio de sesión (Flask-Login).
- Gestión de **Gastos** (monto, fecha, categoría, método de pago, descripción).
- Gestión de **Servicios del hogar** (nombre, proveedor, día de vencimiento, monto estimado, notas).
- Estadísticas: totales del mes, por categoría y últimos 6 meses, con gráficos **Chart.js**.
- UI simple con **Bootstrap 5**.
- Compatible con **Neon** (usa `sslmode=require`).

## Requisitos
- Python 3.10+ (probado con 3.11).
- Una base de datos Postgres (Neon) y su `DATABASE_URL` (con `?sslmode=require`).
- En Render configurar variables de entorno.

## Variables de entorno
Crea un archivo `.env` (para local) basado en `.env.example`:
```
FLASK_ENV=production
SECRET_KEY=super-secret-change-me
DATABASE_URL=postgresql+psycopg2://<user>:<pass>@<host>/<db>?sslmode=require
```
> Nota: Si `DATABASE_URL` no tiene `postgresql+psycopg2`, la app intenta corregirlo automáticamente.
> Si no incluye `sslmode=require`, también se agrega automáticamente para Neon.

## Correr localmente
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Crear DB (si no existen tablas)
export $(cat .env | xargs)  # en Windows usar: set VAR=... por cada una
flask init-db

# Ejecutar
flask run  # http://127.0.0.1:5000
```
Usuario inicial: crea una cuenta en `/auth/register`.

## Despliegue en Render
1. Subí este repo a GitHub.
2. En Render, crea un **Web Service** desde el repo.
3. En **Environment** agregar variables:
   - `SECRET_KEY`: un valor aleatorio largo.
   - `DATABASE_URL`: la URL de Neon; si no tiene `?sslmode=require`, agrégalo.
4. Render detectará `Python`.
5. **Start command**: `gunicorn wsgi:app`
6. Primer deploy: Render crea el contenedor. Una vez arriba, corre `/auth/register` para crear tu usuario.

> También podés usar el `render.yaml` incluido creando un **Blueprint**.
