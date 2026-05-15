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

# ── IMAGE URLS ──
URL_COUR  = "https://www.expert-europe.eu/medias/editor/oneshot-images/4346331516a0681396d543.jpg"
URL_SUD1  = "https://www.expert-europe.eu/medias/editor/oneshot-images/4892571986a068182aaf97.jpg"
URL_SUD2  = "https://www.expert-europe.eu/medias/editor/oneshot-images/6632892076a0683fce6acf.jpg"
URL_HERO  = "https://www.expert-europe.eu/medias/editor/oneshot-images/14335012956a06820ed498a.png"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Lato:wght@300;400;700&display=swap');

/* ── FORCE LIGHT MODE ── */
html, body, .stApp, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main, .block-container,
section[data-testid="stSidebar"] {
    background-color: #FBF9F6 !important;
    color: #3D2B1F !important;
}

#MainMenu, footer, header, .stDeployButton { visibility: hidden !important; }
[data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 0 !important; max-width: 100% !important; }

/* ── GLOBAL TYPE ── */
body, p, span, div, label, li {
    font-family: 'Lato', sans-serif !important;
    color: #3D2B1F !important;
}
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #2C1A0E !important;
}

/* ── HERO ── */
.hero-wrap {
    width: 100%;
    height: 260px;
    overflow: hidden;
    background: #2C1A0E;
    position: relative;
}
.hero-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center 40%;
    display: block;
}

/* ── WELCOME ── */
.welcome-box {
    max-width: 760px;
    margin: 3.5rem auto 0;
    padding: 0 2rem;
    text-align: center;
}
.welcome-box h2 {
    font-family: 'Playfair Display', serif !important;
    font-size: clamp(1.5rem, 2.8vw, 2.1rem);
    font-weight: 400;
    color: #2C1A0E !important;
    margin-bottom: 1rem;
}
.welcome-box p {
    font-size: 0.95rem;
    line-height: 1.9;
    color: #5C3D2E !important;
    margin-bottom: 0.9rem;
    max-width: 66ch;
    margin-left: auto;
    margin-right: auto;
}
.warm-line {
    width: 48px;
    height: 2px;
    background: linear-gradient(to right, #C4763A, #E8A87C);
    margin: 1.1rem auto 1.9rem;
    border-radius: 2px;
}

/* ── RULES BAND ── */
.rules-band {
    background: #F3EDE4;
    padding: 1.3rem 2rem;
    display: flex;
    justify-content: center;
    gap: 2.2rem;
    flex-wrap: wrap;
    margin: 2.5rem 0;
    border-radius: 0;
}
.rule-item {
    font-size: 0.78rem !important;
    color: #5C3D2E !important;
    letter-spacing: 0.03em;
}

/* ── ROOMS ── */
.rooms-title {
    text-align: center;
    padding: 0 1rem 1.8rem;
}
.rooms-title h2 {
    font-family: 'Playfair Display', serif !important;
    font-size: clamp(1.4rem, 2.5vw, 1.9rem);
    font-weight: 400;
    color: #2C1A0E !important;
    margin-bottom: 0.4rem;
}
.rooms-title p {
    font-size: 0.83rem;
    color: #9B7B6A !important;
}

/* ── ROOM CARD ── */
.room-card {
    background: #FFFFFF;
    border-radius: 14px;
    overflow: hidden;
    border: 1.5px solid #EAE0D5;
    transition: box-shadow 0.28s ease, transform 0.28s ease, border-color 0.28s ease;
    cursor: pointer;
    margin-bottom: 0.4rem;
}
.room-card:hover {
    box-shadow: 0 18px 48px rgba(60,30,10,0.13);
    transform: translateY(-4px);
    border-color: #C4763A;
}
.room-card.selected {
    border: 2px solid #C4763A;
    box-shadow: 0 8px 28px rgba(196,118,58,0.18);
}
.room-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    display: block;
    transition: transform 0.5s ease;
}
.room-card:hover img { transform: scale(1.04); }
.room-card-body { padding: 1.15rem 1.4rem 1.3rem; }
.room-floor {
    font-size: 0.58rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.24em !important;
    text-transform: uppercase;
    color: #C4763A !important;
    margin-bottom: 0.25rem;
}
.room-name {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.15rem !important;
    color: #2C1A0E !important;
    margin-bottom: 0.5rem;
}
.room-price {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.4rem !important;
    color: #2C1A0E !important;
}
.room-price span {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.7rem !important;
    color: #9B7B6A !important;
    font-weight: 300;
}
.room-detail {
    font-size: 0.73rem !important;
    color: #9B7B6A !important;
    margin-top: 0.25rem;
    line-height: 1.6;
}

/* ── FORM AREA ── */
.form-area {
    max-width: 800px;
    margin: 3rem auto 4rem;
    padding: 0 1.5rem;
}
.form-card {
    background: #FFFFFF;
    border-radius: 16px;
    border: 1.5px solid #EAE0D5;
    padding: 2.5rem 2.8rem;
    box-shadow: 0 4px 24px rgba(60,30,10,0.06);
}
.form-area h2 {
    font-family: 'Playfair Display', serif !important;
    font-size: clamp(1.3rem, 2.5vw, 1.9rem);
    font-weight: 400;
    color: #2C1A0E !important;
    margin-bottom: 0.4rem;
}
.form-area p {
    font-size: 0.85rem;
    color: #9B7B6A !important;
    margin-bottom: 1.5rem;
    line-height: 1.75;
}
.form-step-label {
    font-size: 0.58rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.26em !important;
    text-transform: uppercase;
    color: #C4763A !important;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #EAE0D5;
    margin-bottom: 1rem;
    margin-top: 1.4rem;
    display: block;
}

/* ── STREAMLIT INPUTS ── */
.stTextInput > label, .stSelectbox > label, .stTextArea > label {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.62rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    color: #7A5C4A !important;
}
.stTextInput input, .stTextArea textarea {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.9rem !important;
    border: 1.5px solid #DDD4C8 !important;
    border-radius: 8px !important;
    background: #FBF9F6 !important;
    color: #2C1A0E !important;
    box-shadow: none !important;
    transition: border-color 0.2s ease !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #C4763A !important;
    box-shadow: 0 0 0 3px rgba(196,118,58,0.12) !important;
}
[data-baseweb="select"] > div {
    border-radius: 8px !important;
    border: 1.5px solid #DDD4C8 !important;
    background: #FBF9F6 !important;
    transition: border-color 0.2s ease !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: #C4763A !important;
    box-shadow: 0 0 0 3px rgba(196,118,58,0.12) !important;
}

/* ── SUMMARY BOX ── */
.summary-box {
    background: #FDF6EF;
    border: 1.5px solid #EAD8C5;
    border-radius: 10px;
    border-left: 3px solid #C4763A;
    padding: 0.9rem 1.2rem;
    font-size: 0.82rem !important;
    color: #5C3D2E !important;
    line-height: 1.8;
    margin-top: 0.5rem;
    margin-bottom: 0.8rem;
}
.summary-box strong { color: #2C1A0E !important; font-weight: 700; }

/* ── BUTTONS ── */
.stFormSubmitButton > button {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    background: linear-gradient(135deg, #C4763A, #A85A22) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.85rem 3rem !important;
    width: 100% !important;
    margin-top: 1.2rem !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 18px rgba(196,118,58,0.3) !important;
}
.stFormSubmitButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

.stButton > button {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.6rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    background: #2C1A0E !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.55rem 1rem !important;
    width: 100% !important;
    transition: background 0.2s, transform 0.15s !important;
}
.stButton > button:hover {
    background: #C4763A !important;
    transform: translateY(-1px) !important;
}

.stDownloadButton > button {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    background: transparent !important;
    color: #2C1A0E !important;
    border: 1.5px solid #2C1A0E !important;
    border-radius: 8px !important;
    padding: 0.7rem 1.8rem !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: #2C1A0E !important;
    color: #FBF9F6 !important;
}

/* ── FOOTER ── */
.site-footer {
    background: #2C1A0E;
    padding: 2.2rem 3rem;
    text-align: center;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    color: rgba(255,245,235,0.45) !important;
    line-height: 1.9;
}
.site-footer strong { color: rgba(255,245,235,0.7) !important; font-weight: 400; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #F3EDE4; }
::-webkit-scrollbar-thumb { background: #C4763A; border-radius: 4px; }

@media (max-width: 768px) {
    .form-card { padding: 1.5rem 1.2rem; }
    .rules-band { gap: 0.9rem; padding: 1rem; }
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
if "selected_room" not in st.session_state:
    st.session_state.selected_room = "1E"

# ── DATA ──
CHAMBRES = {
    "1E":    {"nom": "Chambre Cour",  "etage": "1st floor", "prix": 570, "charges": 30, "gar_red": 600, "img": URL_COUR, "rotate": False},
    "GRISE": {"nom": "Chambre Sud 1", "etage": "2nd floor", "prix": 540, "charges": 30, "gar_red": 600, "img": URL_SUD1, "rotate": True},
    "ROUGE": {"nom": "Chambre Sud 2", "etage": "3rd floor", "prix": 550, "charges": 30, "gar_red": 600, "img": URL_SUD2, "rotate": False},
}

def convert_to_pdf(docx_path):
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_path])
    return docx_path.replace(".docx", ".pdf")

# ── HERO — image seule, sans texte ──
st.markdown(f"""
<div class="hero-wrap">
    <img src="{URL_HERO}" alt="46 Rue de l'Orient, Etterbeek">
</div>
""", unsafe_allow_html=True)

# ── WELCOME ──
st.markdown("""
<div class="welcome-box">
    <h2>Welcome to Rue de l'Orient!</h2>
    <div class="warm-line"></div>
    <p>We are happy to welcome you to this friendly and vibrant neighbourhood, ideally located
    close to the European institutions. Nearby, you can enjoy a drink at <strong>Place Jourdan</strong>,
    do your groceries at Lidl or Colruyt, or go for a run in one of the beautiful parks around
    the house: <strong>Parc Louis Hap</strong>, Parc Leopold, or Parc du Cinquantenaire.</p>
    <p>The house is owner-managed and offers three bedrooms. We aim to create a calm, respectful,
    and family-like environment. This is not a party house — we value peace and quiet, and we
    expect everyone to respect this atmosphere.</p>
    <p>We are a non-smoking home. We all make an effort to keep the common areas clean and
    pleasant, and we believe in mutual respect and helping each other when needed.</p>
    <p>We hope you will feel comfortable and at home here very quickly. <strong>Welcome!</strong></p>
</div>
""", unsafe_allow_html=True)

# ── RULES BAND ──
st.markdown("""
<div class="rules-band">
    <span class="rule-item">Non-smoking home</span>
    <span class="rule-item">Mutual respect</span>
    <span class="rule-item">Clean common areas</span>
    <span class="rule-item">Peace &amp; quiet</span>
    <span class="rule-item">5 min · EU institutions</span>
    <span class="rule-item">Lidl &amp; Colruyt nearby</span>
    <span class="rule-item">Parc Louis Hap · Parc du Cinquantenaire</span>
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
        btn_label = "Selected" if is_sel else "Select this room"
        img_style = "transform: rotate(90deg); object-fit: cover; width: 100%; height: 200px;" if ch["rotate"] else "width: 100%; height: 200px; object-fit: cover;"

        st.markdown(f"""
        <div class="{sel_class}">
            <div style="height:200px; overflow:hidden; background:#F3EDE4;">
                <img src="{ch['img']}" alt="{ch['nom']}" style="{img_style} display:block;">
            </div>
            <div class="room-card-body">
                <p class="room-floor">{ch['etage']}</p>
                <h3 class="room-name">{ch['nom']}</h3>
                <div class="room-price">{ch['prix']} &euro; <span>/ month</span></div>
                <p class="room-detail">Utilities: {ch['charges']} &euro; &nbsp;&middot;&nbsp; Deposit: {ch['gar_red']} &euro;</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(btn_label, key=f"btn_{key}", use_container_width=True):
            st.session_state.selected_room = key
            st.rerun()

# ── FORM ──
st.markdown("""
<div class="form-area">
    <h2>Generate your rental contract</h2>
    <div class="warm-line" style="margin-left:0;"></div>
    <p>Fill in the form below to receive your personalised rental contract as a PDF,
    ready to sign. All fields marked with * are required.</p>
    <div class="form-card">
</div>
</div>
""", unsafe_allow_html=True)

with st.form("contract_form"):
    st.markdown('<span class="form-step-label">Personal information</span>', unsafe_allow_html=True)

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

    st.markdown('<span class="form-step-label">Room & rental details</span>', unsafe_allow_html=True)

    ch_keys = list(CHAMBRES.keys())
    current_idx = ch_keys.index(st.session_state.selected_room)
    room = st.selectbox(
        "Room",
        ch_keys,
        index=current_idx,
        format_func=lambda k: f"{CHAMBRES[k]['nom']}  —  {CHAMBRES[k]['prix']} €/month  ({CHAMBRES[k]['etage']})"
    )
    ch = CHAMBRES[room]
    st.markdown(f"""
    <div class="summary-box">
        <strong>{ch['nom']}</strong> &middot; {ch['etage']}<br>
        Rent: <strong>{ch['prix']} &euro;</strong> &nbsp;&middot;&nbsp;
        Utilities: <strong>{ch['charges']} &euro;</strong> &nbsp;&middot;&nbsp;
        Total / month: <strong>{ch['prix'] + ch['charges']} &euro;</strong> &nbsp;&middot;&nbsp;
        Security deposit: <strong>{ch['gar_red']} &euro;</strong>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="form-step-label">Special clause (optional)</span>', unsafe_allow_html=True)
    special_clause = st.text_area(
        "Any specific condition agreed with the owner",
        placeholder="E.g. garage access included, pet allowed...",
        height=85,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
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

        st.success(f"Contract ready for {gender} {fname} {lname.upper()} — {ch['nom']}")
        dl1, dl2 = st.columns(2)
        with dl1:
            with open(pdf_name, "rb") as f:
                st.download_button("Download PDF", f, file_name=pdf_name, mime="application/pdf")
        with dl2:
            with open(docx_name, "rb") as f:
                st.download_button("Download Word", f, file_name=docx_name,
                                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

# ── FOOTER ──
st.markdown("""
<div class="site-footer">
    <strong>46, Rue de l'Orient</strong> &middot; Etterbeek, 1040 Brussels &middot; Belgium<br>
    Owner-managed accommodation &middot; Contracts generated securely &middot; 2025
</div>
""", unsafe_allow_html=True)
