'use client'

import { useState } from 'react'
import { ArrowRight, BarChart2, Zap, Shield, TrendingUp, ChevronDown, Check } from 'lucide-react'

// ─── Datos de ejemplo para el hero ───────────────────────────────────────────

const SAMPLE_JORNADA = {
  numero: 65,
  partidos: [
    { local: 'Real Madrid',    visitante: 'Barcelona',     prob: [52, 22, 26], bomba: false, signo: '1' },
    { local: 'Atlético',       visitante: 'Sevilla',       prob: [48, 26, 26], bomba: false, signo: '1' },
    { local: 'Athletic',       visitante: 'Betis',         prob: [35, 28, 37], bomba: true,  signo: 'X' },
    { local: 'Valencia',       visitante: 'Villarreal',    prob: [38, 30, 32], bomba: false, signo: 'X' },
    { local: 'Osasuna',        visitante: 'Getafe',        prob: [44, 28, 28], bomba: false, signo: '1' },
  ]
}

// ─── Componentes de UI ────────────────────────────────────────────────────────

function Nav() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-brand-border bg-brand-night/80 backdrop-blur-md">
      <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
        <div className="flex items-center gap-1.5">
          <div className="w-6 h-6 rounded bg-brand-accent flex items-center justify-center">
            <BarChart2 size={13} className="text-brand-night" />
          </div>
          <span className="font-semibold text-white tracking-tight">Datakick</span>
        </div>
        <div className="hidden md:flex items-center gap-6">
          <a href="#como-funciona" className="nav-link">Cómo funciona</a>
          <a href="#precios" className="nav-link">Precios</a>
          <a href="#resultados" className="nav-link">Resultados</a>
        </div>
        <div className="flex items-center gap-3">
          <a href="/login" className="nav-link hidden md:block">Entrar</a>
          <a href="#waitlist" className="btn-primary py-1.5 px-4 text-xs">
            Acceso anticipado
          </a>
        </div>
      </div>
    </nav>
  )
}

function HeroPreview() {
  return (
    <div className="card border-brand-accent/30 bg-brand-dark/80 backdrop-blur overflow-hidden">
      <div className="flex items-center justify-between mb-4">
        <div>
          <span className="text-xs text-brand-muted uppercase tracking-wider">Jornada {SAMPLE_JORNADA.numero}</span>
          <div className="flex items-center gap-2 mt-0.5">
            <span className="text-sm font-medium text-white">Análisis pre-jornada</span>
            <span className="badge-accent text-2xs">EN VIVO</span>
          </div>
        </div>
        <div className="text-right">
          <div className="text-xs text-brand-muted">Rentabilidad esperada</div>
          <div className="text-lg font-semibold text-brand-accent">+12.4%</div>
        </div>
      </div>

      <div className="space-y-1.5">
        {SAMPLE_JORNADA.partidos.map((p, i) => (
          <div key={i} className={`flex items-center gap-3 rounded-lg px-3 py-2 ${p.bomba ? 'bg-brand-accent/10 border border-brand-accent/20' : 'bg-white/3'}`}>
            <div className={`w-6 h-6 rounded flex items-center justify-center text-xs font-bold flex-shrink-0 ${
              p.signo === '1' ? 'bg-blue-500/20 text-blue-400' :
              p.signo === 'X' ? 'bg-amber-500/20 text-amber-400' :
              'bg-red-500/20 text-red-400'
            }`}>
              {p.signo}
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-xs text-white truncate">{p.local} — {p.visitante}</div>
              <div className="flex gap-1.5 mt-1">
                <div className="h-1 rounded-full bg-blue-500/70" style={{width: `${p.prob[0]}%`, maxWidth: '60%'}} />
                <div className="h-1 rounded-full bg-amber-500/70" style={{width: `${p.prob[1] * 0.6}%`}} />
                <div className="h-1 rounded-full bg-red-500/50"  style={{width: `${p.prob[2] * 0.6}%`}} />
              </div>
            </div>
            {p.bomba && (
              <div className="flex items-center gap-1 text-2xs text-brand-accent font-medium flex-shrink-0">
                <Zap size={10} />BOMBA
              </div>
            )}
            <div className="text-xs text-brand-muted flex-shrink-0 font-mono">
              {p.prob[0]}·{p.prob[1]}·{p.prob[2]}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 pt-3 border-t border-brand-border flex items-center justify-between">
        <div className="text-xs text-brand-muted">Motor v2.1 · 16 reglas activas</div>
        <button className="text-xs text-brand-accent hover:underline flex items-center gap-1">
          Descargar HTML <ArrowRight size={10} />
        </button>
      </div>
    </div>
  )
}

function WaitlistForm() {
  const [email, setEmail] = useState('')
  const [status, setStatus] = useState<'idle' | 'loading' | 'done'>('idle')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!email) return
    setStatus('loading')
    // TODO: conectar a Supabase
    await new Promise(r => setTimeout(r, 800))
    setStatus('done')
  }

  if (status === 'done') {
    return (
      <div className="flex items-center gap-2 text-brand-accent text-sm">
        <Check size={16} />
        <span>Apuntado. Te avisamos cuando abramos acceso.</span>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 max-w-sm">
      <input
        type="email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="tu@email.com"
        className="input flex-1"
        required
      />
      <button type="submit" className="btn-primary whitespace-nowrap" disabled={status === 'loading'}>
        {status === 'loading' ? '...' : 'Unirme'}
      </button>
    </form>
  )
}

const STATS = [
  { value: '+65', label: 'Jornadas analizadas' },
  { value: '16',  label: 'Reglas del motor' },
  { value: '86%', label: 'Mejor jornada' },
  { value: '€0',  label: 'Para empezar' },
]

const HOW_IT_WORKS = [
  {
    icon: BarChart2,
    title: 'Datos reales, no intuición',
    desc: 'El motor compara probabilidades de casas de apuestas contra el porcentaje de jugadores de LAE. Cuando divergen, hay valor.'
  },
  {
    icon: Zap,
    title: 'Bombazos detectados',
    desc: 'Identificamos los partidos donde la masa se equivoca. Ahí está la rentabilidad esperada que la mayoría no ve.'
  },
  {
    icon: TrendingUp,
    title: 'HTML pre-cargado semanal',
    desc: 'Descarga el archivo de la semana, ábrelo en el navegador y juega con el análisis ya hecho. En 5 minutos, listo.'
  },
  {
    icon: Shield,
    title: 'Track record público',
    desc: 'Publicamos todos los resultados, los buenos y los malos. J64 fue nuestra peor jornada. Lo sabemos. Está en el histórico.'
  },
]

const PLANS = [
  {
    name: 'Free',
    price: '€0',
    period: '/mes',
    desc: 'Para conocer la plataforma',
    features: [
      'Resultado de la jornada anterior',
      'Histórico últimas 4 jornadas',
      '1 análisis básico por jornada',
    ],
    cta: 'Empezar gratis',
    highlight: false,
  },
  {
    name: 'Pro',
    price: '€9.99',
    period: '/mes',
    desc: 'Para el jugador serio',
    features: [
      'Análisis completo pre-jornada',
      'HTML pre-cargado descargable',
      'Bombazos + rentabilidad esperada',
      'Histórico completo desde J1',
      'Alertas Telegram',
      'Quinigol análisis básico',
    ],
    cta: 'Empezar con Pro',
    highlight: true,
  },
  {
    name: 'Elite',
    price: '€19.99',
    period: '/mes',
    desc: 'Para el analítico total',
    features: [
      'Todo lo de Pro',
      'Quinigol análisis avanzado',
      'Acceso beta a nuevas funciones',
      'Canal privado de comunidad',
      'API de datos (próximamente)',
    ],
    cta: 'Empezar con Elite',
    highlight: false,
  },
]

// ─── PÁGINA PRINCIPAL ─────────────────────────────────────────────────────────

export default function Home() {
  return (
    <div className="bg-brand-night min-h-screen">
      <Nav />

      {/* ── HERO ─────────────────────────────────────────────────────────── */}
      <section className="pt-28 pb-20 px-6 bg-grid relative overflow-hidden">
        {/* Glow ambiental */}
        <div className="absolute top-20 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-brand-accent/5 rounded-full blur-3xl pointer-events-none" />

        <div className="max-w-6xl mx-auto grid lg:grid-cols-2 gap-16 items-center relative">
          <div>
            <div className="badge-accent mb-5 inline-flex">
              Motor analítico para La Quiniela española
            </div>
            <h1 className="text-4xl md:text-5xl font-semibold leading-tight text-white mb-5">
              La quiniela no es<br />
              <span className="text-gradient">suerte. Es datos.</span>
            </h1>
            <p className="text-brand-muted text-lg leading-relaxed mb-8 max-w-md">
              Analizamos probabilidades reales contra la masa de jugadores LAE.
              Cuando divergen, encontramos valor. Cada semana, antes de la jornada.
            </p>

            <div id="waitlist" className="mb-6">
              <WaitlistForm />
              <p className="text-xs text-brand-muted mt-2">
                Acceso anticipado · Sin tarjeta · Primeros 200 usuarios a mitad de precio
              </p>
            </div>

            <div className="flex flex-wrap gap-x-6 gap-y-2">
              {STATS.map(s => (
                <div key={s.label}>
                  <div className="text-xl font-semibold text-white">{s.value}</div>
                  <div className="text-xs text-brand-muted">{s.label}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="relative">
            <HeroPreview />
            <div className="absolute -bottom-4 -right-4 w-24 h-24 bg-brand-accent/10 rounded-full blur-2xl pointer-events-none" />
          </div>
        </div>
      </section>

      {/* ── CÓMO FUNCIONA ────────────────────────────────────────────────── */}
      <section id="como-funciona" className="py-20 px-6 border-t border-brand-border">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <p className="text-brand-accent text-sm font-medium uppercase tracking-wider mb-3">Metodología</p>
            <h2 className="text-3xl font-semibold text-white">El motor, explicado</h2>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {HOW_IT_WORKS.map((item, i) => (
              <div key={i} className="card hover:border-brand-accent/30 transition-colors">
                <div className="w-9 h-9 rounded-lg bg-brand-accent/10 flex items-center justify-center mb-4">
                  <item.icon size={18} className="text-brand-accent" />
                </div>
                <h3 className="text-sm font-medium text-white mb-2">{item.title}</h3>
                <p className="text-xs text-brand-muted leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── PRECIOS ──────────────────────────────────────────────────────── */}
      <section id="precios" className="py-20 px-6 border-t border-brand-border">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-14">
            <p className="text-brand-accent text-sm font-medium uppercase tracking-wider mb-3">Precios</p>
            <h2 className="text-3xl font-semibold text-white">Sin letra pequeña</h2>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {PLANS.map((plan, i) => (
              <div key={i} className={`card flex flex-col ${plan.highlight ? 'border-brand-accent bg-brand-accent/5' : ''}`}>
                {plan.highlight && (
                  <div className="badge-accent self-start mb-3">Más popular</div>
                )}
                <div className="mb-1">
                  <span className="text-sm font-medium text-white">{plan.name}</span>
                </div>
                <div className="flex items-baseline gap-1 mb-1">
                  <span className="text-3xl font-semibold text-white">{plan.price}</span>
                  <span className="text-brand-muted text-sm">{plan.period}</span>
                </div>
                <p className="text-xs text-brand-muted mb-5">{plan.desc}</p>
                <ul className="space-y-2 mb-6 flex-1">
                  {plan.features.map((f, j) => (
                    <li key={j} className="flex items-start gap-2 text-xs text-brand-muted">
                      <Check size={12} className="text-brand-accent mt-0.5 flex-shrink-0" />
                      {f}
                    </li>
                  ))}
                </ul>
                <button className={plan.highlight ? 'btn-primary justify-center' : 'btn-secondary justify-center'}>
                  {plan.cta}
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA FINAL ────────────────────────────────────────────────────── */}
      <section className="py-20 px-6 border-t border-brand-border">
        <div className="max-w-xl mx-auto text-center">
          <h2 className="text-3xl font-semibold text-white mb-4">
            La próxima jornada<br />empieza el viernes.
          </h2>
          <p className="text-brand-muted mb-8">
            Únete antes del viernes y recibe el análisis de la jornada 65 gratis.
          </p>
          <WaitlistForm />
        </div>
      </section>

      {/* ── FOOTER ───────────────────────────────────────────────────────── */}
      <footer className="border-t border-brand-border py-8 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-1.5">
            <div className="w-5 h-5 rounded bg-brand-accent/20 flex items-center justify-center">
              <BarChart2 size={11} className="text-brand-accent" />
            </div>
            <span className="text-sm font-medium text-white">Datakick</span>
          </div>
          <p className="text-xs text-brand-muted">
            Datakick es una herramienta de análisis estadístico. No constituye asesoramiento de apuestas.
            El juego puede crear adicción. Juega con responsabilidad.
          </p>
          <div className="flex gap-4 text-xs text-brand-muted">
            <a href="/privacidad" className="hover:text-white transition-colors">Privacidad</a>
            <a href="/terminos" className="hover:text-white transition-colors">Términos</a>
          </div>
        </div>
      </footer>
    </div>
  )
}
