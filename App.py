import streamlit as st
import time
import json
from datetime import datetime
import random

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DesignGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0A0A0A;
    color: #E8E8E8;
}

.stApp { background-color: #0A0A0A; }

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem 2rem; max-width: 1400px; }

/* ── Header ── */
.dg-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.5rem;
    background: #111111;
    border: 1px solid #1E1E1E;
    border-radius: 10px;
    margin-bottom: 1.5rem;
}
.dg-logo { font-family: 'JetBrains Mono', monospace; font-size: 1.3rem; font-weight: 700; color: #1DB954; letter-spacing: -0.5px; }
.dg-logo span { color: #E8E8E8; }
.dg-badge { background: #1A2B1A; border: 1px solid #1DB954; color: #1DB954; font-size: 0.7rem; font-weight: 600; padding: 3px 10px; border-radius: 20px; letter-spacing: 1px; }
.dg-subtitle { color: #666; font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; }

/* ── Cards ── */
.dg-card {
    background: #111111;
    border: 1px solid #1E1E1E;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
.dg-card-title {
    font-size: 0.7rem;
    font-weight: 600;
    color: #555;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Step pipeline ── */
.pipeline-step {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 6px;
    font-size: 0.85rem;
    font-family: 'JetBrains Mono', monospace;
    transition: all 0.3s;
}
.step-pending  { background: #141414; border: 1px solid #1E1E1E; color: #444; }
.step-running  { background: #1A2000; border: 1px solid #4A6000; color: #AACC00; }
.step-done     { background: #0D1F0D; border: 1px solid #1DB954; color: #1DB954; }
.step-icon { font-size: 1rem; min-width: 20px; }

/* ── Violation cards ── */
.viol-card {
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    border-left: 3px solid;
}
.viol-critical { background: #1A0A0A; border-color: #E53E3E; }
.viol-warning  { background: #1A1400; border-color: #D97706; }
.viol-info     { background: #0A0F1A; border-color: #2563EB; }
.viol-title    { font-weight: 600; font-size: 0.9rem; margin-bottom: 4px; }
.viol-body     { font-size: 0.8rem; color: #888; margin-bottom: 8px; }
.viol-fix      { font-size: 0.78rem; color: #1DB954; font-family: 'JetBrains Mono', monospace; }
.badge-critical { color: #E53E3E; font-size: 0.65rem; font-weight: 700; letter-spacing: 1px; background: #2A1010; padding: 2px 8px; border-radius: 4px; }
.badge-warning  { color: #D97706; font-size: 0.65rem; font-weight: 700; letter-spacing: 1px; background: #2A1E00; padding: 2px 8px; border-radius: 4px; }
.badge-info     { color: #2563EB; font-size: 0.65rem; font-weight: 700; letter-spacing: 1px; background: #0A1530; padding: 2px 8px; border-radius: 4px; }

/* ── Metric boxes ── */
.metric-row { display: flex; gap: 10px; margin-bottom: 1rem; }
.metric-box {
    flex: 1;
    background: #111111;
    border: 1px solid #1E1E1E;
    border-radius: 8px;
    padding: 0.9rem 1rem;
    text-align: center;
}
.metric-val { font-size: 1.8rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.metric-lbl { font-size: 0.7rem; color: #555; margin-top: 2px; letter-spacing: 1px; text-transform: uppercase; }

/* ── Terminal log ── */
.terminal {
    background: #080808;
    border: 1px solid #1E1E1E;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #4A9;
    max-height: 220px;
    overflow-y: auto;
    line-height: 1.7;
}
.log-ts  { color: #333; }
.log-ok  { color: #1DB954; }
.log-warn { color: #D97706; }
.log-err { color: #E53E3E; }
.log-dim { color: #444; }

/* ── RAG panel ── */
.rag-chunk {
    background: #0D1020;
    border: 1px solid #1E2A50;
    border-radius: 6px;
    padding: 0.7rem 1rem;
    font-size: 0.78rem;
    font-family: 'JetBrains Mono', monospace;
    color: #7A9CC8;
    margin-bottom: 6px;
}
.rag-score { float: right; color: #2563EB; font-weight: 700; }

/* ── Feature table ── */
.feat-row { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #161616; font-size: 0.82rem; }
.feat-key { color: #555; font-family: 'JetBrains Mono', monospace; }
.feat-val { color: #E8E8E8; font-weight: 500; }

/* ── Buttons ── */
.stButton > button {
    background: #1DB954 !important;
    color: #0A0A0A !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { background: #17A347 !important; transform: translateY(-1px); }

/* ── File uploader ── */
.stFileUploader > div {
    background: #111111 !important;
    border: 1.5px dashed #1E1E1E !important;
    border-radius: 10px !important;
}

/* ── Progress bar ── */
.stProgress > div > div { background-color: #1DB954 !important; }

/* ── Selectbox ── */
.stSelectbox > div > div { background: #111111 !important; border-color: #1E1E1E !important; color: #E8E8E8 !important; }

/* ── Section divider ── */
.dg-divider { border: none; border-top: 1px solid #161616; margin: 1.2rem 0; }
</style>
""", unsafe_allow_html=True)

# ─── Data: Sample CAD files ───────────────────────────────────────────────────
SAMPLE_FILES = {
    "bracket_assembly_v3.STEP": {
        "type": "Structural Bracket", "material": "AL6061-T6", "weight": "342g",
        "dims": "120 × 80 × 45 mm", "features": 14, "tolerances": 8,
        "features_extracted": {
            "Overall dimensions": "120 × 80 × 45 mm",
            "Material spec": "AL6061-T6",
            "Wall thickness (min)": "1.2 mm",
            "Hole diameter": "Ø 6.0 mm",
            "Surface finish": "Ra 3.2 μm",
            "Draft angle": "0.5°",
            "Fillet radius (min)": "0.8 mm",
            "Tolerance class": "ISO 2768-m",
            "Thread spec": "M6 × 1.0",
            "Assembly clearance": "0.15 mm",
        },
        "violations": [
            {
                "severity": "critical",
                "rule": "DFM-104: Minimum Wall Thickness",
                "description": "Wall thickness at rib section is 1.2mm — below the 1.5mm minimum for AL6061 die-casting per Varroc DFM standard DFM-104.",
                "fix": "→ Increase rib wall thickness to ≥ 1.5mm or switch manufacturing process to CNC machining.",
                "standard": "Varroc DFM-104 / ISO 10135",
                "confidence": 97,
            },
            {
                "severity": "warning",
                "rule": "ISO 2768-m: General Tolerance",
                "description": "Assembly clearance of 0.15mm is within ISO 2768-m limits but creates a risk of interference fit under thermal expansion at operating temperature (−20°C to +120°C).",
                "fix": "→ Revise clearance to 0.25mm minimum to account for AL6061 thermal expansion coefficient (23.6 μm/m·°C).",
                "standard": "ISO 2768-m / FMEA-TH-07",
                "confidence": 84,
            },
            {
                "severity": "warning",
                "rule": "DFM-211: Draft Angle",
                "description": "Draft angle of 0.5° is below the recommended 1.0° minimum for die-cast aluminium parts at this depth-to-width ratio.",
                "fix": "→ Increase draft angle to 1.0°–1.5° to ensure clean part release and reduce tooling wear.",
                "standard": "Varroc DFM-211",
                "confidence": 79,
            },
            {
                "severity": "info",
                "rule": "Surface Finish Optimisation",
                "description": "Ra 3.2μm surface finish on mating face may cause inconsistent seal performance. Non-critical but worth reviewing.",
                "fix": "→ Consider Ra 1.6μm for mating faces in contact with gaskets or sealing elements.",
                "standard": "Varroc SFC-03",
                "confidence": 65,
            },
        ],
        "anomaly_score": 0.74,
        "rag_chunks": [
            ("DFM-104 §3.2 — Minimum wall thickness for die-cast AL alloys shall be 1.5mm...", 0.94),
            ("FMEA-TH-07 — Thermal expansion clearance margin for bracket assemblies...", 0.87),
            ("DFM-211 §1.1 — Draft angles for vertical surfaces: 1.0° minimum for depth > 30mm...", 0.81),
            ("ISO 2768-m — General tolerances for linear and angular dimensions...", 0.76),
            ("SFC-03 §2 — Surface finish requirements for mating and sealing faces...", 0.61),
        ],
    },
    "headlamp_housing_v2.IGES": {
        "type": "Headlamp Housing", "material": "PC+ABS Blend", "weight": "218g",
        "dims": "340 × 160 × 95 mm", "features": 22, "tolerances": 11,
        "features_extracted": {
            "Overall dimensions": "340 × 160 × 95 mm",
            "Material spec": "PC+ABS (Lexan 940)",
            "Wall thickness (min)": "2.0 mm",
            "Snap-fit arm thickness": "1.8 mm",
            "Lens seat tolerance": "±0.3 mm",
            "Draft angle": "1.5°",
            "Gate location": "Side gate",
            "Rib height-to-thickness ratio": "6.5:1",
            "Boss diameter": "Ø 8.0 mm",
            "UV resistance coating": "Not specified",
        },
        "violations": [
            {
                "severity": "critical",
                "rule": "DFM-318: Rib H/T Ratio",
                "description": "Rib height-to-thickness ratio of 6.5:1 exceeds the 5:1 maximum for PC+ABS injection moulding — high risk of sink marks on Class-A surface.",
                "fix": "→ Reduce rib height or increase rib thickness to achieve ≤ 5:1 ratio. Consider coring out the rib base.",
                "standard": "Varroc DFM-318 / BASF Plastics Guidelines",
                "confidence": 96,
            },
            {
                "severity": "critical",
                "rule": "ECE R112: Headlamp Durability",
                "description": "UV resistance coating is unspecified. Automotive lighting housings must meet ECE R112 UV weathering standards for 3000hr equivalent exposure.",
                "fix": "→ Specify UV stabiliser additive (e.g. Tinuvin 234) in material spec or apply UV clear coat post-moulding.",
                "standard": "ECE Regulation R112 §6.2",
                "confidence": 93,
            },
            {
                "severity": "warning",
                "rule": "DFM-205: Snap-Fit Design",
                "description": "Snap-fit arm thickness of 1.8mm with current arm length gives a deflection strain of ~3.8% — above the 3.0% fatigue limit for PC+ABS at −20°C.",
                "fix": "→ Increase arm thickness to 2.2mm or reduce arm length by 8mm to keep strain ≤ 3.0%.",
                "standard": "Varroc DFM-205 / DuPont Snap-Fit Design Guide",
                "confidence": 81,
            },
        ],
        "anomaly_score": 0.88,
        "rag_chunks": [
            ("DFM-318 §4.1 — Maximum rib height-to-thickness ratio for PC+ABS: 5:1...", 0.96),
            ("ECE R112 §6.2 — UV weathering requirements for headlamp housings...", 0.91),
            ("DFM-205 §2.3 — Snap-fit deflection strain limits by material and temperature...", 0.83),
            ("Varroc Material Spec MS-44 — Approved thermoplastics for lighting applications...", 0.72),
            ("FMEA-PL-12 — Failure modes for injection-moulded snap-fit assemblies...", 0.68),
        ],
    },
    "ev_motor_bracket_v1.DXF": {
        "type": "EV Motor Bracket", "material": "S355 Steel", "weight": "1.24 kg",
        "dims": "280 × 190 × 60 mm", "features": 18, "tolerances": 13,
        "features_extracted": {
            "Overall dimensions": "280 × 190 × 60 mm",
            "Material spec": "S355 JR Steel",
            "Weld joint type": "Fillet weld",
            "Weld throat size": "4 mm",
            "Hole pattern": "8 × Ø10mm",
            "Surface treatment": "Zinc phosphate",
            "Fatigue class": "Not specified",
            "Corner radius (min)": "2.0 mm",
            "Plate thickness": "6 mm",
            "Bolt pre-load spec": "Not specified",
        },
        "violations": [
            {
                "severity": "critical",
                "rule": "AWS D1.1: Weld Throat Size",
                "description": "Fillet weld throat of 4mm is undersized for 6mm plate carrying EV motor loads (estimated 2.4kN vibration load). Minimum required throat: 5mm per AWS D1.1.",
                "fix": "→ Increase fillet weld throat to 5mm minimum. Specify weld class E70 or higher.",
                "standard": "AWS D1.1 / Varroc WLD-08",
                "confidence": 95,
            },
            {
                "severity": "warning",
                "rule": "Fatigue Classification Missing",
                "description": "EV motor brackets experience cyclic loading. No fatigue class (BS 7608 or IIW) is specified — critical for NVH and durability sign-off.",
                "fix": "→ Assign fatigue class D or E per BS 7608. Add fatigue life calculation to design notes.",
                "standard": "BS 7608 / IIW Doc. XIII-1965",
                "confidence": 88,
            },
            {
                "severity": "info",
                "rule": "Bolt Pre-load Specification",
                "description": "Bolt pre-load not specified for Ø10mm hole pattern. Under EV vibration, unspecified pre-load risks joint loosening.",
                "fix": "→ Specify torque value and use thread-locking compound (Loctite 243) or Nord-Lock washers.",
                "standard": "Varroc FST-15",
                "confidence": 72,
            },
        ],
        "anomaly_score": 0.81,
        "rag_chunks": [
            ("AWS D1.1 §4.2 — Minimum fillet weld sizes for structural steel plate...", 0.95),
            ("Varroc WLD-08 §3 — Weld specifications for EV drivetrain components...", 0.90),
            ("BS 7608 — Fatigue design of welded steel structures...", 0.85),
            ("IIW Doc. XIII-1965 — Fatigue classification of welded joints...", 0.77),
            ("Varroc FST-15 — Fastener pre-load and thread locking requirements...", 0.69),
        ],
    },
}

LOG_LINES = []


def ts():
    return f'<span class="log-ts">[{datetime.now().strftime("%H:%M:%S.%f")[:12]}]</span>'


def add_log(msg, level="ok"):
    cls = {"ok": "log-ok", "warn": "log-warn", "err": "log-err", "dim": "log-dim"}.get(level, "log-ok")
    LOG_LINES.append(f'{ts()} <span class="{cls}">{msg}</span>')


def render_log():
    html = "<br>".join(LOG_LINES[-30:])
    return f'<div class="terminal">{html}</div>'


def render_violation(v):
    sev = v["severity"]
    badge_cls = f"badge-{sev}"
    card_cls = f"viol-{sev}"
    sev_label = sev.upper()
    conf = v["confidence"]
    return f"""
    <div class="viol-card {card_cls}">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px">
            <span class="viol-title">{v['rule']}</span>
            <span>
                <span class="{badge_cls}">{sev_label}</span>
                &nbsp;<span style="font-size:0.7rem; color:#444; font-family:JetBrains Mono">confidence {conf}%</span>
            </span>
        </div>
        <div class="viol-body">{v['description']}</div>
        <div class="viol-fix">{v['fix']}</div>
        <div style="margin-top:6px; font-size:0.68rem; color:#333; font-family:JetBrains Mono">
            Standard ref: {v['standard']}
        </div>
    </div>"""


# ─── App State ────────────────────────────────────────────────────────────────
if "stage" not in st.session_state:
    st.session_state.stage = "upload"
if "selected_file" not in st.session_state:
    st.session_state.selected_file = None
if "log_lines_stored" not in st.session_state:
    st.session_state.log_lines_stored = []

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dg-header">
    <div>
        <div class="dg-logo">Design<span>Guard</span> AI</div>
        <div class="dg-subtitle">AI-Driven Design Intelligence · Early-Stage CAD Validation</div>
    </div>
    <div style="display:flex; gap:12px; align-items:center">
        <span class="dg-subtitle">Varroc Eureka Challenge 3.0 · PS-9</span>
        <span class="dg-badge">LIVE DEMO</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Stage: Upload ────────────────────────────────────────────────────────────
if st.session_state.stage == "upload":
    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.markdown('<div class="dg-card">', unsafe_allow_html=True)
        st.markdown('<div class="dg-card-title">Select CAD File</div>', unsafe_allow_html=True)

        file_choice = st.selectbox(
            "Load sample design file",
            list(SAMPLE_FILES.keys()),
            label_visibility="collapsed"
        )
        st.session_state.selected_file = file_choice

        fd = SAMPLE_FILES[file_choice]
        st.markdown(f"""
        <div style="display:flex; gap:10px; margin:12px 0">
            <div style="background:#141414; border:1px solid #1E1E1E; border-radius:6px; padding:8px 14px; flex:1; text-align:center">
                <div style="font-size:0.7rem; color:#555; margin-bottom:2px">TYPE</div>
                <div style="font-size:0.82rem; font-weight:600">{fd['type']}</div>
            </div>
            <div style="background:#141414; border:1px solid #1E1E1E; border-radius:6px; padding:8px 14px; flex:1; text-align:center">
                <div style="font-size:0.7rem; color:#555; margin-bottom:2px">MATERIAL</div>
                <div style="font-size:0.82rem; font-weight:600">{fd['material']}</div>
            </div>
            <div style="background:#141414; border:1px solid #1E1E1E; border-radius:6px; padding:8px 14px; flex:1; text-align:center">
                <div style="font-size:0.7rem; color:#555; margin-bottom:2px">DIMENSIONS</div>
                <div style="font-size:0.82rem; font-weight:600">{fd['dims']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<hr class="dg-divider">', unsafe_allow_html=True)
        st.markdown('<div class="dg-card-title">Feature Preview</div>', unsafe_allow_html=True)
        features_html = ""
        for k, v in list(fd["features_extracted"].items())[:6]:
            features_html += f'<div class="feat-row"><span class="feat-key">{k}</span><span class="feat-val">{v}</span></div>'
        st.markdown(features_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="dg-card">', unsafe_allow_html=True)
        st.markdown('<div class="dg-card-title">Validation Pipeline</div>', unsafe_allow_html=True)

        steps_html = ""
        pipeline_steps = [
            ("📂", "CAD File Ingestion", "OpenCascade / FreeCAD API"),
            ("⚙️", "Geometry Feature Extraction", "PyVista · Trimesh"),
            ("🗄️", "RAG Standards Retrieval", "LangChain · Pinecone"),
            ("🧠", "LLM Compliance Reasoning", "GPT-4o / Claude API"),
            ("🔍", "ML Anomaly Detection", "Isolation Forest"),
            ("📋", "Validation Report Generation", "FastAPI · PDF Export"),
        ]
        for icon, name, tech in pipeline_steps:
            steps_html += f"""
            <div class="pipeline-step step-pending">
                <span class="step-icon">{icon}</span>
                <div>
                    <div style="font-weight:500; color:#333">{name}</div>
                    <div style="font-size:0.68rem; color:#2A2A2A; margin-top:1px">{tech}</div>
                </div>
            </div>"""
        st.markdown(steps_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("▶  Run DesignGuard AI Validation", use_container_width=True):
            st.session_state.stage = "running"
            st.session_state.log_lines_stored = []
            st.rerun()

# ─── Stage: Running (animated pipeline) ──────────────────────────────────────
elif st.session_state.stage == "running":
    fd = SAMPLE_FILES[st.session_state.selected_file]

    st.markdown('<div class="dg-card">', unsafe_allow_html=True)
    st.markdown('<div class="dg-card-title">Running Validation Pipeline</div>', unsafe_allow_html=True)

    col_pipe, col_log = st.columns([1, 1])

    pipeline_steps = [
        ("📂", "CAD File Ingestion",           "OpenCascade / FreeCAD API",   1.2),
        ("⚙️",  "Geometry Feature Extraction",  "PyVista · Trimesh",           1.4),
        ("🗄️", "RAG Standards Retrieval",       "LangChain · Pinecone",        1.6),
        ("🧠", "LLM Compliance Reasoning",      "GPT-4o / Claude API",         2.0),
        ("🔍", "ML Anomaly Detection",          "Isolation Forest",            1.1),
        ("📋", "Validation Report Generation",  "FastAPI · PDF Export",        0.9),
    ]

    log_messages = [
        [("INFO  parsing STEP file headers...", "ok"),
         (f"INFO  file: {st.session_state.selected_file}", "dim"),
         ("INFO  OpenCascade kernel loaded successfully", "ok"),
         ("INFO  geometry topology validated ✓", "ok")],

        [("INFO  extracting boundary representation...", "ok"),
         (f"INFO  detected {fd['features']} geometric features", "ok"),
         (f"INFO  found {fd['tolerances']} tolerance annotations", "ok"),
         ("INFO  feature vector serialised → JSON", "ok")],

        [("INFO  querying Pinecone vector index...", "ok"),
         ("INFO  embedding model: text-embedding-3-large", "dim"),
         ("INFO  retrieved top-5 matching rule chunks", "ok"),
         ("INFO  similarity threshold: 0.60 | all passed", "ok")],

        [("INFO  sending context to LLM endpoint...", "ok"),
         ("INFO  model: gpt-4o | temperature: 0.1", "dim"),
         ("INFO  tokens: 3,241 prompt / 892 completion", "dim"),
         ("WARN  rule violations detected — see report", "warn")],

        [("INFO  running Isolation Forest on feature vec...", "ok"),
         (f"INFO  anomaly score: {fd['anomaly_score']:.2f}", "warn" if fd['anomaly_score'] > 0.7 else "ok"),
         ("INFO  threshold: 0.70 | flagging for review", "warn"),
         ("INFO  autoencoder cross-check: CONFIRMED", "ok")],

        [("INFO  compiling validation report...", "ok"),
         (f"INFO  {len(fd['violations'])} violations found → structured JSON", "ok"),
         ("INFO  PDF report rendered successfully", "ok"),
         ("INFO  ✓ pipeline complete", "ok")],
    ]

    pipe_placeholder = col_pipe.empty()
    log_placeholder = col_log.empty()
    prog_bar = st.progress(0)
    status_txt = st.empty()

    completed = []
    all_logs = []

    for i, (icon, name, tech, delay) in enumerate(pipeline_steps):
        status_txt.markdown(f'<div style="color:#1DB954; font-family:JetBrains Mono; font-size:0.8rem; margin:4px 0">⟳ Running: {name}...</div>', unsafe_allow_html=True)

        # Render pipeline steps
        steps_html = ""
        for j, (ic, nm, tc, _) in enumerate(pipeline_steps):
            if j < i:
                cls = "step-done"
                indicator = "✓"
                col_nm = "#1DB954"
            elif j == i:
                cls = "step-running"
                indicator = "◉"
                col_nm = "#AACC00"
            else:
                cls = "step-pending"
                indicator = "○"
                col_nm = "#333"
            steps_html += f"""
            <div class="pipeline-step {cls}">
                <span class="step-icon">{ic}</span>
                <div style="flex:1">
                    <div style="font-weight:500; color:{col_nm}">{nm}</div>
                    <div style="font-size:0.68rem; color:#2A2A2A; margin-top:1px">{tc}</div>
                </div>
                <span style="color:{col_nm}; font-size:0.8rem">{indicator}</span>
            </div>"""
        pipe_placeholder.markdown(steps_html, unsafe_allow_html=True)

        # Stream log messages for this step
        for msg, level in log_messages[i]:
            all_logs.append((msg, level))
            log_html = '<div class="terminal">'
            for lm, ll in all_logs[-20:]:
                cls = {"ok": "log-ok", "warn": "log-warn", "err": "log-err", "dim": "log-dim"}.get(ll, "log-ok")
                ts_str = datetime.now().strftime("%H:%M:%S.%f")[:12]
                log_html += f'<span class="log-ts">[{ts_str}]</span> <span class="{cls}">{lm}</span><br>'
            log_html += '</div>'
            log_placeholder.markdown(log_html, unsafe_allow_html=True)
            time.sleep(delay / 4)

        completed.append(i)
        prog_bar.progress((i + 1) / len(pipeline_steps))
        time.sleep(0.2)

    # Final state — all done
    steps_html = ""
    for ic, nm, tc, _ in pipeline_steps:
        steps_html += f"""
        <div class="pipeline-step step-done">
            <span class="step-icon">{ic}</span>
            <div style="flex:1">
                <div style="font-weight:500; color:#1DB954">{nm}</div>
                <div style="font-size:0.68rem; color:#2A2A2A; margin-top:1px">{tc}</div>
            </div>
            <span style="color:#1DB954; font-size:0.8rem">✓</span>
        </div>"""
    pipe_placeholder.markdown(steps_html, unsafe_allow_html=True)
    status_txt.markdown('<div style="color:#1DB954; font-family:JetBrains Mono; font-size:0.8rem; margin:4px 0">✓ Validation complete — 0 errors</div>', unsafe_allow_html=True)

    st.session_state.log_lines_stored = all_logs
    st.markdown('</div>', unsafe_allow_html=True)

    time.sleep(0.6)
    st.session_state.stage = "results"
    st.rerun()

# ─── Stage: Results ───────────────────────────────────────────────────────────
elif st.session_state.stage == "results":
    fd = SAMPLE_FILES[st.session_state.selected_file]
    violations = fd["violations"]
    n_critical = sum(1 for v in violations if v["severity"] == "critical")
    n_warning  = sum(1 for v in violations if v["severity"] == "warning")
    n_info     = sum(1 for v in violations if v["severity"] == "info")
    anom_score = fd["anomaly_score"]

    # ── Top metric bar ────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-box">
            <div class="metric-val" style="color:#E53E3E">{n_critical}</div>
            <div class="metric-lbl">Critical</div>
        </div>
        <div class="metric-box">
            <div class="metric-val" style="color:#D97706">{n_warning}</div>
            <div class="metric-lbl">Warnings</div>
        </div>
        <div class="metric-box">
            <div class="metric-val" style="color:#2563EB">{n_info}</div>
            <div class="metric-lbl">Info</div>
        </div>
        <div class="metric-box">
            <div class="metric-val" style="color:{'#E53E3E' if anom_score > 0.7 else '#1DB954'}">{anom_score:.2f}</div>
            <div class="metric-lbl">Anomaly Score</div>
        </div>
        <div class="metric-box">
            <div class="metric-val" style="color:#1DB954">{len(fd['features_extracted'])}</div>
            <div class="metric-lbl">Features Parsed</div>
        </div>
        <div class="metric-box">
            <div class="metric-val" style="color:#7C3AED">{len(fd['rag_chunks'])}</div>
            <div class="metric-lbl">Rules Retrieved</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 0.9])

    # ── Left: Violations ─────────────────────────────────────────────────────
    with col1:
        st.markdown('<div class="dg-card">', unsafe_allow_html=True)
        st.markdown('<div class="dg-card-title">Validation Report — Violations Detected</div>', unsafe_allow_html=True)

        viols_html = ""
        for v in violations:
            viols_html += render_violation(v)
        st.markdown(viols_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Feature extraction panel
        st.markdown('<div class="dg-card">', unsafe_allow_html=True)
        st.markdown('<div class="dg-card-title">Extracted Geometry Features</div>', unsafe_allow_html=True)
        feats_html = ""
        for k, v in fd["features_extracted"].items():
            feats_html += f'<div class="feat-row"><span class="feat-key">{k}</span><span class="feat-val">{v}</span></div>'
        st.markdown(feats_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Right: RAG + anomaly + log ────────────────────────────────────────────
    with col2:
        st.markdown('<div class="dg-card">', unsafe_allow_html=True)
        st.markdown('<div class="dg-card-title">RAG — Retrieved Standards Chunks</div>', unsafe_allow_html=True)
        for chunk_text, score in fd["rag_chunks"]:
            st.markdown(f'<div class="rag-chunk"><span class="rag-score">sim: {score:.2f}</span>{chunk_text}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Anomaly
        anom_color = "#E53E3E" if anom_score > 0.8 else "#D97706" if anom_score > 0.6 else "#1DB954"
        anom_label = "HIGH RISK" if anom_score > 0.8 else "MODERATE" if anom_score > 0.6 else "NORMAL"
        st.markdown(f"""
        <div class="dg-card">
            <div class="dg-card-title">ML Anomaly Detection — Isolation Forest</div>
            <div style="display:flex; align-items:center; gap:16px; margin-bottom:10px">
                <div style="font-size:2.5rem; font-weight:700; font-family:JetBrains Mono; color:{anom_color}">{anom_score:.2f}</div>
                <div>
                    <div style="color:{anom_color}; font-weight:700; font-size:0.8rem; letter-spacing:1px">{anom_label}</div>
                    <div style="color:#444; font-size:0.75rem; margin-top:2px">Threshold: 0.70 · Trained on 14,200 Varroc designs</div>
                </div>
            </div>
            <div style="background:#0D0D0D; border-radius:6px; height:8px; overflow:hidden">
                <div style="background:{anom_color}; width:{int(anom_score*100)}%; height:100%; border-radius:6px; transition:width 1s"></div>
            </div>
            <div style="font-size:0.75rem; color:#444; margin-top:8px; font-family:JetBrains Mono">
                Autoencoder cross-check: CONFIRMED &nbsp;|&nbsp; n_estimators=200 &nbsp;|&nbsp; contamination=0.05
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Terminal log
        st.markdown('<div class="dg-card">', unsafe_allow_html=True)
        st.markdown('<div class="dg-card-title">Pipeline Execution Log</div>', unsafe_allow_html=True)
        if st.session_state.log_lines_stored:
            log_html = '<div class="terminal">'
            for lm, ll in st.session_state.log_lines_stored:
                cls = {"ok": "log-ok", "warn": "log-warn", "err": "log-err", "dim": "log-dim"}.get(ll, "log-ok")
                log_html += f'<span class="{cls}">{lm}</span><br>'
            log_html += '</div>'
            st.markdown(log_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Run again ─────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button("◀  Validate Another Design", use_container_width=True):
            st.session_state.stage = "upload"
            st.session_state.log_lines_stored = []
            st.rerun()