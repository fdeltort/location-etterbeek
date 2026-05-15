import streamlit as st
import os
import subprocess
from docxtpl import DocxTemplate
from datetime import datetime
from num2words import num2words

st.set_page_config(
    page_title="46 Rue de l'Orient — Etterbeek, Brussels",
    page_icon="🏠",
    layout="wide"
)

# ── IMAGE URLS (hébergées sur expert-europe.eu) ──
URL_COUR  = "https://www.expert-europe.eu/medias/editor/oneshot-images/4346331516a0681396d543.jpg"
URL_SUD1  = "https://www.expert-europe.eu/medias/editor/oneshot-images/4892571986a068182aaf97.jpg"
URL_SUD2  = "https://www.expert-europe.eu/f8d5a1b5-34da-4ab6-bf12-398a4d5d7ec3"
URL_HERO  = "https://www.expert-europe.eu/medias/editor/oneshot-images/14335012956a06820ed498a.png"

# ── CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Lato:wght@300;400;700&display=swap');

/* Force light mode partout */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"],
.stApp, .main, section, .block-container {
    background-color: #FFFFFF !important;
    color: #1A1A1A !important;
}
* { color: #1A1A1A; }

/* Streamlit chrome */
#MainMenu, footer, header, .stDeployButton { visibility: hidden !important; }
[data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 0 !important; max-width: 100% !important; }

/* Typographie */
h1, h2, h3, .section-title {
    font-family: 'Playfair Display', serif !important;
    color: #1A1A1A !important;
}
p, span, label, div {
    font-family: 'Lato', sans-serif !important;
    color: #1A1A1A !important;
}

/* ── HERO IMAGE ── */
.hero-wrap {
    position: relative;
    width: 100%;
    height: 280px;
    overflow: hidden;
    background: #111;
}
.hero-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center 40%;
    opacity: 0.72;
    display: block;
}
.hero-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 1rem 2rem;
    background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.55));
}
.hero-tag {
    font-family: 'Lato', sans-serif;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.32em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.75) !important;
    border: 1px solid rgba(255,255,255,0.35);
    padding: 0.28rem 1.1rem;
    margin-bottom: 0.9rem;
    display: inline-block;
}
.hero-title {
    font-family: 'Playfair Display', serif !important;
    font-weight: 400;
    font-size: clamp(1.9rem, 4.5vw, 3.5rem);
    color: #FFFFFF !important;
    line-height: 1.1;
    margin-bottom: 0.4rem;
}
.hero-sub {
    font-family: 'Lato', sans-serif !important;
    font-weight: 300;
    font-size: 0.85rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.72) !important;
}

/* ── WELCOME ── */
.welcome-box {
    max-width: 780px;
    margin: 3rem auto 2rem;
    padding: 0 2rem;
    text-align: center;
}
.welcome-box h2 {
    font-family: 'Playfair Display', serif !important;
    font-size: clamp(1.4rem, 2.5vw, 2rem);
    font-weight: 400;
    color: #1A1A1A !important;
    margin-bottom: 1.2rem;
}
.welcome-box p {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.95rem;
    line-height: 1.85;
    color: #3A3A3A !important;
    margin-bottom: 0.85rem;
    max-width: 68ch;
    margin-left: auto;
    margin-right: auto;
}
.accent-line {
    width: 44px;
    height: 2px;
    background: #1A1A1A;
    margin: 1.2rem auto 1.8rem;
}

/* ── RULES BAND ── */
.rules-band {
    background: #F5F3EE;
    padding: 1.2rem 2rem;
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    flex-wrap: wrap;
    border-top: 1px solid #E8E4DC;
    border-bottom: 1px solid #E8E4DC;
    margin-bottom: 3rem;
}
.rule-item {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.78rem;
    color: #3A3A3A !important;
    letter-spacing: 0.04em;
    display: flex;
    align-items: center;
    gap: 0.45rem;
}

/* ── ROOM CARDS ── */
.rooms-title {
    text-align: center;
    margin-bottom: 2rem;
    padding: 0 1rem;
}
.rooms-title h2 {
    font-family: 'Playfair Display', serif !important;
    font-size: clamp(1.3rem, 2.5vw, 1.9rem);
    font-weight: 400;
    color: #1A1A1A !important;
    margin-bottom: 0.4rem;
}
.rooms-title p {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.83rem;
    color: #777 !important;
}

.room-card {
    background: #FFFFFF;
    border: 1px solid #E8E4DC;
    overflow: hidden;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
    margin-bottom: 0.5rem;
}
.room-card:hover {
    box-shadow: 0 12px 36px rgba(0,0,0,0.1);
    transform: translateY(-2px);
}
.room-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    display: block;
    transition: transform 0.45s ease;
}
.room-card.selected {
    border: 2px solid #1A1A1A;
}
.room-card:hover img { transform: scale(1.03); }
.room-card-body { padding: 1.1rem 1.3rem 1.3rem; }
.room-floor {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.59rem;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #888 !important;
    margin-bottom: 0.3rem;
}
.room-name {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.15rem;
    color: #1A1A1A !important;
    margin-bottom: 0.6rem;
}
.room-price {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.4rem;
    color: #1A1A1A !important;
}
.room-price span {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.7rem;
    color: #888 !important;
    font-weight: 300;
}
.room-detail {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.73rem;
    color: #888 !important;
    margin-top: 0.25rem;
    line-height: 1.6;
}

/* ── FORM SECTION ── */
.form-section {
    max-width: 780px;
    margin: 3rem auto 4rem;
    padding: 0 1.5rem;
}
.form-section h2 {
    font-family: 'Playfair Display', serif !important;
    font-size: clamp(1.3rem, 2.5vw, 1.9rem);
    font-weight: 400;
    color: #1A1A1A !important;
    margin-bottom: 0.5rem;
}
.form-section p {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.85rem;
    color: #666 !important;
    margin-bottom: 1.5rem;
    line-height: 1.7;
}
.form-step-label {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #888 !important;
    padding-bottom: 0.45rem;
    border-bottom: 1px solid #E8E4DC;
    margin-bottom: 1rem;
    margin-top: 1.5rem;
    display: block;
}

/* Streamlit inputs */
.stTextInput > label, .stSelectbox > label, .stTextArea > label {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.63rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    color: #555 !important;
}
.stTextInput input, .stTextArea textarea {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.9rem !important;
    border: 1px solid #D0CCC4 !important;
    border-radius: 0 !important;
    background: #FAFAF8 !important;
    color: #1A1A1A !important;
    box-shadow: none !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #1A1A1A !important;
    box-shadow: none !important;
}
[data-baseweb="select"] > div {
    border-radius: 0 !important;
    border: 1px solid #D0CCC4 !important;
    background: #FAFAF8 !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: #1A1A1A !important;
}

/* Summary */
.summary-box {
    background: #F9F7F3;
    border: 1px solid #E8E4DC;
    border-left: 2px solid #1A1A1A;
    padding: 0.9rem 1.1rem;
    font-family: 'Lato', sans-serif !important;
    font-size: 0.82rem;
    color: #3A3A3A !important;
    line-height: 1.75;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
}
.summary-box strong { color: #1A1A1A !important; font-weight: 700; }

/* Buttons */
.stFormSubmitButton > button {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    background: #1A1A1A !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0.85rem 3rem !important;
    width: 100% !important;
    margin-top: 1rem !important;
    transition: background 0.2s !important;
}
.stFormSubmitButton > button:hover { background: #444 !important; }

.stButton > button {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.62rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    background: #1A1A1A !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0.6rem 1.2rem !important;
    width: 100% !important;
    transition: background 0.2s !important;
}
.stButton > button:hover { background: #444 !important; }

.stDownloadButton > button {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    background: transparent !important;
    color: #1A1A1A !important;
    border: 1px solid #1A1A1A !important;
    border-radius: 0 !important;
    padding: 0.7rem 1.8rem !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: #1A1A1A !important;
    color: #fff !important;
}

/* Footer */
.site-footer {
    background: #1A1A1A;
    padding: 2rem 3rem;
    text-align: center;
    font-family: 'Lato', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    color: rgba(255,255,255,0.4) !important;
    line-height: 1.9;
}
.site-footer strong { color: rgba(255,255,255,0.65) !important; font-weight: 400; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #F5F3EE; }
::-webkit-scrollbar-thumb { background: #1A1A1A; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
if "selected_room" not in st.session_state:
    st.session_state.selected_room = "1E"

# ── DATA ──
CHAMBRES = {
    "1E":    {"nom": "Chambre Cour",  "etage": "1st floor", "prix": 570, "charges": 30, "gar_red": 600,  "img": URL_COUR},
    "GRISE": {"nom": "Chambre Sud 1", "etage": "2nd floor", "prix": 540, "charges": 30, "gar_red": 500,  "img": URL_SUD1},
    "ROUGE": {"nom": "Chambre Sud 2", "etage": "3rd floor", "prix": 550, "charges": 30, "gar_red": 550,  "img": URL_SUD2},
}

def convert_to_pdf(docx_path):
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_path])
    return docx_path.replace(".docx", ".pdf")

# ── HERO ──
st.markdown(f"""
<div class="hero-wrap">
    <img src="{URL_HERO}" alt="Rue de l'Orient 46">
    <div class="hero-overlay">
        <span class="hero-tag">Room rental · Etterbeek, Brussels</span>
        <h1 class="hero-title">46, Rue de l'Orient</h1>
        <p class="hero-sub">Close to the European Institutions · Owner-managed</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── WELCOME TEXT ──
st.markdown("""
<div class="welcome-box">
    <h2>Welcome to Rue de l'Orient!</h2>
    <div class="accent-line"></div>
    <p>We are happy to welcome you to this friendly and vibrant neighbourhood, ideally located
    close to the European institutions. Nearby, you can enjoy a drink at <strong>Place Jourdan</strong>,
    do your groceries at Lidl or Colruyt, or go for a run in one of the beautiful parks around
    the house: <strong>Parc Louis Hap</strong>, Parc Léopold, or Parc du Cinquantenaire.</p>
    <p>The house is owner-managed and offers three bedrooms. We aim to create a calm, respectful,
    and family-like environment. This is not a party house. We value peace and quiet, and we
    expect everyone to respect this atmosphere.</p>
    <p>We are a non-smoking home, and we all make an effort to keep the common areas clean and
    pleasant for everyone. We also believe in mutual respect and helping each other when needed.</p>
    <p>We hope you will feel comfortable and at home here very quickly. <strong>Welcome!</strong> 🙂</p>
</div>
""", unsafe_allow_html=True)

# ── RULES BAND ──
st.markdown("""
<div class="rules-band">
    <span class="rule-item">🚭 Non-smoking</span>
    <span class="rule-item">🤝 Mutual respect</span>
    <span class="rule-item">🌿 Clean common areas</span>
    <span class="rule-item">🔇 Peace &amp; quiet</span>
    <span class="rule-item">🏛️ 5 min · EU institutions</span>
    <span class="rule-item">🛒 Lidl &amp; Colruyt nearby</span>
    <span class="rule-item">🌳 Parc Louis Hap · Parc du Cinquantenaire</span>
</div>
""", unsafe_allow_html=True)

# ── ROOM CARDS ──
st.markdown("""
<div class="rooms-title">
    <h2>The Bedrooms</h2>
    <p>Click on a room to select it — the form below will update automatically.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
for col, (key, ch) in zip([col1, col2, col3], CHAMBRES.items()):
    with col:
        is_sel = st.session_state.selected_room == key
        sel_class = "room-card selected" if is_sel else "room-card"
        btn_label = "✓ Selected" if is_sel else "Select →"

        # Note: chambre sud 1 photo is rotated — CSS fix
        img_style = "transform: rotate(0deg);" if key != "GRISE" else "transform: rotate(90deg); object-position: center;"

        st.markdown(f"""
        <div class="{sel_class}">
            <div style="height:200px; overflow:hidden;">
                <img src="{ch['img']}" alt="{ch['nom']}"
                     style="width:100%; height:200px; object-fit:cover; display:block; {img_style}">
            </div>
            <div class="room-card-body">
                <p class="room-floor">{ch['etage']}</p>
                <h3 class="room-name">{ch['nom']}</h3>
                <div class="room-price">{ch['prix']} € <span>/ month</span></div>
                <p class="room-detail">Utilities: {ch['charges']} € &nbsp;·&nbsp; Deposit: {ch['gar_red']} €</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(btn_label, key=f"btn_{key}", use_container_width=True):
            st.session_state.selected_room = key
            st.rerun()

# ── FORM ──
st.markdown("""
<div class="form-section">
    <h2>Generate your rental contract</h2>
    <div class="accent-line" style="margin-left:0;"></div>
    <p>Fill in the form below to receive your personalised rental contract as a PDF,
    ready to sign. All fields marked with * are required.</p>
</div>
""", unsafe_allow_html=True)

with st.form("contract_form"):

    st.markdown('<span class="form-step-label">① Personal information</span>', unsafe_allow_html=True)
    col_t, col_f, col_l = st.columns([1, 2, 2])
    with col_t:
        gender = st.selectbox("Title", ["Mr.", "Ms.", "Dr."])
    with col_f:
        fname = st.text_input("First name *")
    with col_l:
        lname = st.text_input("Last name *")

    col_n, col_b, col_e = st.columns(3)
    with col_n:
        natio = st.text_input("Nationality *")
    with col_b:
        bday = st.text_input("Date of birth *", placeholder="DD/MM/YYYY")
    with col_e:
        email = st.text_input("Email address *")

    st.markdown('<span class="form-step-label">② Room & rental details</span>', unsafe_allow_html=True)

    ch_keys = list(CHAMBRES.keys())
    current_idx = ch_keys.index(st.session_state.selected_room)
    room = st.selectbox(
        "Room",
        ch_keys,
        index=current_idx,
        format_func=lambda k: f"{CHAMBRES[k]['nom']} — {CHAMBRES[k]['prix']} €/month ({CHAMBRES[k]['etage']})"
    )

    ch = CHAMBRES[room]
    st.markdown(f"""
    <div class="summary-box">
        <strong>{ch['nom']}</strong> · {ch['etage']}<br>
        Rent: <strong>{ch['prix']} €</strong> &nbsp;·&nbsp;
        Utilities: <strong>{ch['charges']} €</strong> &nbsp;·&nbsp;
        Total / month: <strong>{ch['prix'] + ch['charges']} €</strong> &nbsp;·&nbsp;
        Security deposit: <strong>{ch['gar_red']} €</strong>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="form-step-label">③ Special clause (optional)</span>', unsafe_allow_html=True)
    special_clause = st.text_area(
        "Any specific condition agreed with the owner",
        placeholder="E.g. garage access included, pet allowed...",
        height=85
    )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
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

        st.success(f"✓ Contract ready for {gender} {fname} {lname.upper()} — {ch['nom']}")

        dl1, dl2 = st.columns(2)
        with dl1:
            with open(pdf_name, "rb") as f:
                st.download_button("⬇ Download PDF", f,
                                   file_name=pdf_name, mime="application/pdf")
        with dl2:
            with open(docx_name, "rb") as f:
                st.download_button("⬇ Download Word", f,
                                   file_name=docx_name,
                                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

# ── FOOTER ──
st.markdown("""
<div class="site-footer">
    <strong>46, Rue de l'Orient</strong> · Etterbeek, 1040 Brussels · Belgium<br>
    Owner-managed accommodation · Contracts generated securely · © 2025
</div>
""", unsafe_allow_html=True)
