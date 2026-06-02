import streamlit as st
from datetime import date, datetime
import anthropic

st.set_page_config(page_title="My 6-Month System", page_icon="🎯", layout="wide")

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
.main, section[data-testid="stSidebar"] > div { background: #fafaf8 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { background: #fff !important; border-right: 1px solid #efefef; }

/* hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Top nav bar */
.topnav {
    background: #fff;
    border-bottom: 1px solid #efefef;
    padding: 14px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky; top: 0; z-index: 100;
    margin-bottom: 0;
}
.topnav-title { font-size: 17px; font-weight: 700; color: #1a1a1a; letter-spacing: -0.3px; }
.topnav-sub { font-size: 11px; color: #aaa; margin-top: 2px; }

/* Urgency banner */
.urgency {
    background: #FCEBEB;
    border: 1.5px solid #E24B4A;
    border-radius: 12px;
    padding: 13px 18px;
    margin-bottom: 18px;
    display: flex; align-items: center; gap: 12px;
}
.urgency-title { font-size: 13px; font-weight: 700; color: #A32D2D; }
.urgency-sub { font-size: 12px; color: #c05050; margin-top: 2px; }

/* Stat boxes */
.stats-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin-bottom: 18px; }
.stat-box {
    background: #fff; border: 1px solid #efefef;
    border-radius: 12px; padding: 14px 12px; text-align: center;
}
.stat-val { font-size: 24px; font-weight: 700; }
.stat-lab { font-size: 11px; color: #999; margin-top: 3px; }

/* Goal card */
.goal-card {
    background: #fff;
    border-radius: 16px;
    margin-bottom: 12px;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.goal-header {
    padding: 16px 20px;
    display: flex; align-items: center; gap: 14px;
    cursor: pointer;
}
.goal-icon {
    width: 44px; height: 44px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; flex-shrink: 0;
}
.goal-phase {
    font-size: 11px; font-weight: 600; padding: 2px 9px;
    border-radius: 20px; letter-spacing: 0.3px;
}
.goal-title { font-weight: 600; font-size: 15px; color: #1a1a1a; }
.progress-track {
    height: 5px; background: #f0f0f0; border-radius: 99px;
    overflow: hidden; flex: 1; margin-right: 10px;
}
.progress-fill { height: 100%; border-radius: 99px; transition: width 0.4s; }
.goal-meta { font-size: 12px; color: #888; white-space: nowrap; }

/* Tabs */
.tab-row { display: flex; gap: 7px; padding: 12px 0 10px; }
.tab-btn {
    padding: 5px 15px; border-radius: 20px; border: none;
    font-size: 12px; font-weight: 500; cursor: pointer; transition: all 0.15s;
}
.tab-btn.active { color: #fff; }
.tab-btn.inactive { background: #f5f5f5; color: #666; }

/* Task row */
.task-row {
    display: flex; align-items: center; gap: 10px;
    padding: 9px 0; border-bottom: 1px solid #f8f8f8; cursor: pointer;
}
.task-box {
    width: 18px; height: 18px; border-radius: 5px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; color: #fff; transition: all 0.15s;
}
.task-text { font-size: 13px; }
.task-done { color: #bbb; text-decoration: line-through; }
.task-todo { color: #333; }

/* Habit grid */
.habit-grid { display: grid; gap: 5px 7px; align-items: center; }
.habit-cell {
    width: 26px; height: 26px; border-radius: 6px;
    cursor: pointer; transition: all 0.15s; border: 1.5px solid #e8e8e8;
}
.habit-cell.done { border: none; }

/* Milestone row */
.milestone-row {
    display: flex; align-items: center; gap: 12px;
    padding: 9px 0; border-bottom: 1px solid #f5f5f5;
}
.ms-circle {
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 700; flex-shrink: 0;
}

/* Info box */
.info-box { border-radius: 10px; padding: 10px 14px; font-size: 12px; margin-top: 10px; }

/* Note item */
.note-item { background: #fafafa; border-radius: 8px; padding: 9px 13px; margin-bottom: 7px; }
.note-text { font-size: 13px; color: #333; }
.note-date { font-size: 11px; color: #bbb; margin-top: 3px; }

/* Phase */
.phase-desc { border-radius: 10px; padding: 11px 15px; font-size: 13px; color: #444; line-height: 1.6; }
.phase-goal-chip {
    background: #fff; border: 1px solid #efefef; border-radius: 8px;
    padding: 6px 11px; font-size: 12px; color: #555;
    display: flex; align-items: center; gap: 6px;
}

/* Schedule cell */
.sched-cell {
    border-radius: 8px; padding: 6px 4px;
    font-size: 10px; font-weight: 500; text-align: center;
    color: #444; min-height: 36px;
    display: flex; align-items: center; justify-content: center;
    line-height: 1.3;
}

/* Chat */
.chat-wrap { display: flex; flex-direction: column; gap: 10px; padding: 10px 0; }
.chat-user {
    background: #534AB7; color: #fff;
    border-radius: 14px 14px 4px 14px;
    padding: 10px 14px; margin-left: 15%;
    font-size: 13px; line-height: 1.6; white-space: pre-wrap;
}
.chat-ai {
    background: #f5f5f5; color: #222;
    border-radius: 14px 14px 14px 4px;
    padding: 10px 14px; margin-right: 15%;
    font-size: 13px; line-height: 1.6; white-space: pre-wrap;
}

/* Sidebar nav */
.sidenav-item {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px; border-radius: 10px;
    cursor: pointer; font-size: 14px; font-weight: 500;
    margin-bottom: 4px; transition: background 0.15s;
}
.sidenav-item.active { background: #534AB7; color: #fff; }
.sidenav-item.inactive { color: #555; }
.sidenav-item.inactive:hover { background: #f5f5f5; }

/* Sidebar goal mini */
.sidebar-goal { margin-bottom: 12px; }
.sidebar-goal-title { font-size: 12px; font-weight: 600; color: #333; margin-bottom: 4px; }
.sidebar-track { height: 4px; background: #f0f0f0; border-radius: 99px; overflow: hidden; margin-bottom: 2px; }
.sidebar-fill { height: 100%; border-radius: 99px; }
.sidebar-meta { font-size: 10px; color: #aaa; }

/* stButton tweaks */
div[data-testid="stVerticalBlock"] button { font-family: 'Inter', sans-serif !important; }

/* content wrapper */
.content-wrap { max-width: 780px; margin: 0 auto; padding: 22px 20px; }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
GOALS = [
    {
        "id": "coursework", "title": "Coursework Reassessment",
        "icon": "📚", "color": "#E24B4A", "bg": "#FCEBEB",
        "deadline": date(2025, 6, 8), "phase": "URGENT",
        "target": "Complete 2 courseworks", "daily_time": "3h  (6–9 PM)",
        "tasks": [
            "Coursework 1 — outline & draft", "Coursework 1 — write & revise",
            "Coursework 1 — submit", "Coursework 2 — outline & draft",
            "Coursework 2 — write & revise", "Coursework 2 — submit",
        ],
        "habits": ["Study session (6–9 PM)", "Review notes (morning)"],
        "milestones": ["CW1 draft done", "CW1 submitted", "CW2 draft done", "CW2 submitted ✓"],
    },
    {
        "id": "fitness", "title": "Lose 5 kg in 3 Months",
        "icon": "💪", "color": "#1D9E75", "bg": "#E1F5EE",
        "deadline": date(2025, 8, 29), "phase": "Month 1–3",
        "target": "−5 kg by end of August", "daily_time": "30 min  (5:30–6 AM)",
        "tasks": [
            "Set up meal tracking app", "Plan weekly workout schedule",
            "First weigh-in (baseline)", "Reach −2 kg milestone",
            "Reach −3.5 kg milestone", "Reach −5 kg goal! 🎉",
        ],
        "habits": ["Morning workout (30 min)", "Track meals / calories", "8 glasses of water"],
        "milestones": ["Workout routine set", "−1 kg", "−2.5 kg", "−5 kg ✓"],
    },
    {
        "id": "youtube", "title": "Solar Tech YouTube + Social",
        "icon": "☀️", "color": "#BA7517", "bg": "#FAEEDA",
        "deadline": date(2025, 11, 29), "phase": "Month 2–6",
        "target": "Regular income from content", "daily_time": "1–2h evenings + Sunday batch",
        "tasks": [
            "Set up YouTube channel", "Create Facebook & TikTok pages",
            "Film first YouTube video", "Post first TikTok/Facebook reel",
            "Reach 100 YouTube subscribers", "First monetisation milestone",
        ],
        "habits": ["Post short-form content (TikTok/FB)", "Sunday batch-create content", "Engage with community"],
        "milestones": ["Channel live", "10 videos posted", "100 subscribers", "First $50 earned"],
    },
    {
        "id": "trading", "title": "Stock & Options Trading",
        "icon": "📈", "color": "#534AB7", "bg": "#EEEDFE",
        "deadline": date(2025, 11, 29), "phase": "Month 1–6",
        "target": "$100–150/day profit", "daily_time": "30 min study  (7–7:30 PM)",
        "tasks": [
            "Choose a trading platform / broker", "Complete beginner options course",
            "Start paper trading (simulated)", "Track 30 paper trades",
            "First real trade (small amount)", "Consistent $50/day paper profit",
        ],
        "habits": ["30 min trading study", "Review market pre-open", "Log trade in journal"],
        "milestones": ["Paper trading started", "30 trades logged", "Profitable week (paper)", "$50/day consistent"],
    },
]

PHASES = [
    {"label": "Now → 8 Jun", "color": "#FCEBEB", "text": "#A32D2D",
     "desc": "🚨 EMERGENCY: Coursework only. Exercise daily for energy."},
    {"label": "Jun → Jul", "color": "#E6F1FB", "text": "#185FA5",
     "desc": "🚀 LAUNCH: Start YouTube channel, begin paper trading, lock in daily habits."},
    {"label": "Jul → Aug", "color": "#EAF3DE", "text": "#3B6D11",
     "desc": "⚡ ACCELERATE: Hit weight goal, 8+ YT videos, first small real trades."},
    {"label": "Sep → Nov", "color": "#FAEEDA", "text": "#854F0B",
     "desc": "📈 SCALE: Social media income building, trading consistency growing."},
]

DAYS_LABELS = ["M", "T", "W", "T", "F", "S", "S"]
DAYS_FULL   = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

SCHEDULE = [
    ("5:30–6 AM",   ["🏃 Exercise"]*5 + ["😴 Rest",        "😴 Rest"],        ["#EAF3DE"]*5+["#f5f5f5"]*2),
    ("9 AM–5 PM",   ["💼 Day Job"]*5  + ["🎬 YT Filming",  "📦 Batch"],        ["#e8e8e8"]*5+["#FAEEDA"]*2),
    ("5–6 PM",      ["😮 Wind Down"]*5+ ["📊 Trading",     "🆓 Free"],         ["#fafafa"]*5+["#EEEDFE","#fafafa"]),
    ("6–7 PM",      ["✍️ YT/Study"]*5 + ["📲 Post+Sched",  "📋 Week Review"],  ["#E6F1FB"]*5+["#FAEEDA","#E6F1FB"]),
    ("7–7:30 PM",   ["📈 Trading"]*5  + ["🔍 Trade Rev",   "—"],               ["#EEEDFE"]*5+["#EEEDFE","#fafafa"]),
    ("7:30–9 PM",   ["🛋️ Relax"]*7,                                            ["#fafafa"]*7),
]

SYSTEM_PROMPT = """You are a personal goal coach for someone with these 4 active goals:
1. COURSEWORK REASSESSMENT (URGENT) - 2 courseworks due 8 June. Works 9-5 PM as a Senior Project Manager in Singapore.
2. LOSE 5 KG IN 3 MONTHS - by end of August. Morning 30-min workouts 5:30-6 AM.
3. SOLAR TECH YOUTUBE + SOCIAL MEDIA (TikTok, Facebook) - starts after June 8. Sunday batch content creation. 1-2h evenings.
4. STOCK & OPTIONS TRADING - paper trade first 2 months, target $100-150/day by month 5-6. 30 min daily 7-7:30 PM.
Free time: 6-9 PM weekdays + weekends.
Be concise, practical, encouraging. Give specific actionable advice. Use emojis very sparingly."""

# ── Session state ─────────────────────────────────────────────────────────────
def init():
    for g in GOALS:
        gid = g["id"]
        st.session_state.setdefault(f"tasks_{gid}",  [False]*len(g["tasks"]))
        st.session_state.setdefault(f"habits_{gid}", [[False]*7 for _ in g["habits"]])
        st.session_state.setdefault(f"notes_{gid}",  [])
        st.session_state.setdefault(f"tab_{gid}",    "tasks")
        st.session_state.setdefault(f"open_{gid}",   False)
    st.session_state.setdefault("page", "dashboard")
    st.session_state.setdefault("chat", [
        {"role":"assistant","content":"Hi! I'm your AI goal coach 🎯  Ask me anything about your 4 goals, time management, or what to focus on today."}
    ])
    st.session_state.setdefault("chat_input", "")
init()

def days_until(d): return max((d - date.today()).days, 0)
def pct(gid, tasks):
    done = sum(st.session_state[f"tasks_{gid}"])
    return done, len(tasks), round(done/len(tasks)*100)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:18px 14px 10px">
      <div style="font-size:16px;font-weight:700;color:#1a1a1a">🎯 My 6-Month System</div>
      <div style="font-size:11px;color:#aaa;margin-top:3px">{} days remaining</div>
    </div>
    """.format(days_until(date(2025,11,29))), unsafe_allow_html=True)

    st.markdown("<div style='padding:0 8px'>", unsafe_allow_html=True)
    pages = [("📊","Dashboard","dashboard"),("🗓️","Schedule","weekly"),
             ("🗺️","Phase Plan","phases"),("🤖","AI Coach","coach")]
    for icon, label, key in pages:
        active = st.session_state.page == key
        bg  = "#534AB7" if active else "transparent"
        col = "#fff"    if active else "#555"
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid #efefef;margin:14px 0'>", unsafe_allow_html=True)
    st.markdown("<div style='padding:0 14px;font-size:12px;font-weight:600;color:#999;margin-bottom:10px'>PROGRESS</div>", unsafe_allow_html=True)
    for g in GOALS:
        done, total, p = pct(g["id"], g["tasks"])
        st.markdown(f"""
        <div style="padding:0 14px;margin-bottom:14px">
          <div style="font-size:12px;font-weight:600;color:#333;margin-bottom:5px">{g['icon']} {g['title']}</div>
          <div style="height:4px;background:#f0f0f0;border-radius:99px;overflow:hidden;margin-bottom:3px">
            <div style="width:{p}%;height:100%;background:{g['color']};border-radius:99px"></div>
          </div>
          <div style="font-size:10px;color:#aaa">{done}/{total} tasks · {days_until(g['deadline'])}d left</div>
        </div>
        """, unsafe_allow_html=True)

# ── Top nav ───────────────────────────────────────────────────────────────────
page_names = {"dashboard":"Goal Dashboard","weekly":"Weekly Schedule","phases":"Phase Plan","coach":"AI Coach"}
st.markdown(f"""
<div class="topnav">
  <div>
    <div class="topnav-title">My 6-Month System</div>
    <div class="topnav-sub">{days_until(date(2025,11,29))} days remaining overall</div>
  </div>
  <div style="font-size:15px;font-weight:600;color:#534AB7">{page_names[st.session_state.page]}</div>
</div>
""", unsafe_allow_html=True)

# ── DASHBOARD ─────────────────────────────────────────────────────────────────
if st.session_state.page == "dashboard":
    st.markdown('<div class="content-wrap">', unsafe_allow_html=True)

    days_cw = days_until(date(2025,6,8))
    st.markdown(f"""
    <div class="urgency">
      <span style="font-size:22px">⚠️</span>
      <div>
        <div class="urgency-title">URGENT: {days_cw} days until coursework deadline (8 June)</div>
        <div class="urgency-sub">All 6–9 PM slots + weekends = coursework only until deadline.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-box"><div class="stat-val" style="color:#534AB7">4</div><div class="stat-lab">Active Goals</div></div>
      <div class="stat-box"><div class="stat-val" style="color:#E24B4A">{days_cw}</div><div class="stat-lab">Days to CW</div></div>
      <div class="stat-box"><div class="stat-val" style="color:#1D9E75">3h</div><div class="stat-lab">Daily Focus</div></div>
      <div class="stat-box"><div class="stat-val" style="color:#BA7517">6mo</div><div class="stat-lab">Total Runway</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Goal cards
    for g in GOALS:
        gid   = g["id"]
        done, total, p = pct(gid, g["tasks"])
        is_open = st.session_state[f"open_{gid}"]
        border  = g["color"] if is_open else "#e8e8e8"
        shadow  = f"0 4px 24px {g['color']}22" if is_open else "0 1px 4px rgba(0,0,0,0.05)"

        st.markdown(f"""
        <div class="goal-card" style="border:1.5px solid {border};box-shadow:{shadow}">
          <div class="goal-header">
            <div class="goal-icon" style="background:{g['bg']}">{g['icon']}</div>
            <div style="flex:1;min-width:0">
              <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">
                <span class="goal-title">{g['title']}</span>
                <span class="goal-phase" style="background:{g['bg']};color:{g['color']}">{g['phase']}</span>
              </div>
              <div style="margin-top:7px;display:flex;align-items:center;gap:10px">
                <div class="progress-track"><div class="progress-fill" style="width:{p}%;background:{g['color']}"></div></div>
                <span class="goal-meta">{done}/{total} tasks · {days_until(g['deadline'])}d left</span>
              </div>
            </div>
            <span style="font-size:18px;color:#aaa;transform:{'rotate(180deg)' if is_open else 'none'};transition:transform 0.2s">⌄</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Toggle open button (invisible but clickable)
        toggle_col, _ = st.columns([1, 5])
        with toggle_col:
            btn_label = "▲ Collapse" if is_open else "▼ Expand"
            if st.button(btn_label, key=f"toggle_{gid}", use_container_width=True):
                st.session_state[f"open_{gid}"] = not is_open
                st.rerun()

        if is_open:
            with st.container():
                st.markdown(f"""<div style="background:#fff;border:1.5px solid {g['color']};border-top:none;
                    border-radius:0 0 16px 16px;padding:4px 20px 20px;margin-top:-12px;
                    box-shadow:{shadow}">""", unsafe_allow_html=True)

                # Sub tabs
                tab_names = ["✅ Tasks", "🔄 Habits", "🏆 Milestones", "📝 Notes"]
                tabs = st.tabs(tab_names)

                # ── TASKS ──
                with tabs[0]:
                    st.caption(f"Daily time: **{g['daily_time']}**")
                    task_states = st.session_state[f"tasks_{gid}"]
                    changed = False
                    for i, task in enumerate(g["tasks"]):
                        col_cb, col_lbl = st.columns([0.05, 0.95])
                        with col_cb:
                            val = st.checkbox("", value=task_states[i], key=f"ck_{gid}_{i}", label_visibility="collapsed")
                            if val != task_states[i]:
                                st.session_state[f"tasks_{gid}"][i] = val
                                changed = True
                        with col_lbl:
                            style = "text-decoration:line-through;color:#bbb" if task_states[i] else "color:#333"
                            st.markdown(f"<span style='font-size:13px;{style}'>{task}</span>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="info-box" style="background:{g['bg']}">
                      <span style="color:{g['color']};font-weight:600;font-size:12px">🎯 Target: </span>
                      <span style="font-size:12px;color:#555">{g['target']}</span>
                    </div>""", unsafe_allow_html=True)

                # ── HABITS ──
                with tabs[1]:
                    st.caption("Tap each day you completed the habit this week:")
                    habit_states = st.session_state[f"habits_{gid}"]
                    # Header row
                    cols = st.columns([4]+[1]*7)
                    cols[0].markdown("<span style='font-size:11px;color:#aaa'>Habit</span>", unsafe_allow_html=True)
                    for di, d in enumerate(DAYS_LABELS):
                        cols[di+1].markdown(f"<div style='text-align:center;font-size:11px;color:#aaa'>{d}</div>", unsafe_allow_html=True)

                    for hi, habit in enumerate(g["habits"]):
                        cols = st.columns([4]+[1]*7)
                        cols[0].markdown(f"<span style='font-size:12px;color:#444'>{habit}</span>", unsafe_allow_html=True)
                        for di in range(7):
                            with cols[di+1]:
                                checked = habit_states[hi][di]
                                bg = g["color"] if checked else "#f5f5f5"
                                border = "none" if checked else "1.5px solid #e8e8e8"
                                # Use checkbox but style it
                                new_val = st.checkbox("", value=checked, key=f"h_{gid}_{hi}_{di}", label_visibility="collapsed")
                                if new_val != checked:
                                    st.session_state[f"habits_{gid}"][hi][di] = new_val
                                    st.rerun()
                        days_done = sum(habit_states[hi])
                        st.caption(f"✅ {days_done}/7 days this week")

                # ── MILESTONES ──
                with tabs[2]:
                    milestone_threshold = p // 25
                    for i, m in enumerate(g["milestones"]):
                        unlocked = i < milestone_threshold
                        circle_bg  = g["color"] if unlocked else "#f0f0f0"
                        circle_col = "#fff" if unlocked else "#ccc"
                        text_col   = "#333" if unlocked else "#aaa"
                        done_badge = f'<span style="margin-left:auto;font-size:12px;color:{g["color"]};font-weight:600">✓ Done</span>' if unlocked else ""
                        st.markdown(f"""
                        <div class="milestone-row" style="{'border-bottom:none' if i==len(g['milestones'])-1 else ''}">
                          <div class="ms-circle" style="background:{circle_bg};color:{circle_col}">{i+1}</div>
                          <span style="font-size:13px;color:{text_col};flex:1">{m}</span>
                          {done_badge}
                        </div>""", unsafe_allow_html=True)

                # ── NOTES ──
                with tabs[3]:
                    notes = st.session_state[f"notes_{gid}"]
                    nc1, nc2 = st.columns([5,1])
                    with nc1:
                        new_note = st.text_input("", placeholder="Add a note or reflection...",
                                                  key=f"noteinput_{gid}", label_visibility="collapsed")
                    with nc2:
                        if st.button("Add", key=f"notebtn_{gid}", use_container_width=True) and new_note.strip():
                            notes.insert(0, {"text": new_note, "date": datetime.now().strftime("%d %b %Y, %H:%M")})
                            st.session_state[f"notes_{gid}"] = notes
                            st.rerun()
                    if not notes:
                        st.caption("No notes yet. Log wins, blockers, ideas here.")
                    for n in notes:
                        st.markdown(f"""
                        <div class="note-item">
                          <div class="note-text">{n['text']}</div>
                          <div class="note-date">{n['date']}</div>
                        </div>""", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── SCHEDULE ──────────────────────────────────────────────────────────────────
elif st.session_state.page == "weekly":
    st.markdown('<div class="content-wrap">', unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px;color:#999;margin-bottom:16px'>Post-June 8 routine. Until then, 6–9 PM = coursework only.</p>", unsafe_allow_html=True)

    # Day headers
    header_cols = st.columns([1.4]+[1]*7)
    header_cols[0].markdown("")
    for i, d in enumerate(DAYS_FULL):
        header_cols[i+1].markdown(f"<div style='text-align:center;font-size:11px;font-weight:600;color:#888;padding-bottom:4px'>{d}</div>", unsafe_allow_html=True)

    for time_label, slots, colors in SCHEDULE:
        row_cols = st.columns([1.4]+[1]*7)
        row_cols[0].markdown(f"<div style='font-size:11px;color:#999;padding-top:8px;line-height:1.3'>{time_label}</div>", unsafe_allow_html=True)
        for i in range(7):
            row_cols[i+1].markdown(f"""
            <div class="sched-cell" style="background:{colors[i]}">{slots[i]}</div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid #efefef;margin:18px 0'>", unsafe_allow_html=True)

    # Legend
    legends = [("🏃 Exercise","#EAF3DE"),("💼 Day Job","#e8e8e8"),("✍️ Study/Script","#E6F1FB"),
               ("☀️ YouTube","#FAEEDA"),("📈 Trading","#EEEDFE"),("🛋️ Rest","#fafafa")]
    leg_cols = st.columns(6)
    for col, (lab, col_hex) in zip(leg_cols, legends):
        col.markdown(f"""
        <div style="display:flex;align-items:center;gap:6px;font-size:11px;color:#555">
          <div style="width:13px;height:13px;border-radius:3px;background:{col_hex};border:1px solid #ddd;flex-shrink:0"></div>{lab}
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Until June 8:** Replace 6–9 PM with coursework only. YouTube can wait 9 days.")
    st.markdown('</div>', unsafe_allow_html=True)

# ── PHASES ────────────────────────────────────────────────────────────────────
elif st.session_state.page == "phases":
    st.markdown('<div class="content-wrap">', unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px;color:#999;margin-bottom:22px'>Phase in your goals — don't go full intensity on all 4 at once.</p>", unsafe_allow_html=True)

    for i, p in enumerate(PHASES):
        left, right = st.columns([0.08, 0.92])
        with left:
            st.markdown(f"""
            <div style="width:38px;height:38px;border-radius:50%;background:{p['color']};
                border:2px solid {p['text']};display:flex;align-items:center;justify-content:center;
                font-weight:700;font-size:15px;color:{p['text']};margin-top:4px">{i+1}</div>
            """, unsafe_allow_html=True)
            if i < len(PHASES)-1:
                st.markdown("<div style='width:2px;height:44px;background:#f0f0f0;margin:4px auto 0;'></div>", unsafe_allow_html=True)

        with right:
            st.markdown(f"<div style='font-weight:700;font-size:14px;color:{p['text']};margin-bottom:5px'>{p['label']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='phase-desc' style='background:{p['color']}'>{p['desc']}</div>", unsafe_allow_html=True)
            active_goals = GOALS if i > 0 else [GOALS[0], GOALS[1]]
            gcols = st.columns(len(active_goals))
            for gc, g in zip(gcols, active_goals):
                faded = (i == 0 and g["id"] == "youtube")
                gc.markdown(f"""
                <div class="phase-goal-chip" style="opacity:{'0.35' if faded else '1'}">
                  {g['icon']} {' '.join(g['title'].split()[:3])}
                  {'<span style="margin-left:auto;font-size:10px;color:#ccc">wait</span>' if faded else ''}
                </div>""", unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── AI COACH ──────────────────────────────────────────────────────────────────
elif st.session_state.page == "coach":
    st.markdown('<div class="content-wrap">', unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;padding:16px 20px;
        background:#fff;border:1px solid #efefef;border-radius:16px 16px 0 0;
        border-bottom:1px solid #f0f0f0;margin-bottom:0">
      <div style="width:40px;height:40px;border-radius:50%;background:#EEEDFE;
          display:flex;align-items:center;justify-content:center;font-size:20px">🤖</div>
      <div>
        <div style="font-weight:700;font-size:14px;color:#1a1a1a">AI Goal Coach</div>
        <div style="font-size:11px;color:#1D9E75;margin-top:1px">● Online · Powered by Claude</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick prompts
    st.markdown("<div style='padding:10px 0 6px'>", unsafe_allow_html=True)
    qcols = st.columns(4)
    quick = ["What should I do today?","How to start trading?","YouTube content ideas?","I'm overwhelmed"]
    for qc, q in zip(qcols, quick):
        if qc.button(q, use_container_width=True, key=f"q_{q[:10]}"):
            st.session_state.chat.append({"role":"user","content":q})
            with st.spinner("Thinking…"):
                try:
                    client = anthropic.Anthropic()
                    api_msgs = [m for m in st.session_state.chat
                                if not (m["role"]=="assistant" and "Hi! I'm your AI" in m["content"])]
                    resp = client.messages.create(
                        model="claude-sonnet-4-20250514", max_tokens=600,
                        system=SYSTEM_PROMPT, messages=api_msgs or [{"role":"user","content":q}]
                    )
                    st.session_state.chat.append({"role":"assistant","content":resp.content[0].text})
                except Exception as e:
                    st.session_state.chat.append({"role":"assistant","content":f"Connection error: {str(e)[:80]}"})
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Chat history
    chat_html = '<div style="background:#fff;border:1px solid #efefef;border-top:none;border-radius:0 0 16px 16px;padding:16px 20px;min-height:360px;max-height:420px;overflow-y:auto">'
    for msg in st.session_state.chat:
        if msg["role"] == "user":
            chat_html += f'<div class="chat-user">{msg["content"]}</div>'
        else:
            chat_html += f'<div class="chat-ai">{msg["content"]}</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # Input
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    ic1, ic2 = st.columns([6,1])
    with ic1:
        user_input = st.text_input("", placeholder="Ask your coach anything…",
                                    key="coach_input", label_visibility="collapsed")
    with ic2:
        send_btn = st.button("Send ↑", use_container_width=True, key="coach_send")

    if send_btn and user_input.strip():
        st.session_state.chat.append({"role":"user","content":user_input.strip()})
        with st.spinner("Thinking…"):
            try:
                client = anthropic.Anthropic()
                api_msgs = [m for m in st.session_state.chat
                            if not (m["role"]=="assistant" and "Hi! I'm your AI" in m["content"])]
                resp = client.messages.create(
                    model="claude-sonnet-4-20250514", max_tokens=600,
                    system=SYSTEM_PROMPT, messages=api_msgs
                )
                st.session_state.chat.append({"role":"assistant","content":resp.content[0].text})
            except Exception as e:
                st.session_state.chat.append({"role":"assistant","content":f"Connection error: {str(e)[:80]}"})
        st.rerun()

    if st.button("🗑️ Clear chat", key="clear_chat"):
        st.session_state.chat = [{"role":"assistant","content":"Hi! I'm your AI goal coach 🎯  Ask me anything about your 4 goals, time management, or what to focus on today."}]
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
