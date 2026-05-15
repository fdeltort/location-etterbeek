import streamlit as st
import os
import subprocess
import json
import smtplib
from email.message import EmailMessage
from docxtpl import DocxTemplate
from datetime import datetime
from num2words import num2words

# --- CONFIGURATION STYLE "LE COLLECTIONIST" ---
st.set_page_config(page_title="46 Rue de l'Orient", layout="centered")

# CSS : Forçage du mode clair, polices Serif et design épuré
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lato:wght@300;400&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        font-family: 'Lato', sans-serif;
    }
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 42px;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-title {
        font-family: 'Lato', sans-serif;
        font-weight: 300;
        text-align: center;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-size: 14px;
        margin-bottom: 40px;
    }
    h3, h4 {
        font-family: 'Playfair Display', serif;
        font-weight: 400;
        border-bottom: 1px solid #EEE;
        padding-bottom: 10px;
        margin-top: 30px;
    }
    .stButton>button {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border-radius: 0px !important;
        border: none !important;
        width: 100%;
        padding: 15px !important;
        font-family: 'Playfair Display', serif !important;
        letter-spacing: 2px !important;
        margin-top: 20px;
    }
    /* Fix pour l'image qui ne s'affiche pas */
    .header-img {
        width: 100%;
        height: 400px;
        object-fit: cover;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE MÉTIER ---
CHAMBRES = {
    "1E": {"id": "1E", "etage": "1e", "prix": 570, "charges": 30, "gar_norm": 1000, "gar_red": 600},
    "GRISE": {"id": "Grise", "etage": "deuxième", "prix": 540, "charges": 50, "gar_norm": 1080, "gar_red": 500},
    "ROUGE": {"id": "Rouge", "etage": "troisième", "prix": 550, "charges": 40, "gar_norm": 1100, "gar_red": 550}
}

def format_prix(n):
    return f"{num2words(n, lang='fr')} euro ({n} euro)"

def convert_to_pdf(docx_path):
    # Commande LibreOffice pour Streamlit Cloud (via packages.txt)
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_path])
    return docx_path.replace(".docx", ".pdf")

def get_next_ref():
    file_ref = "ref_counter.json"
    year = str(datetime.now().year)
    if os.path.exists(file_ref):
        with open(file_ref, "r") as f: data = json.load(f)
    else: data = {"year": year, "count": 0}
    if data["year"] != year: data = {"year": year, "count": 1}
    else: data["count"] += 1
    with open(file_ref, "w") as f: json.dump(data, f)
    return f"{year}-{data['count']}"

# --- INTERFACE ---
# Image de Bruxelles ou de la maison
st.markdown('<img src="https://images.unsplash.com/photo-1563124417-6803861d0729?auto=format&fit=crop&q=80&w=1200" class="header-img">', unsafe_allow_html=True)

st.markdown('<div class="main-title">Rue de l’Orient 46</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Etterbeek, Brussels — Guest Experience</div>', unsafe_allow_html=True)

st.write("""
Welcome to our home. We aim to create a calm, respectful, and family-like environment. 
Please complete this form to finalize your rental application.
""")

# Récupération automatique de la clause via URL si présente
query_params = st.query_params
default_clause = query_params.get("clause", "")

with st.form("lease_form"):
    st.subheader("Tenant Identity")
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Title", ["Mr.", "Ms."])
        fname = st.text_input("First Name *")
        lname = st.text_input("Last Name *")
        natio = st.text_input("Nationality *")
    with col2:
        bday = st.text_input("Date of Birth (DD/MM/YYYY) *")
        bplace = st.text_input("Place of Birth *")
        email = st.text_input("Email Address *")
        phone = st.text_input("Phone Number")

    st.subheader("Documentation")
    addr = st.text_area("Permanent Address (Home Country) *")
    id_type = st.selectbox("ID Document", ["Passport", "Identity Card"])
    id_num = st.text_input("Document Number *")

    st.subheader("Lease Period & Selection")
    col3, col4 = st.columns(2)
    with col3:
        room_choice = st.selectbox("Selected Room", ["1E", "GRISE", "ROUGE"])
        start_date = st.date_input("Lease Start Date")
    with col4:
        end_date = st.date_input("Lease End Date")

    special_clause = st.text_area("Special Conditions (Agreed with Landlord)", value=default_clause)
    
    st.write("---")
    submit = st.form_submit_button("VALIDATE & GENERATE PDF")

if submit:
    # Validation des champs obligatoires
    mandatory = [fname, lname, natio, bday, bplace, email, addr, id_num]
    if not all(mandatory):
        st.error("Please fill in all fields marked with *")
    else:
        ch = CHAMBRES[room_choice]
        is_f = (gender == "Ms.")
        
        context = {
            "reference_contrat": get_next_ref(),
            "titre_civil": "Mme" if is_f else "M.",
            "prenom": fname,
            "nom": lname.upper(),
            "adresse_actuelle": addr,
            "date_naissance": bday,
            "lieu_naissance": bplace,
            "nationalite": natio,
            "telephone": phone,
            "email": email,
            "id_type": id_type,
            "id_numero": id_num,
            "pronom_refl": "elle-même" if is_f else "lui-même",
            "preneur_accord": "La preneuse" if is_f else "Le preneur",
            "accord_e": "e" if is_f else "",
            "chambre_desc": f"chambre meublée dite '{room_choice.lower()}'" if room_choice != "1E" else "chambre au 1e étage",
            "etage": ch["etage"],
            "debut_bail": start_date.strftime("%d/%m/%Y"),
            "fin_bail": end_date.strftime("%d/%m/%Y"),
            "loyer_total": format_prix(ch["prix"]),
            "charges": format_prix(ch["charges"]),
            "total_mensuel": f"{ch['prix'] + ch['charges']} €",
            "garantie_normale": format_prix(ch["gar_norm"]),
            "garantie_reduite": format_prix(ch["gar_red"]),
            "special_clause": special_clause if special_clause else "Néant",
            "date_signature": datetime.now().strftime("%d %B %Y"),
            "prix_invite": "cinquante euros (50 euros)",
            "forfait_nettoyage": "soixante-dix euro (70 euro)",
            "pot_commun": "Cinq euro (5 euro)"
        }

        # Génération Word
        doc = DocxTemplate("Contrat de location - Template.docx")
        doc.render(context)
        docx_name = f"Contract_{lname}.docx"
        doc.save(docx_name)
        
        # Conversion PDF
        with st.spinner("Securing document..."):
            pdf_name = convert_to_pdf(docx_name)
        
        st.success("Your contract has been generated successfully.")
        
        with open(pdf_name, "rb") as f:
            st.download_button("Download Secure PDF", f, file_name=pdf_name)
            
        # Envoi Email Invisible
        try:
            msg = EmailMessage()
            msg['Subject'] = f"New Lease Request: {fname} {lname}"
            msg['From'] = st.secrets["EMAIL_USER"]
            msg['To'] = st.secrets["EMAIL_RECEIVER"]
            msg.set_content(f"Tenant: {fname} {lname}\nRoom: {room_choice}\nClause: {special_clause}")
            with open(pdf_name, 'rb') as fp:
                msg.add_attachment(fp.read(), maintype='application', subtype='pdf', filename=pdf_name)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(st.secrets["EMAIL_USER"], st.secrets["EMAIL_PASS"])
                smtp.send_message(msg)
        except:
            pass