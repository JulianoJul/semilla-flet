"""
core/database/migrations/seed_data.py — INSERT OR IGNORE for all reference tables.
"""

# --- IMPORTS ---
from __future__ import annotations

import sqlite3

_Q = "INSERT OR IGNORE INTO {} ({}) VALUES ({})"


# --- SETTINGS ---
def _seed_settings(c: sqlite3.Connection) -> None:
    rows = [
        ("shields_per_week", "1"), ("inactivity_threshold", "5"),
        ("max_today_intentions", "3"), ("chest_drop_rate", "0.4"),
        ("pity_timer_days", "3"), ("fade_out_days", "14"),
        ("morning_ritual_hour", "8"), ("grace_period_hours", "2"),
        ("sound_volume", "1.0"), ("haptic_intensity", "1.0"),
        ("compassion_pact_accepted", "0"), ("user_archetype", ""),
        ("onboarding_complete", "0"), ("last_chest_date", ""),
        ("endowed_progress_checkins", "2"),
    ]
    c.executemany("INSERT OR IGNORE INTO settings VALUES (?, ?)", rows)


# --- GAMIFICATION PARAMS ---
def _seed_gamification(c: sqlite3.Connection) -> None:
    rows = [
        ("pity_timer_days", "3"),
        ("streak_milestone_days", "[7,14,21,30,60,100]"),
    ]
    c.executemany("INSERT OR IGNORE INTO gamification_params VALUES (?, ?)", rows)


# --- DESIGN TOKENS ---
def _seed_tokens(c: sqlite3.Connection) -> None:
    rows = [
        ("radius_small", "10"), ("radius_standard", "16"),
        ("radius_large", "24"), ("shadow_blur", "8"),
        ("shadow_offset", "4"), ("shadow_dark_opacity", "0.4"),
        ("shadow_light_opacity", "0.8"), ("color_base", "E8EDEA"),
        ("color_shadow_dark", "B8BDB9"), ("color_shadow_light", "FFFFFF"),
        ("color_primary", "2E4A3E"), ("color_secondary", "7FAF8C"),
        ("color_text_main", "1A2E25"), ("color_text_sub", "4A6358"),
        ("color_accent_alert", "C17A3A"),
    ]
    c.executemany("INSERT OR IGNORE INTO design_tokens VALUES (?, ?)", rows)


# --- BADGES ---
def _seed_badges(c: sqlite3.Connection) -> None:
    cols = "key, name, description, condition_type, condition_value, emoji_placeholder"
    q = f"INSERT OR IGNORE INTO badges ({cols}) VALUES (?,?,?,?,?,?)"
    c.executemany(q, [
        ("primer_brote", "Primer Brote", "Completa tu primera actividad", "total_completions", "1", "🌱"),
        ("jardinero", "Jardinero", "Completa 10 actividades", "total_completions", "10", "🧑‍🌾"),
        ("racha_7", "Racha de 7", "Mantén una racha de 7 días", "streak", "7", "🔥"),
        ("racha_21", "Racha de 21", "Mantén una racha de 21 días", "streak", "21", "💪"),
        ("racha_30", "Racha de 30", "Mantén una racha de 30 días", "streak", "30", "🏆"),
        ("racha_60", "Racha de 60", "Mantén una racha de 60 días", "streak", "60", "🌟"),
        ("racha_100", "Racha de 100", "Mantén una racha de 100 días", "streak", "100", "👑"),
        ("resiliente", "Resiliente", "Usa un escudo para proteger tu racha", "shield_used", "1", "🛡️"),
        ("mañanas", "Madrugador", "Completa 7 actividades antes de las 9AM", "morning_completions", "7", "☀️"),
        ("constancia", "Constancia", "Mantén 80%+ semanal por 4 semanas", "weekly_consistency", "4", "⚡"),
    ])


# --- UI COPY ---
def _seed_ui_copy(c: sqlite3.Connection) -> None:
    q = "INSERT OR IGNORE INTO ui_copy (key, value, context) VALUES (?,?,?)"
    c.executemany(q, [
        ("onboarding_question_1", "¿Qué tipo de cultivador eres?", "onboarding"),
        ("archetype_1", "🌱 El Sembrador — Empiezo muchas cosas", "onboarding"),
        ("archetype_2", "🌿 El Jardinero — Cuido lo que ya tengo", "onboarding"),
        ("archetype_3", "🌳 El Podador — Necesito simplificar", "onboarding"),
        ("confirm_habit", "Plantar mi primera semilla", "onboarding"),
        ("confirm_pact", "Acepto el pacto", "onboarding"),
        ("first_seed_title", "Tu primera semilla", "onboarding"),
        ("first_seed_hint", "Escribe un hábito que quieras cultivar", "onboarding"),
        ("pact_title", "Pacto de autocompasión", "onboarding"),
        ("pact_text", "Me comprometo a ser amable conmigo cuando falle. Cada día es una nueva semilla.", "onboarding"),
        ("fresh_start_monday", "¡Nuevo lunes, nueva tierra fértil!", "home"),
        ("fresh_start_month", "¡Nuevo mes! Tu jardín se renueva.", "home"),
        ("home_title", "Tu jardín", "home"),
        ("today_title", "Hoy cultivo", "home"),
        ("habits_title", "Mis hábitos", "home"),
        ("deadlines_title", "Horizontes", "home"),
        ("backlog_title", "Semillas en espera", "home"),
        ("ritual_button", "Elegir semillas de hoy", "home"),
        ("empty_today", "Elige hasta 3 semillas para hoy", "home"),
        ("chest_opened_prefix", "¡Has encontrado un cofre!", "gamification"),
        ("chest_title", "¡Cofre encontrado!", "gamification"),
        ("chest_open_label", "Abrir", "gamification"),
        ("chest_reward_1", "¡Una recompensa especial! 🌱", "gamification"),
        ("chest_reward_2", "Tu jardín se fortalece 🌿", "gamification"),
        ("chest_reward_3", "¡Sigue cultivando tus metas! 🌻", "gamification"),
        ("badge_celebration", "¡Nueva insignia desbloqueada!", "gamification"),
        ("create_title", "Plantar nueva semilla", "create"),
        ("confirm_a", "Plantar hábito", "create"),
        ("confirm_b", "Establecer meta", "create"),
        ("confirm_c", "Guardar semilla", "create"),
        ("confirm_d", "Cultivar hoy", "create"),
        ("intention_hint", "Si [situación], entonces [haré]...", "create"),
        ("coping_hint", "Si me resulta difícil, puedo...", "create"),
        ("horizon_prefix", "Horizonte en", "home"),
        ("new_activity_title", "Plantar nueva semilla", "create"),
        ("activity_name_hint", "Nombre de tu semilla...", "create"),
        ("implementation_hint", "Intención de implementación...", "create"),
    ])


# --- NOTIFICATION COPY ---
def _seed_notif_copy(c: sqlite3.Connection) -> None:
    q = "INSERT OR IGNORE INTO notification_copy (key, value, moment, activity_type) VALUES (?,?,?,?)"
    c.executemany(q, [
        ("morning_ritual", "Buenos días, cultivador. Tu jardín te espera.", "morning", None),
        ("deadline_2_days", "Tu meta está a 2 días del horizonte.", "deadline", "B"),
        ("deadline_today", "Hoy es el día: tu meta alcanza su horizonte.", "deadline", "B"),
        ("streak_milestone", "¡Días seguidos! Tu planta ha crecido.", "milestone", None),
        ("streak_broken", "Tu racha se reinició. Cada día es nueva semilla.", "reset", None),
        ("shield_used", "Tu escudo protegió la racha. Sigue cultivando.", "shield", None),
        ("fade_out", "Llevas tiempo sin visitar tu jardín. Todo sigue aquí.", "fade", None),
        ("notification_morning_title", "Semilla", "morning", None),
        ("notification_evening_title", "¡Bien hecho!", "evening", None),
        ("notification_streak_reminder", "Tu jardín te espera 🌱", "reminder", None),
        ("notification_completion", "Tu jardín crece 🌱", "feedback", None),
    ])


# --- ENTRY POINT ---
def seed_all(conn: sqlite3.Connection) -> None:
    _seed_settings(conn)
    _seed_gamification(conn)
    _seed_tokens(conn)
    _seed_badges(conn)
    _seed_ui_copy(conn)
    _seed_notif_copy(conn)
