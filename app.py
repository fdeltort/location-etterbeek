import streamlit as st
import os
import subprocess
from docxtpl import DocxTemplate
from datetime import datetime
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Rue de l'Orient 46 — Etterbeek",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS LUXE COMPLET ---
st.markdown("""
<style>
/* =============================================
   IMPORTS TYPOGRAPHIE
   ============================================= */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500&display=swap');

/* =============================================
   RESET & BASE
   ============================================= */
* { box-sizing: border-box; margin: 0; padding: 0; }

/* Force fond blanc, supprime le gris Streamlit */
.stApp {
    background: #FAFAF8 !important;
    font-family: 'Jost', sans-serif !important;
    color: #1A1A1A !important;
}

/* Masquer éléments inutiles Streamlit */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stHeader"] { background: transparent !important; }
.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
}

/* =============================================
   HERO SECTION — Vidéo Plein écran
   ============================================= */
.hero-wrapper {
    position: relative;
    width: 100%;
    height: 88vh;
    overflow: hidden;
    background: #0d0d0d;
}

.hero-video-container {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 100%; height: 100%;
    overflow: hidden;
}

.hero-video-container iframe {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 177.78vh; /* 16:9 ratio */
    height: 100%;
    min-width: 100%;
    min-height: 56.25vw;
    pointer-events: none;
    border: none;
}

.hero-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
        to bottom,
        rgba(10,10,10,0.35) 0%,
        rgba(10,10,10,0.15) 40%,
        rgba(10,10,10,0.55) 100%
    );
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}

.hero-badge {
    font-family: 'Jost', sans-serif;
    font-weight: 400;
    font-size: 0.7rem;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.75);
    margin-bottom: 1.4rem;
    border: 1px solid rgba(255,255,255,0.3);
    padding: 0.45rem 1.4rem;
    border-radius: 0;
}

.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-weight: 300;
    font-size: clamp(3rem, 6vw, 6rem);
    color: #FFFFFF;
    line-height: 1.05;
    letter-spacing: -0.01em;
    margin-bottom: 1.2rem;
}

.hero-subtitle {
    font-family: 'Jost', sans-serif;
    font-weight: 300;
    font-size: clamp(0.9rem, 1.5vw, 1.05rem);
    letter-spacing: 0.12em;
    color: rgba(255,255,255,0.75);
    text-transform: uppercase;
    margin-bottom: 2.8rem;
}

.hero-scroll-hint {
    position: absolute;
    bottom: 2.5rem;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.6rem;
    color: rgba(255,255,255,0.55);
    font-family: 'Jost', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    animation: pulse 2.5s ease-in-out infinite;
}

.hero-scroll-hint::after {
    content: '';
    width: 1px;
    height: 40px;
    background: rgba(255,255,255,0.4);
    display: block;
}

@keyframes pulse {
    0%, 100% { opacity: 0.5; transform: translateX(-50%) translateY(0); }
    50% { opacity: 1; transform: translateX(-50%) translateY(-6px); }
}

/* =============================================
   BANDE CARACTERISTIQUES
   ============================================= */
.features-band {
    background: #1A1A1A;
    padding: 1.8rem 4rem;
    display: flex;
    justify-content: center;
    gap: 4rem;
    flex-wrap: wrap;
}

.feature-item {
    text-align: center;
    color: rgba(255,255,255,0.85);
}

.feature-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.7rem;
    font-weight: 400;
    color: #C9A96E;
    line-height: 1;
    margin-bottom: 0.25rem;
}

.feature-label {
    font-family: 'Jost', sans-serif;
    font-size: 0.62rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.45);
}

/* =============================================
   SECTION PHOTOS GALERIE
   ============================================= */
.section-eyebrow {
    font-family: 'Jost', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #C9A96E;
    margin-bottom: 1rem;
}

.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-weight: 300;
    font-size: clamp(2.2rem, 4vw, 3.5rem);
    line-height: 1.1;
    color: #1A1A1A;
    margin-bottom: 1rem;
}

.section-lead {
    font-family: 'Jost', sans-serif;
    font-size: 0.95rem;
    line-height: 1.75;
    color: #6B6B6B;
    max-width: 52ch;
}

.gallery-grid {
    display: grid;
    grid-template-columns: 1.5fr 1fr;
    grid-template-rows: 260px 260px;
    gap: 12px;
    border-radius: 0;
}

.gallery-item {
    overflow: hidden;
    background: #e8e4de;
}

.gallery-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.7s ease;
    display: block;
}

.gallery-item:hover img {
    transform: scale(1.04);
}

.gallery-item.tall {
    grid-row: span 2;
}

/* =============================================
   SECTION CHAMBRES — CARTES
   ============================================= */
.rooms-section {
    background: #F4F1EC;
    padding: 6rem 4rem;
}

.room-card {
    background: #FFFFFF;
    border: 1px solid rgba(0,0,0,0.07);
    padding: 0;
    overflow: hidden;
    transition: box-shadow 0.3s ease, transform 0.3s ease;
    cursor: pointer;
}

.room-card:hover {
    box-shadow: 0 20px 60px rgba(0,0,0,0.12);
    transform: translateY(-4px);
}

.room-card-img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    display: block;
}

.room-card-body {
    padding: 1.8rem;
}

.room-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.5rem;
    font-weight: 400;
    color: #1A1A1A;
    margin-bottom: 0.4rem;
}

.room-floor {
    font-family: 'Jost', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #C9A96E;
    margin-bottom: 1rem;
}

.room-price {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem;
    font-weight: 300;
    color: #1A1A1A;
}

.room-price span {
    font-family: 'Jost', sans-serif;
    font-size: 0.75rem;
    color: #9B9B9B;
    font-weight: 300;
    letter-spacing: 0.1em;
}

.room-charges {
    font-family: 'Jost', sans-serif;
    font-size: 0.78rem;
    color: #9B9B9B;
    margin-top: 0.3rem;
}

/* =============================================
   FORMULAIRE SECTION
   ============================================= */
.form-section {
    padding: 6rem 4rem;
    max-width: 1100px;
    margin: 0 auto;
}

.form-divider {
    width: 50px;
    height: 1px;
    background: #C9A96E;
    margin: 1.5rem 0 2.5rem 0;
}

/* Inputs Streamlit — override complet */
.stTextInput > label,
.stSelectbox > label,
.stTextArea > label,
.stDateInput > label {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.7rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #5A5A5A !important;
    margin-bottom: 0.4rem !important;
}

.stTextInput input,
.stSelectbox select,
.stTextArea textarea {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.95rem !important;
    color: #1A1A1A !important;
    background: #FAFAF8 !important;
    border: 1px solid #D8D4CC !important;
    border-radius: 0 !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s ease !important;
    box-shadow: none !important;
}

.stTextInput input:focus,
.stSelectbox select:focus,
.stTextArea textarea:focus {
    border-color: #C9A96E !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(201,169,110,0.15) !important;
}

/* Sélecteur Streamlit */
[data-baseweb="select"] > div {
    border-radius: 0 !important;
    border: 1px solid #D8D4CC !important;
    background: #FAFAF8 !important;
    font-family: 'Jost', sans-serif !important;
}

[data-baseweb="select"] > div:focus-within {
    border-color: #C9A96E !important;
    box-shadow: 0 0 0 2px rgba(201,169,110,0.15) !important;
}

/* Bouton de soumission */
.stFormSubmitButton > button {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.25em !important;
    text-transform: uppercase !important;
    background: #1A1A1A !important;
    color: #FFFFFF !important;
    border: 1px solid #1A1A1A !important;
    border-radius: 0 !important;
    padding: 0.9rem 3rem !important;
    transition: all 0.25s ease !important;
    width: 100% !important;
}

.stFormSubmitButton > button:hover {
    background: #C9A96E !important;
    border-color: #C9A96E !important;
    color: #FFFFFF !important;
}

/* Download button */
.stDownloadButton > button {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    background: transparent !important;
    color: #1A1A1A !important;
    border: 1px solid #1A1A1A !important;
    border-radius: 0 !important;
    padding: 0.8rem 2.5rem !important;
    transition: all 0.25s ease !important;
}

.stDownloadButton > button:hover {
    background: #1A1A1A !important;
    color: #FFFFFF !important;
}

/* Alerts & messages */
.stAlert {
    border-radius: 0 !important;
    border-left: 3px solid !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.85rem !important;
}

/* Spinner */
.stSpinner > div {
    color: #C9A96E !important;
}

/* Subheaders du formulaire */
.stSubheader, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    font-weight: 400 !important;
    font-size: 1.4rem !important;
    color: #1A1A1A !important;
    letter-spacing: 0.02em !important;
}

/* Colonnes — espacement fin */
[data-testid="column"] {
    padding-left: 0.75rem !important;
    padding-right: 0.75rem !important;
}

/* Separateur section formulaire */
.form-step-title {
    font-family: 'Jost', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #C9A96E;
    margin-bottom: 1.2rem;
    margin-top: 2rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #E8E4DC;
    display: block;
}

/* =============================================
   FOOTER
   ============================================= */
.site-footer {
    background: #0F0F0F;
    padding: 3.5rem 4rem;
    text-align: center;
    color: rgba(255,255,255,0.35);
    font-family: 'Jost', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
}

.site-footer strong {
    color: rgba(255,255,255,0.7);
    font-weight: 400;
}

/* =============================================
   CITATION LUXE
   ============================================= */
.luxury-quote {
    text-align: center;
    padding: 5rem 2rem;
    background: #1A1A1A;
}

.luxury-quote blockquote {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1.6rem, 3vw, 2.4rem);
    font-weight: 300;
    font-style: italic;
    color: rgba(255,255,255,0.85);
    line-height: 1.5;
    max-width: 700px;
    margin: 0 auto 1.5rem;
}

.luxury-quote cite {
    font-family: 'Jost', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #C9A96E;
    font-style: normal;
}

/* Scrollbar élégante */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #F4F1EC; }
::-webkit-scrollbar-thumb { background: #C9A96E; border-radius: 0; }

/* =============================================
   RESPONSIVE
   ============================================= */
@media (max-width: 768px) {
    .features-band { padding: 1.5rem 1.5rem; gap: 1.5rem; }
    .gallery-grid { grid-template-columns: 1fr; grid-template-rows: auto; }
    .gallery-item.tall { grid-row: span 1; }
    .rooms-section { padding: 3rem 1.5rem; }
    .form-section { padding: 3rem 1.5rem; }
}
</style>
""", unsafe_allow_html=True)

# =============================================
# LOGIQUE MÉTIER
# =============================================
CHAMBRES = {
    "1E":    {"nom": "Suite Premier Étage", "prix": 570, "charges": 30, "gar_red": 600, "etage": "1er étage",
              "img": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80"},
    "GRISE": {"nom": "Chambre Grise",       "prix": 540, "charges": 50, "gar_red": 500, "etage": "2e étage",
              "img": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800&q=80"},
    "ROUGE": {"nom": "Chambre Rouge",       "prix": 550, "charges": 40, "gar_red": 550, "etage": "3e étage",
              "img": "https://images.unsplash.com/photo-1560185127-6a9eed8d4d23?w=800&q=80"},
}

def convert_to_pdf(docx_path):
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_path])
    return docx_path.replace(".docx", ".pdf")

# =============================================
# HERO — Vidéo drone Bruxelles
# =============================================
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-video-container">
        <!-- Vidéo drone Bruxelles : Tour & Taxis vue aérienne 4K -->
        <iframe
            src="https://www.youtube.com/embed/i8y5NZa9osU?autoplay=1&mute=1&loop=1&playlist=i8y5NZa9osU&controls=0&showinfo=0&rel=0&modestbranding=1&disablekb=1&iv_load_policy=3&start=5"
            allow="autoplay; fullscreen"
            allowfullscreen>
        </iframe>
    </div>
    <div class="hero-overlay">
        <div class="hero-badge">Location Résidentielle · Etterbeek, Bruxelles</div>
        <h1 class="hero-title">Rue de l'Orient 46</h1>
        <p class="hero-subtitle">L'élégance et le calme au cœur d'Etterbeek</p>
    </div>
    <div class="hero-scroll-hint">Découvrir</div>
</div>
""", unsafe_allow_html=True)

# =============================================
# BANDE CARACTÉRISTIQUES
# =============================================
st.markdown("""
<div class="features-band">
    <div class="feature-item">
        <div class="feature-value">3</div>
        <div class="feature-label">Chambres disponibles</div>
    </div>
    <div class="feature-item">
        <div class="feature-value">540–570 €</div>
        <div class="feature-label">Loyer mensuel</div>
    </div>
    <div class="feature-item">
        <div class="feature-value">Etterbeek</div>
        <div class="feature-label">Quartier européen</div>
    </div>
    <div class="feature-item">
        <div class="feature-value">2025</div>
        <div class="feature-label">Entièrement rénové</div>
    </div>
    <div class="feature-item">
        <div class="feature-value">Contrat</div>
        <div class="feature-label">Généré instantanément</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================
# SECTION BRUXELLES — photos + texte
# =============================================
st.markdown("""
<div style="display:grid; grid-template-columns:1fr 1fr; gap:0; min-height:600px;">
    <div style="padding:5rem 4rem; background:#FAFAF8; display:flex; flex-direction:column; justify-content:center;">
        <p class="section-eyebrow">Le quartier</p>
        <h2 class="section-title">Vivre au cœur<br>de Bruxelles</h2>
        <div class="form-divider"></div>
        <p class="section-lead">
            Etterbeek, commune prisée aux portes du Quartier européen, offre une qualité de vie incomparable.
            Parcs verdoyants, marchés animés, cafés bruxellois authentiques — tout à portée de main.
        </p>
        <p class="section-lead" style="margin-top:1rem;">
            Le 46, Rue de l'Orient bénéficie d'une situation idéale : à deux pas des institutions
            de l'Union européenne, du Cinquantenaire et du Parc du Cinquantenaire.
        </p>
    </div>
    <div class="gallery-grid" style="display:grid; grid-template-columns:1.5fr 1fr; grid-template-rows:300px 300px; gap:8px;">
        <div class="gallery-item tall" style="grid-row:span 2; overflow:hidden;">
            <img src="https://images.unsplash.com/photo-1559827291-72ee739d0d9a?w=900&q=80"
                 alt="Grand-Place Bruxelles" loading="lazy" style="width:100%;height:100%;object-fit:cover;transition:transform 0.7s ease;">
        </div>
        <div class="gallery-item" style="overflow:hidden;">
            <img src="https://images.unsplash.com/photo-1518684079-3c830dcef090?w=700&q=80"
                 alt="Bruxelles architecture" loading="lazy" style="width:100%;height:100%;object-fit:cover;transition:transform 0.7s ease;">
        </div>
        <div class="gallery-item" style="overflow:hidden;">
            <img src="https://images.unsplash.com/photo-1565060169194-19fabf63012c?w=700&q=80"
                 alt="Bruxelles Cinquantenaire" loading="lazy" style="width:100%;height:100%;object-fit:cover;transition:transform 0.7s ease;">
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================
# CITATION LUXE
# =============================================
st.markdown("""
<div class="luxury-quote">
    <blockquote>
        « Une adresse, c'est bien plus qu'une porte — c'est le début d'une histoire. »
    </blockquote>
    <cite>Rue de l'Orient, Etterbeek — Bruxelles</cite>
</div>
""", unsafe_allow_html=True)

# =============================================
# SECTION CHAMBRES
# =============================================
st.markdown("""
<div class="rooms-section">
    <div style="text-align:center; margin-bottom:3.5rem;">
        <p class="section-eyebrow" style="justify-content:center; display:block;">Nos espaces</p>
        <h2 class="section-title" style="text-align:center;">Choisissez votre chambre</h2>
    </div>
</div>
""", unsafe_allow_html=True)

col_r1, col_r2, col_r3 = st.columns(3)
for col, (room_key, room_data) in zip([col_r1, col_r2, col_r3], CHAMBRES.items()):
    with col:
        st.markdown(f"""
        <div class="room-card">
            <img class="room-card-img" src="{room_data['img']}" alt="{room_data['nom']}" loading="lazy">
            <div class="room-card-body">
                <p class="room-floor">{room_data['etage']}</p>
                <h3 class="room-name">{room_data['nom']}</h3>
                <div class="form-divider" style="width:30px; margin:1rem 0;"></div>
                <div class="room-price">{room_data['prix']} € <span>/ mois</span></div>
                <p class="room-charges">Charges : {room_data['charges']} € · Garantie : {room_data['gar_red']} €</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# =============================================
# FORMULAIRE
# =============================================
st.markdown("""
<div class="form-section">
    <p class="section-eyebrow">Votre demande</p>
    <h2 class="section-title">Générer votre<br>contrat de location</h2>
    <div class="form-divider"></div>
    <p class="section-lead" style="margin-bottom:3rem;">
        Complétez ce formulaire pour recevoir votre contrat personnalisé en quelques secondes,
        prêt à signer au format PDF.
    </p>
</div>
""", unsafe_allow_html=True)

with st.form("contract_form"):
    st.markdown('<span class="form-step-title">✦ Informations Personnelles</span>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        gender = st.selectbox("Titre", ["M.", "Mme", "Dr."])
    with col2:
        fname = st.text_input("Prénom *")
    with col3:
        lname = st.text_input("Nom de famille *")

    col4, col5, col6 = st.columns(3)
    with col4:
        natio = st.text_input("Nationalité *")
    with col5:
        bday = st.text_input("Date de naissance *", placeholder="JJ/MM/AAAA")
    with col6:
        email = st.text_input("Adresse email *")

    st.markdown('<span class="form-step-title">✦ Détails de la Location</span>', unsafe_allow_html=True)
    
    col7, col8 = st.columns([1, 2])
    with col7:
        room = st.selectbox("Chambre souhaitée", list(CHAMBRES.keys()),
                           format_func=lambda k: f"{CHAMBRES[k]['nom']} — {CHAMBRES[k]['prix']} €/mois")
    with col8:
        st.markdown(f"""
        <div style="background:#F4F1EC; border:1px solid #E8E4DC; padding:1rem 1.3rem; margin-top:1.75rem; font-family:'Jost',sans-serif; font-size:0.82rem; color:#5A5A5A; line-height:1.7;">
            <strong style="color:#C9A96E; letter-spacing:0.1em; text-transform:uppercase; font-size:0.65rem;">Récapitulatif</strong><br>
            Loyer : <strong>{CHAMBRES[room]['prix']} €</strong> &nbsp;·&nbsp;
            Charges : <strong>{CHAMBRES[room]['charges']} €</strong> &nbsp;·&nbsp;
            Garantie locative : <strong>{CHAMBRES[room]['gar_red']} €</strong>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<span class="form-step-title">✦ Clause Particulière</span>', unsafe_allow_html=True)
    special_clause = st.text_area("Condition négociée (optionnel)",
                                   placeholder="Ex : Accès garage inclus, animal de compagnie autorisé...",
                                   height=100)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    submit = st.form_submit_button("✦  Générer mon contrat  ✦")

if submit:
    mandatory_fields = [fname, lname, natio, bday, email]
    if not all(mandatory_fields):
        st.error("Veuillez remplir tous les champs marqués d'un astérisque (*).")
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
            "special_clause": special_clause if special_clause else "Néant",
            "date_signature": datetime.now().strftime("%d/%m/%Y"),
        }

        tpl = DocxTemplate("Contrat de location - Template.docx")
        tpl.render(context)
        docx_name = f"Contrat_{lname.upper()}_{room}.docx"
        tpl.save(docx_name)

        with st.spinner("Génération du contrat sécurisé..."):
            pdf_name = convert_to_pdf(docx_name)

        st.success(f"✓  Contrat généré avec succès pour {gender} {fname} {lname.upper()}")
        
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            with open(pdf_name, "rb") as f:
                st.download_button("⬇  Télécharger le contrat PDF", f,
                                   file_name=pdf_name, mime="application/pdf")
        with col_dl2:
            with open(docx_name, "rb") as f:
                st.download_button("⬇  Télécharger le contrat Word", f,
                                   file_name=docx_name,
                                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

# =============================================
# FOOTER
# =============================================
st.markdown("""
<div class="site-footer">
    <strong>Rue de l'Orient 46</strong> &nbsp;·&nbsp; Etterbeek, 1040 Bruxelles &nbsp;·&nbsp;
    Belgique<br><br>
    <span>Contrats générés via technologie sécurisée &nbsp;·&nbsp; © 2025 — Tous droits réservés</span>
</div>
""", unsafe_allow_html=True)
