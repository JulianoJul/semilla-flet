# README.md — Semilla: No gestionas tareas. Cultivas tu día.

# 🌱 Semilla

> **No gestionas tareas. Cultivas tu día.**

App offline-first de cultivo de hábitos construida con Python + Flet. Diseño Neumórfico accesible (WCAG AA). Sin backend, sin autenticación, sin tracking externo.

---

## Arquitectura

```
semilla-flet/
├── core/
│   ├── database/         # DBHelper (SQLite WAL), migrations, seed_data
│   ├── design/           # Tokens, NeuCard, NeuButton, Typography, Animations
│   ├── notifications/    # NotificationService (plyer, graceful degradation)
│   └── container.py      # AppContainer — DI singleton
├── domain/
│   ├── entities/         # Activity, CheckIn, Streak, BadgeEntity, Results
│   ├── repositories/     # Abstract interfaces
│   └── use_cases/        # CreateActivity, CompleteActivity, ManageStreak, …
├── data/
│   ├── datasources/      # SQL queries + mappers (≤120L cada archivo)
│   └── repositories/     # Implementaciones concretas
├── features/
│   ├── onboarding/       # 3 pasos: arquetipo → primera semilla → pacto
│   ├── home/             # HomeView + 5 widgets seccionales
│   ├── activity/         # CreateActivityView (BottomSheet)
│   └── gamification/     # StreakIndicator, ChestWidget, BadgeCelebration
├── tests/
│   └── unit/             # pytest — streak, create_activity, design_system
└── main.py               # Entry point Flet
```

## Capas y reglas

| Capa | Puede importar | No puede importar |
|------|---------------|-------------------|
| `domain/` | nada externo | `data/`, `features/`, `flet` |
| `data/` | `domain/`, `core/` | `features/` |
| `features/` | `domain/`, `core/`, `data/` vía container | otros features |
| `core/design/` | `flet` | `domain/`, `data/`, `features/` |

## Tipos de actividad

| Código | Nombre UI | Sección home |
|--------|-----------|--------------|
| `A` | Hábito | 🔁 Mis hábitos (chips) + Hoy cultivo |
| `B` | Horizonte | 📅 Horizontes (deadlines) |
| `C` | Semilla | 💤 Semillas en espera (backlog) |

## Gamificación

- **Racha** (`streaks`): consecutive daily completions. Grace period de 24h. Escudo consume `shields_available`.
- **Badges**: se desbloquean en `check_and_unlock()` según `condition_type` (`streak`, `total_completions`, `shield_used`).
- **Cofre**: drop probabilístico (40%) con pity timer de 3 días.
- **Planta**: escala visual 0→5 según `total_completions`.

## Design System Neumórfico

Tokens almacenados en tabla `design_tokens` (override desde DB):

```python
color_base     = "#E8EDEA"   # fondo único de toda la app
shadow_dark    = "#B8BDB9"   # sombra inferior-derecha
shadow_light   = "#FFFFFF"   # sombra superior-izquierda
color_primary  = "#2E4A3E"   # texto principal, botón primario
```

Contraste WCAG AA verificado automáticamente vía `check_contrast()`.

## Correr la app

```bash
# Instalar dependencias
uv sync  # o: pip install -r requirements.txt

# Ejecutar
python main.py

# Tests
pytest tests/unit/ -v
```

## Archivos de assets esperados

```
assets/
├── images/plant_stage_0.png  ... plant_stage_5.png
└── sounds/complete.wav
```

Si faltan → `core/asset_helper.py` devuelve placeholders (emoji/silencio).

---

*Semilla no te juzga. Te acompaña.* 🌱
