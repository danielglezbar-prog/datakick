from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.v1.endpoints import quiniela

# ─── App ─────────────────────────────────────────────────────────────────────

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    **Datakick API** — Motor analítico para La Quiniela española.

    ## Endpoints principales

    - `/api/v1/quiniela/analizar` — Análisis completo de jornada (Pro/Elite)
    - `/api/v1/quiniela/historico` — Track record público
    - `/api/v1/quiniela/waitlist` — Registro de interesados

    ## Autenticación
    Próximamente: Bearer token JWT via Supabase Auth.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── CORS ────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "https://datakick.es",
        "https://www.datakick.es",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ─────────────────────────────────────────────────────────────────

app.include_router(quiniela.router, prefix="/api/v1")

# ─── Health check ────────────────────────────────────────────────────────────

@app.get("/", include_in_schema=False)
async def root():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}

@app.get("/health", tags=["sistema"])
async def health():
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }

# ─── Exception handlers ──────────────────────────────────────────────────────

@app.exception_handler(404)
async def not_found(request, exc):
    return JSONResponse(status_code=404, content={"error": "Endpoint no encontrado"})

@app.exception_handler(500)
async def server_error(request, exc):
    return JSONResponse(status_code=500, content={"error": "Error interno del servidor"})
