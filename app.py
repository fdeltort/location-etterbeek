import streamlit as st
import os
import subprocess
from docxtpl import DocxTemplate
from datetime import datetime
from num2words import num2words

# --- CONFIGURATION STYLE "LE COLLECTIONIST" ---
st.set_page_config(page_title="Rue de l'Orient 46", page_icon="✨", layout="wide")

# CSS pour forcer le mode clair et un style élégant (Serif fonts, blanc pur)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lato:wght@300;400&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF;
        color: #1A1A1A;
        font-family: 'Lato', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #1A1A1A;
        letter-spacing: 0.05em;
    }
    .stButton>button {
        background-color: #1A1A1A;
        color: white;
        border-radius: 0px;
        padding: 1rem 2rem;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #444444;
        color: white;
    }
    /* Cacher le menu Streamlit pour faire "vrai site" */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE MÉTIER ---
CHAMBRES = {
    "1E": {"prix": 570, "charges": 30, "gar_red": 600, "etage": "1e"},
    "GRISE": {"prix": 540, "charges": 50, "gar_red": 500, "etage": "deuxième"},
    "ROUGE": {"prix": 550, "charges": 40, "gar_red": 550, "etage": "troisième"}
}

def convert_to_pdf(docx_path):
    # Utilise LibreOffice installé via packages.txt
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_path])
    return docx_path.replace(".docx", ".pdf")

# --- INTERFACE ---
# Vidéo de fond ou Grande image élégante
# Astuce : Pour une vidéo, utilise une URL directe .mp4
video_url = "https://www.w3schools.com/html/mov_bbb.mp4" # Remplace par une belle vue de Bruxelles
st.video(video_url, format="video/mp4", start_time=0, loop=True, autoplay=True, muted=True)

st.title("Bienvenue Rue de l'Orient 46")
st.write("L'élégance et le calme au cœur d'Etterbeek.")

with st.form("contract_form"):
    st.subheader("Informations Personnelles")
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Titre", ["M.", "Mme"])
        fname = st.text_input("Prénom *")
        lname = st.text_input("Nom *")
    with col2:
        natio = st.text_input("Nationalité *")
        bday = st.text_input("Date de naissance (JJ/MM/AAAA) *")
        email = st.text_input("Email *")

    st.subheader("Détails de la Location")
    room = st.selectbox("Chambre", ["1E", "GRISE", "ROUGE"])
    
    # --- CLAUSE PARTICULIÈRE ---
    special_clause = st.text_area("Clause particulière (optionnel)", 
                                 help="Ajoutez ici une condition spécifique négociée.")

    submit = st.form_submit_button("VALIDER MA DEMANDE")

if submit:
    # --- VALIDATION DES CHAMPS ---
    mandatory_fields = [fname, lname, natio, bday, email]
    if not all(mandatory_fields):
        st.error("Veuillez remplir tous les champs marqués d'une astérisque (*).")
    else:
        # Génération du dictionnaire (context)
        ch = CHAMBRES[room]
        context = {
            "prenom": fname, "nom": lname.upper(), "nationalite": natio,
            "loyer_total": f"{num2words(ch['prix'], lang='fr')} euros ({ch['prix']} €)",
            "special_clause": special_clause if special_clause else "Néant",
            # ... ajoute ici toutes tes autres variables habituelles
        }

        # 1. Créer le Word
        tpl = DocxTemplate("Contrat de location - Template.docx")
        tpl.render(context)
        docx_name = f"Contrat_{lname}.docx"
        tpl.save(docx_name)

        # 2. Convertir en PDF
        with st.spinner("Génération du contrat sécurisé..."):
            pdf_name = convert_to_pdf(docx_name)
        
        st.success("Votre contrat est prêt.")
        with open(pdf_name, "rb") as f:
            st.download_button("Télécharger le Contrat (PDF)", f, file_name=pdf_name)