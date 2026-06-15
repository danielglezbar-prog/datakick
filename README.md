# Datakick

> Inteligencia de datos para el fútbol que juegas.

Plataforma de análisis estadístico para La Quiniela y mercados de fútbol español.

## Stack

| Capa | Tecnología | Hosting |
|------|-----------|---------|
| Frontend | Next.js 14 + Tailwind | Vercel (gratis) |
| Backend API | Python 3.11 + FastAPI | Railway (~€5/mes) |
| Base de datos | PostgreSQL (Supabase) | Supabase (gratis) |
| Auth | Supabase Auth | Supabase |
| Pagos | Stripe | Stripe (1.5% + €0.25) |
| Odds | The Odds API | €20/mes |
| Email | Resend | Gratis hasta 3K/mes |

## Arrancar en local

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Rellena las variables
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env.local  # Rellena las variables
npm run dev
```

Frontend en http://localhost:3000
API docs en http://localhost:8000/docs

## Estructura

```
datakick/
├── frontend/          # Next.js 14
│   ├── app/
│   │   ├── marketing/ # Landing, pricing (público)
│   │   └── dashboard/ # App autenticada
│   ├── components/
│   │   ├── ui/        # Botones, cards, inputs
│   │   ├── layout/    # Nav, footer, sidebar
│   │   └── quiniela/  # Componentes específicos
│   └── lib/           # Supabase client, utils
│
└── backend/           # FastAPI
    └── app/
        ├── api/v1/    # Endpoints REST
        ├── core/      # Config, seguridad
        ├── models/    # Modelos SQLAlchemy
        ├── schemas/   # Schemas Pydantic
        └── services/  # Lógica de negocio (motor QuinielaAI)
```

## Fases

- **Fase 1** (ahora): MVP — suscripciones + motor quiniela
- **Fase 2** (mes 4): SEO + afiliación + Quinigol  
- **Fase 3** (mes 9): API B2B + app móvil
- **Fase 4** (mes 18): Marketplace tipsters
