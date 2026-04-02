import streamlit as st
import numpy as np
import pickle
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AQI Predictor | Industrial Pollution Monitor",
    page_icon="🏭",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&family=Orbitron:wght@700;900&display=swap');

/* ── Root / Background ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0a0c10 !important;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 40% at 50% 0%, rgba(255,100,0,0.08) 0%, transparent 60%),
        repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(255,100,0,0.03) 40px),
        repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(255,100,0,0.03) 40px),
        #0a0c10;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
footer { display: none; }

/* ── Global font ── */
* { font-family: 'Rajdhani', sans-serif !important; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.hero-icon {
    font-size: 3.5rem;
    display: block;
    margin-bottom: 0.4rem;
    filter: drop-shadow(0 0 18px rgba(255,120,0,0.7));
    animation: pulse-glow 2.5s ease-in-out infinite;
}
@keyframes pulse-glow {
    0%, 100% { filter: drop-shadow(0 0 14px rgba(255,120,0,0.6)); }
    50%       { filter: drop-shadow(0 0 28px rgba(255,160,0,0.9)); }
}
.hero-title {
    font-family: 'Orbitron', monospace !important;
    font-size: 2rem;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    line-height: 1.15;
}
.hero-title span { color: #ff6b00; }
.hero-sub {
    font-size: 1.05rem;
    color: #7a8496;
    letter-spacing: 0.12em;
    margin-top: 0.35rem;
    text-transform: uppercase;
    font-weight: 500;
}

/* ── Divider ── */
.divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #ff6b00 40%, #ff6b00 60%, transparent);
    opacity: 0.35;
    margin: 1.2rem 0 2rem;
}

/* ── Panel card ── */
.panel {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,107,0,0.2);
    border-radius: 8px;
    padding: 1.6rem 1.8rem 1.2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #ff6b00, transparent);
}
.panel-label {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.72rem;
    color: #ff6b00;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.1rem;
    opacity: 0.85;
}

/* ── Sliders & number inputs ── */
[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg, #ff6b00, #ffaa00) !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: #ff6b00 !important;
    box-shadow: 0 0 10px rgba(255,107,0,0.7) !important;
    border: 2px solid #ffaa00 !important;
}
[data-testid="stSlider"] label,
[data-testid="stNumberInput"] label {
    color: #c4cdd8 !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em;
}
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"] {
    color: #4a5568 !important;
    font-size: 0.75rem !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* ── Predict button ── */
[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #ff6b00, #e05000) !important;
    color: #ffffff !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.75rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(255,107,0,0.35) !important;
    margin-top: 0.6rem;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #ff8020, #ff6b00) !important;
    box-shadow: 0 6px 30px rgba(255,107,0,0.55) !important;
    transform: translateY(-1px) !important;
}

/* ── Result boxes ── */
.result-box {
    border-radius: 8px;
    padding: 1.6rem 1.4rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-top: 1.2rem;
}
.result-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
/* AQI box */
.aqi-box {
    background: rgba(255,107,0,0.07);
    border: 1px solid rgba(255,107,0,0.3);
}
.aqi-box::before { background: linear-gradient(90deg, #ff6b00, #ffaa00, #ff6b00); }
.aqi-label {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    color: #ff9040;
    text-transform: uppercase;
}
.aqi-value {
    font-family: 'Orbitron', monospace !important;
    font-size: 3.4rem;
    font-weight: 900;
    color: #ffffff;
    line-height: 1.1;
    text-shadow: 0 0 30px rgba(255,107,0,0.5);
}

/* Level badges */
.level-box { border: 1px solid; }
.level-LOW    { background: rgba(34,197,94,0.08);  border-color: rgba(34,197,94,0.35); }
.level-MEDIUM { background: rgba(251,191,36,0.08); border-color: rgba(251,191,36,0.35); }
.level-HIGH   { background: rgba(239,68,68,0.10);  border-color: rgba(239,68,68,0.40); }
.level-LOW::before    { background: linear-gradient(90deg, #16a34a, #4ade80, #16a34a); }
.level-MEDIUM::before { background: linear-gradient(90deg, #d97706, #fbbf24, #d97706); }
.level-HIGH::before   { background: linear-gradient(90deg, #dc2626, #f87171, #dc2626); }

.level-icon { font-size: 2.6rem; display: block; margin-bottom: 0.25rem; }
.level-label {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    opacity: 0.7;
}
.level-value {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.8rem;
    font-weight: 900;
    letter-spacing: 0.06em;
}
.level-LOW    .level-value { color: #4ade80; text-shadow: 0 0 20px rgba(74,222,128,0.4); }
.level-MEDIUM .level-value { color: #fbbf24; text-shadow: 0 0 20px rgba(251,191,36,0.4); }
.level-HIGH   .level-value { color: #f87171; text-shadow: 0 0 20px rgba(248,113,113,0.5); }

/* ── Info bar ── */
.info-bar {
    display: flex;
    gap: 0.8rem;
    justify-content: space-between;
    margin-top: 1.4rem;
}
.info-pill {
    flex: 1;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
    padding: 0.7rem 0.5rem;
    text-align: center;
}
.info-pill-label {
    font-size: 0.7rem;
    color: #4a5568;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-family: 'Share Tech Mono', monospace !important;
}
.info-pill-value {
    font-size: 1.05rem;
    font-weight: 700;
    color: #c4cdd8;
    margin-top: 0.15rem;
}

/* ── Model note ── */
.model-note {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.72rem;
    color: #3d4658;
    text-align: center;
    letter-spacing: 0.1em;
    padding-top: 1rem;
}

/* ── Error box ── */
.error-panel {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: #f87171;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "pollution_model.pkl")

@st.cache_resource
def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

try:
    model = load_model()
    model_loaded = True
except FileNotFoundError:
    model_loaded = False
except Exception as e:
    model_loaded = False
    model_error = str(e)

# ── Helper functions ──────────────────────────────────────────────────────────
def classify_aqi(aqi: float) -> tuple[str, str]:
    if aqi <= 150:
        return "LOW", "✅"
    elif aqi <= 300:
        return "MEDIUM", "⚠️"
    else:
        return "HIGH", "🔴"

def predict_aqi(production, temperature, humidity) -> float:
    features = np.array([[production, temperature, humidity]])
    return float(model.predict(features)[0])

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <span class="hero-icon">🏭</span>
  <div class="hero-title">Industrial <span>AQI</span> Predictor</div>
  <div class="hero-sub">Polynomial Regression · Environmental Monitor</div>
</div>
<hr class="divider"/>
""", unsafe_allow_html=True)

if not model_loaded:
    st.markdown(f"""
    <div class="error-panel">
        ⚠️ &nbsp;<strong>Model file not found.</strong><br>
        Place <code>pollution_model.pkl</code> inside the <code>model/</code> folder.<br>
        Expected path: <code>{MODEL_PATH}</code>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Input panel ──────────────────────────────────────────────────────────────
st.markdown('<div class="panel"><div class="panel-label">// Input Parameters</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    production = st.slider(
        "🏭 Production (tons/day)",
        min_value=0, max_value=1000, value=300, step=5,
        help="Daily factory output in tons"
    )
    temperature = st.slider(
        "🌡️ Temperature (°C)",
        min_value=-10, max_value=50, value=28, step=1,
        help="Ambient temperature in Celsius"
    )

with col2:
    humidity = st.slider(
        "💧 Humidity (%)",
        min_value=0, max_value=100, value=60, step=1,
        help="Relative humidity percentage"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ── Predict button ────────────────────────────────────────────────────────────
predict_clicked = st.button("⚡ ANALYZE POLLUTION LEVEL", use_container_width=True)

# ── Results ───────────────────────────────────────────────────────────────────
if predict_clicked:
    try:
        aqi = predict_aqi(production, temperature, humidity)
        aqi = max(0.0, aqi)          # clamp negatives
        level, icon = classify_aqi(aqi)

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown(f"""
            <div class="result-box aqi-box">
                <div class="aqi-label">Predicted AQI</div>
                <div class="aqi-value">{aqi:.1f}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_b:
            st.markdown(f"""
            <div class="result-box level-box level-{level}">
                <span class="level-icon">{icon}</span>
                <div class="level-label">Pollution Level</div>
                <div class="level-value">{level}</div>
            </div>
            """, unsafe_allow_html=True)

        # Info pills
        aqi_pct = min(int((aqi / 500) * 100), 100)
        st.markdown(f"""
        <div class="info-bar">
            <div class="info-pill">
                <div class="info-pill-label">Production</div>
                <div class="info-pill-value">{production} t/d</div>
            </div>
            <div class="info-pill">
                <div class="info-pill-label">Temperature</div>
                <div class="info-pill-value">{temperature}°C</div>
            </div>
            <div class="info-pill">
                <div class="info-pill-label">Humidity</div>
                <div class="info-pill-value">{humidity}%</div>
            </div>
            <div class="info-pill">
                <div class="info-pill-label">AQI Scale</div>
                <div class="info-pill-value">{aqi_pct}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Advisory message
        advisories = {
            "LOW":    ("🟢", "Air quality is acceptable. Minimal health risk for the general population."),
            "MEDIUM": ("🟡", "Moderate concern. Sensitive individuals should limit prolonged outdoor activity."),
            "HIGH":   ("🔴", "Unhealthy air quality. Immediate action required — reduce factory output."),
        }
        adv_icon, adv_text = advisories[level]
        st.info(f"{adv_icon}  **Advisory:** {adv_text}")

    except Exception as e:
        st.markdown(f'<div class="error-panel">Prediction failed: {e}</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="model-note">
    MODEL // Polynomial Regression · Degree-3 · Ridge Regularization &nbsp;|&nbsp;
    THRESHOLD // LOW ≤ 150 · MEDIUM ≤ 300 · HIGH > 300
</div>
""", unsafe_allow_html=True)
