import streamlit as st
import os
import subprocess
from docxtpl import DocxTemplate
from datetime import datetime
from num2words import num2words
import base64

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Rue de l'Orient 46 — Etterbeek, Brussels",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- HELPER: encode local image to base64 ---
def img_b64(path):
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        ext = path.split(".")[-1].lower()
        mime = "image/jpeg" if ext in ["jpg","jpeg"] else "image/png"
        return f"data:{mime};base64,{data}"
    except:
        return ""

# Paths for static images (works both locally and on Streamlit Cloud)
STATIC = "static"
IMG = {
    "cour":     f"{STATIC}/chambre_cour.jpg",
    "sud1":     f"{STATIC}/chambre_sud1.jpg",
    "sud2":     f"{STATIC}/chambre_sud2.jpg",
    "house":    f"{STATIC}/house.jpg",
    "entrance": f"{STATIC}/entrance.jpg",
    "kitchen":  f"{STATIC}/kitchen.jpg",
    "living1":  f"{STATIC}/living1.jpg",
    "living2":  f"{STATIC}/living2.jpg",
}
# Use app/static/ URL path for Streamlit static serving
IMG_URL = {k: f"app/{v}" for k, v in IMG.items()}

# --- CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap');

/* Reset Streamlit chrome */
.stApp { background: #F8F6F1 !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header, .stDeployButton { visibility: hidden !important; display: none !important; }
[data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 0 !important; padding-bottom: 0 !important; max-width: 100% !important; }

/* ── HEADER BANNER ── */
.header-banner {
    position: relative;
    width: 100%;
    height: 340px;
    overflow: hidden;
    background: #1a1a1a;
}
.header-banner iframe {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 177.78vh;
    height: 100%;
    min-width: 100%;
    min-height: 56.25vw;
    pointer-events: none;
    border: none;
    opacity: 0.75;
}
.header-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.55) 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 1rem 2rem;
}
.header-tag {
    font-family: 'Inter', sans-serif;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.7);
    border: 1px solid rgba(255,255,255,0.3);
    padding: 0.3rem 1.2rem;
    margin-bottom: 1rem;
}
.header-title {
    font-family: 'Lora', serif;
    font-weight: 400;
    font-size: clamp(2rem, 5vw, 4rem);
    color: #fff;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}
.header-sub {
    font-family: 'Inter', sans-serif;
    font-weight: 300;
    font-size: 0.9rem;
    letter-spacing: 0.1em;
    color: rgba(255,255,255,0.75);
    text-transform: uppercase;
}

/* ── WELCOME SECTION ── */
.welcome-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    min-height: 420px;
}
.welcome-text {
    padding: 3.5rem 3.5rem;
    background: #F8F6F1;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.welcome-photos {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 6px;
}
.welcome-photos img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}
.eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 0.62rem;
    font-weight: 500;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #B85C38;
    margin-bottom: 0.8rem;
}
.section-h2 {
    font-family: 'Lora', serif;
    font-weight: 400;
    font-size: clamp(1.6rem, 3vw, 2.4rem);
    color: #1A1A1A;
    line-height: 1.2;
    margin-bottom: 1.2rem;
}
.welcome-body {
    font-family: 'Inter', sans-serif;
    font-size: 0.92rem;
    line-height: 1.8;
    color: #4A4A4A;
    max-width: 55ch;
}
.welcome-body p { margin-bottom: 0.9rem; }
.welcome-body strong { color: #1A1A1A; font-weight: 500; }

/* ── RULES BAND ── */
.rules-band {
    background: #2C2C2C;
    padding: 1.6rem 3rem;
    display: flex;
    justify-content: center;
    gap: 3rem;
    flex-wrap: wrap;
}
.rule-item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    color: rgba(255,255,255,0.75);
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    letter-spacing: 0.05em;
}
.rule-icon { font-size: 1.1rem; }

/* ── ROOMS SECTION ── */
.rooms-section {
    padding: 4rem 2.5rem 3rem;
    background: #F8F6F1;
}
.rooms-intro {
    text-align: center;
    margin-bottom: 2.5rem;
}

/* Room card */
.room-card {
    background: #fff;
    border: 1px solid #E8E4DC;
    overflow: hidden;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
    cursor: pointer;
}
.room-card:hover {
    box-shadow: 0 16px 48px rgba(0,0,0,0.1);
    transform: translateY(-3px);
}
.room-card img {
    width: 100%;
    height: 220px;
    object-fit: cover;
    display: block;
    transition: transform 0.5s ease;
}
.room-card:hover img { transform: scale(1.04); }
.room-card-body { padding: 1.4rem 1.5rem; }
.room-name {
    font-family: 'Lora', serif;
    font-size: 1.25rem;
    color: #1A1A1A;
    margin-bottom: 0.2rem;
}
.room-floor {
    font-family: 'Inter', sans-serif;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #B85C38;
    margin-bottom: 0.8rem;
}
.room-price {
    font-family: 'Lora', serif;
    font-size: 1.6rem;
    color: #1A1A1A;
    font-weight: 400;
}
.room-price span {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    color: #888;
    font-weight: 300;
}
.room-detail {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    color: #888;
    margin-top: 0.3rem;
    line-height: 1.6;
}
.room-select-btn {
    margin-top: 1rem;
    display: inline-block;
    font-family: 'Inter', sans-serif;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    background: #1A1A1A;
    color: #fff;
    padding: 0.55rem 1.4rem;
    border: none;
    cursor: pointer;
    transition: background 0.2s ease;
}

/* ── FORM SECTION ── */
.form-wrapper {
    background: #fff;
    padding: 4rem 3.5rem;
    max-width: 860px;
    margin: 0 auto;
    border: 1px solid #E8E4DC;
}
.form-divider {
    width: 40px;
    height: 2px;
    background: #B85C38;
    margin: 1rem 0 2rem;
}
.form-step {
    font-family: 'Inter', sans-serif;
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #B85C38;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #E8E4DC;
    margin-bottom: 1.2rem;
    margin-top: 1.8rem;
    display: block;
}

/* Inputs */
.stTextInput > label,
.stSelectbox > label,
.stTextArea > label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.65rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #5A5A5A !important;
}
.stTextInput input, .stTextArea textarea {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    border: 1px solid #D8D4CC !important;
    border-radius: 0 !important;
    background: #FAFAF8 !important;
    box-shadow: none !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #B85C38 !important;
    box-shadow: 0 0 0 2px rgba(184,92,56,0.12) !important;
}
[data-baseweb="select"] > div {
    border-radius: 0 !important;
    border: 1px solid #D8D4CC !important;
    background: #FAFAF8 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: #B85C38 !important;
    box-shadow: 0 0 0 2px rgba(184,92,56,0.12) !important;
}

/* Submit button */
.stFormSubmitButton > button {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.7rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    background: #1A1A1A !important;
    color: #fff !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0.85rem 3rem !important;
    width: 100% !important;
    transition: background 0.2s !important;
}
.stFormSubmitButton > button:hover {
    background: #B85C38 !important;
}
.stDownloadButton > button {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    background: transparent !important;
    color: #1A1A1A !important;
    border: 1px solid #1A1A1A !important;
    border-radius: 0 !important;
    padding: 0.7rem 2rem !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: #1A1A1A !important;
    color: #fff !important;
}

/* Selected room highlight */
.room-selected {
    outline: 2px solid #B85C38;
    outline-offset: -2px;
}

/* Summary box */
.summary-box {
    background: #FBF8F3;
    border: 1px solid #E8E4DC;
    border-left: 3px solid #B85C38;
    padding: 1rem 1.2rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    color: #4A4A4A;
    line-height: 1.7;
}
.summary-box strong { color: #1A1A1A; }

/* Footer */
.site-footer {
    background: #1A1A1A;
    padding: 2.5rem 3rem;
    text-align: center;
    font-family: 'Inter', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    color: rgba(255,255,255,0.35);
    line-height: 1.8;
}
.site-footer strong { color: rgba(255,255,255,0.65); font-weight: 400; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #F8F6F1; }
::-webkit-scrollbar-thumb { background: #B85C38; }

/* Responsive */
@media (max-width: 768px) {
    .welcome-section { grid-template-columns: 1fr; }
    .welcome-photos { height: 280px; }
    .rooms-section { padding: 2.5rem 1rem; }
    .form-wrapper { padding: 2rem 1.2rem; }
    .rules-band { gap: 1.2rem; padding: 1.2rem; }
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE for room selection ──
if "selected_room" not in st.session_state:
    st.session_state.selected_room = "1E"

# ── BUSINESS LOGIC ──
CHAMBRES = {
    "1E":    {"nom": "Chambre Cour",  "etage": "1st floor",  "prix": 570, "charges": 30, "gar_red": 600, "img_key": "cour"},
    "GRISE": {"nom": "Chambre Sud 1", "etage": "2nd floor",  "prix": 540, "charges": 30, "gar_red": 500, "img_key": "sud1"},
    "ROUGE": {"nom": "Chambre Sud 2", "etage": "3rd floor",  "prix": 550, "charges": 30, "gar_red": 550, "img_key": "sud2"},
}

def convert_to_pdf(docx_path):
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_path])
    return docx_path.replace(".docx", ".pdf")

# ── HEADER BANNER with Brussels drone video ──
st.markdown("""
<div class="header-banner">
    <iframe
        src="https://www.youtube.com/embed/QJjZ3BywAdY?autoplay=1&mute=1&loop=1&playlist=QJjZ3BywAdY&controls=0&showinfo=0&rel=0&modestbranding=1&disablekb=1&iv_load_policy=3&start=8"
        allow="autoplay; fullscreen"
        allowfullscreen>
    </iframe>
    <div class="header-overlay">
        <div class="header-tag">Room rental · Etterbeek, Brussels</div>
        <h1 class="header-title">Rue de l'Orient 46</h1>
        <p class="header-sub">Close to the European Institutions · Owner-managed</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── WELCOME SECTION ──
# Build photo grid URLs (static serving)
p_entrance = IMG_URL["entrance"]
p_house    = IMG_URL["house"]
p_kitchen  = IMG_URL["kitchen"]
p_living   = IMG_URL["living1"]

st.markdown(f"""
<div class="welcome-section">
    <div class="welcome-text">
        <p class="eyebrow">Welcome</p>
        <h2 class="section-h2">A home away<br>from home</h2>
        <div class="welcome-body">
            <p>We are happy to welcome you to this <strong>friendly and vibrant neighbourhood</strong>,
            ideally located close to the European institutions.</p>
            <p>Nearby, you can enjoy a drink at <strong>Place Jourdan</strong>, do your groceries at
            Lidl or Colruyt, or go for a run in one of the beautiful parks around the house:
            <strong>Parc Louis Hap</strong>, Parc Léopold, or Parc du Cinquantenaire.</p>
            <p>The house is <strong>owner-managed</strong> and offers three bedrooms. We aim to create
            a calm, respectful, and family-like environment. This is not a party house.
            We value peace and quiet, and we expect everyone to respect this atmosphere.</p>
            <p>We are a <strong>non-smoking home</strong>, and we all make an effort to keep the
            common areas clean and pleasant for everyone. We also believe in mutual respect
            and helping each other when needed.</p>
            <p>We hope you will feel comfortable and at home here very quickly. <strong>Welcome!</strong> 🙂</p>
        </div>
    </div>
    <div class="welcome-photos">
        <img src="{p_entrance}" alt="Entrance" loading="lazy">
        <img src="{p_house}"    alt="House"    loading="lazy">
        <img src="{p_kitchen}"  alt="Kitchen"  loading="lazy">
        <img src="{p_living}"   alt="Living"   loading="lazy">
    </div>
</div>
""", unsafe_allow_html=True)

# ── RULES BAND ──
st.markdown("""
<div class="rules-band">
    <div class="rule-item"><span class="rule-icon">🚭</span> Non-smoking home</div>
    <div class="rule-item"><span class="rule-icon">🤝</span> Mutual respect</div>
    <div class="rule-item"><span class="rule-icon">🌿</span> Clean common areas</div>
    <div class="rule-item"><span class="rule-icon">🔇</span> Peace &amp; quiet</div>
    <div class="rule-item"><span class="rule-icon">🏛️</span> 5 min from EU institutions</div>
    <div class="rule-item"><span class="rule-icon">🛒</span> Lidl &amp; Colruyt nearby</div>
</div>
""", unsafe_allow_html=True)

# ── ROOMS SECTION ──
st.markdown("""
<div class="rooms-section">
    <div class="rooms-intro">
        <p class="eyebrow" style="display:block;">The bedrooms</p>
        <h2 class="section-h2">Choose your room</h2>
        <p style="font-family:'Inter',sans-serif; font-size:0.85rem; color:#6A6A6A; margin-top:0.5rem;">
            Click on a room to select it — the booking form below will update automatically.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
for col, (key, ch) in zip([col1, col2, col3], CHAMBRES.items()):
    with col:
        is_selected = st.session_state.selected_room == key
        selected_class = "room-selected" if is_selected else ""
        badge = "✓ Selected" if is_selected else "Select this room →"
        badge_style = "background:#B85C38; color:#fff;" if is_selected else "background:#1A1A1A; color:#fff;"

        st.markdown(f"""
        <div class="room-card {selected_class}">
            <img src="{IMG_URL[ch['img_key']]}" alt="{ch['nom']}" loading="lazy">
            <div class="room-card-body">
                <p class="room-floor">{ch['etage']}</p>
                <h3 class="room-name">{ch['nom']}</h3>
                <div class="room-price">{ch['prix']} € <span>/ month</span></div>
                <p class="room-detail">
                    Utilities: {ch['charges']} €&nbsp;&nbsp;·&nbsp;&nbsp;Security deposit: {ch['gar_red']} €
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(badge, key=f"btn_{key}", use_container_width=True):
            st.session_state.selected_room = key
            st.rerun()

# Spacer
st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)

# ── BOOKING FORM ──
st.markdown("""
<div style="padding: 0 2.5rem;">
<div class="form-wrapper">
    <p class="eyebrow">Rental contract</p>
    <h2 class="section-h2">Generate your contract</h2>
    <div class="form-divider"></div>
    <p style="font-family:'Inter',sans-serif; font-size:0.85rem; color:#6A6A6A; margin-bottom:2rem; line-height:1.7;">
        Fill in the form below to generate your personalised rental contract as a PDF,
        ready to sign. All fields marked with * are required.
    </p>
</div>
</div>
""", unsafe_allow_html=True)

with st.form("contract_form"):
    st.markdown('<span class="form-step">① Personal information</span>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 2])
    with c1:
        gender = st.selectbox("Title", ["Mr.", "Ms.", "Dr."])
    with c2:
        fname = st.text_input("First name *")
    with c3:
        lname = st.text_input("Last name *")

    c4, c5, c6 = st.columns(3)
    with c4:
        natio = st.text_input("Nationality *")
    with c5:
        bday = st.text_input("Date of birth *", placeholder="DD/MM/YYYY")
    with c6:
        email = st.text_input("Email address *")

    st.markdown('<span class="form-step">② Room & rental details</span>', unsafe_allow_html=True)

    ch_options = list(CHAMBRES.keys())
    current_idx = ch_options.index(st.session_state.selected_room)
    room = st.selectbox(
        "Room",
        ch_options,
        index=current_idx,
        format_func=lambda k: f"{CHAMBRES[k]['nom']} — {CHAMBRES[k]['prix']} €/month ({CHAMBRES[k]['etage']})"
    )

    ch = CHAMBRES[room]
    st.markdown(f"""
    <div class="summary-box">
        <strong>{ch['nom']}</strong> · {ch['etage']}<br>
        Rent: <strong>{ch['prix']} €</strong> &nbsp;·&nbsp;
        Utilities: <strong>{ch['charges']} €</strong> &nbsp;·&nbsp;
        Total monthly: <strong>{ch['prix'] + ch['charges']} €</strong> &nbsp;·&nbsp;
        Security deposit: <strong>{ch['gar_red']} €</strong>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="form-step">③ Special clause (optional)</span>', unsafe_allow_html=True)
    special_clause = st.text_area(
        "Any specific condition agreed with the owner",
        placeholder="E.g. garage access included, pet allowed...",
        height=90
    )

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    submit = st.form_submit_button("Generate my rental contract")

if submit:
    if not all([fname, lname, natio, bday, email]):
        st.error("Please fill in all required fields (*).")
    else:
        ch = CHAMBRES[room]
        context = {
            "gender": gender,
            "prenom": fname,
            "nom": lname.upper(),
            "nationalite": natio,
            "date_naissance": bday,
            "email": email,
            "chambre": room,
            "chambre_nom": ch["nom"],
            "etage": ch["etage"],
            "loyer": ch["prix"],
            "loyer_total": f"{num2words(ch['prix'], lang='fr')} euros ({ch['prix']} €)",
            "charges": ch["charges"],
            "garantie": ch["gar_red"],
            "special_clause": special_clause if special_clause else "None",
            "date_signature": datetime.now().strftime("%d/%m/%Y"),
        }
        tpl = DocxTemplate("Contrat de location - Template.docx")
        tpl.render(context)
        docx_name = f"Contract_{lname.upper()}_{room}.docx"
        tpl.save(docx_name)

        with st.spinner("Generating your secure contract..."):
            pdf_name = convert_to_pdf(docx_name)

        st.success(f"✓ Contract generated for {gender} {fname} {lname.upper()} — {ch['nom']}")
        dl1, dl2 = st.columns(2)
        with dl1:
            with open(pdf_name, "rb") as f:
                st.download_button("⬇ Download PDF contract", f,
                                   file_name=pdf_name, mime="application/pdf")
        with dl2:
            with open(docx_name, "rb") as f:
                st.download_button("⬇ Download Word contract", f,
                                   file_name=docx_name,
                                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

# ── FOOTER ──
st.markdown("""
<div class="site-footer">
    <strong>Rue de l'Orient 46</strong> · Etterbeek, 1040 Brussels · Belgium<br>
    Owner-managed accommodation · Contracts generated securely · © 2025
</div>
""", unsafe_allow_html=True)
