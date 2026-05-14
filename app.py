import streamlit as st
import json
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
from docxtpl import DocxTemplate
from num2words import num2words

# --- CONFIGURATION DES CHAMBRES ---
# Basé sur vos tarifs et le template fourni
CHAMBRES = {
    "1E": {"id": "1E", "etage": "1e", "prix": 570, "charges": 30, "gar_norm": 1000, "gar_red": 600},
    "GRISE": {"id": "Grise", "etage": "deuxième", "prix": 540, "charges": 50, "gar_norm": 1080, "gar_red": 500},
    "ROUGE": {"id": "Rouge", "etage": "troisième", "prix": 550, "charges": 40, "gar_norm": 1100, "gar_red": 550}
}
FILE_REF = "reference_counter.json"

# --- LOGIQUE DE RÉFÉRENCE YYYY-N (Pas de 01) ---
def get_next_ref():
    year = str(datetime.now().year)
    if os.path.exists(FILE_REF):
        with open(FILE_REF, "r") as f: data = json.load(f)
    else: data = {"year": year, "count": 0}
    
    if data["year"] != year: data = {"year": year, "count": 1}
    else: data["count"] += 1
    
    with open(FILE_REF, "w") as f: json.dump(data, f)
    return f"{year}-{data['count']}"

def format_prix(n):
    return f"{num2words(n, lang='fr')} euro ({n} euro)"

# --- FONCTION D'ENVOI D'EMAIL SÉCURISÉ ---
def send_email_to_landlord(file_path, tenant_name):
    try:
        msg = EmailMessage()
        msg['Subject'] = f"New Rental Agreement Draft: {tenant_name}"
        msg['From'] = st.secrets["EMAIL_USER"]
        msg['To'] = st.secrets["EMAIL_RECEIVER"]
        msg.set_content(f"Hello Flavien,\n\nA new tenant ({tenant_name}) has completed the online form for Rue de l'Orient 46.\n\nPlease find the generated contract attached for your validation.")

        with open(file_path, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_path)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(st.secrets["EMAIL_USER"], st.secrets["EMAIL_PASS"])
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Email error: {e}")
        return False

# --- INTERFACE UTILISATEUR (DESIGN LOCATION PRO) ---
st.set_page_config(page_title="Rue de l'Orient 46 - Welcome Home", page_icon="☀️", layout="centered")

# Image ensoleillée de Bruxelles (Cinquantenaire)
st.image("https://images.unsplash.com/photo-1563124417-6803861d0729?auto=format&fit=crop&q=80&w=1200", use_column_width=True)

st.title("Welcome to Rue de l’Orient! 🏡")

# Mot de bienvenue
st.markdown("""
We are happy to welcome you to this friendly and vibrant neighborhood, ideally located close to the European institutions. 
Nearby, you can enjoy a drink at **Place Jourdan**, do your groceries at Lidl or Colruyt, or go for a run in one of the beautiful parks around the house: **Parc Louis Hap, Parc Léopold, or Parc du Cinquantenaire**.

The house is owner-managed and offers three bedrooms. We aim to create a calm, respectful, and family-like environment. **This is not a party house.** We value peace and quiet, and we expect everyone to respect this atmosphere.

We are a non-smoking home, and we all make an effort to keep the common areas clean and pleasant for everyone. We also believe in mutual respect and helping each other when needed.

We hope you will feel comfortable and at home here very quickly.  
**Welcome!**
""")

st.write("---")
st.subheader("📋 Rental Application Form")
st.info("Please complete this form in English. Your official contract will be generated in French.")

with st.form("lease_form"):
    st.markdown("#### 👤 1. Tenant Identity")
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Title", ["Mr.", "Ms."])
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
    with col2:
        natio = st.text_input("Nationality")
        bday = st.text_input("Date of Birth (DD/MM/YYYY)")
        bplace = st.text_input("Place of Birth")

    st.markdown("#### 📍 2. Contact & Address")
    addr = st.text_area("Current Permanent Address (Home country)")
    col3, col4 = st.columns(2)
    with col3:
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
    with col4:
        id_type = st.selectbox("ID Document", ["Identity Card", "Passport"])
        id_num = st.text_input("ID Number")
    
    st.markdown("#### 🏠 3. Lease Terms")
    col5, col6 = st.columns(2)
    with col5:
        room_choice = st.selectbox("Selected Room", ["1E", "GRISE", "ROUGE"])
        start_date = st.date_input("Lease Start Date")
    with col6:
        end_date = st.date_input("Lease End Date")

    submit = st.form_submit_button("Submit & Generate Contract")

if submit:
    if not fname or not lname or not email:
        st.error("Please fill in all required fields.")
    else:
        ch = CHAMBRES[room_choice]
        is_f = (gender == "Ms.")
        
        # Préparation du dictionnaire pour le Word [cite: 204-306]
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
            "chambre_desc": f"chambre meublée (dite 'chambre {room_choice.lower()}')" if room_choice != "1E" else "chambre au 1e étage",
            "etage": ch["etage"],
            "debut_bail": start_date.strftime("%d/%m/%Y"),
            "fin_bail": end_date.strftime("%d/%m/%Y"),
            "loyer_total": format_prix(ch["prix"]),
            "charges": format_prix(ch["charges"]),
            "total_mensuel": f"{ch['prix'] + ch['charges']} €",
            "garantie_normale": format_prix(ch["gar_norm"]),
            "garantie_reduite": format_prix(ch["gar_red"]),
            "prix_invite": "cinquante euros (50 euros)",
            "forfait_nettoyage": "soixante-dix euro (70 euro)",
            "pot_commun": "Cinq euro (5 euro)",
            "date_signature": datetime.now().strftime("%d %B %Y")
        }

        # Génération du document Word
        doc = DocxTemplate("Contrat de location - Template.docx")
        doc.render(context)
        
        # Nom de fichier demandé [cite: 102]
        f_name = f"{ch['prix']} - {ch['id']} - Contrat de location - {fname} {lname.upper()} {start_date.strftime('%d%m%y')} au {end_date.strftime('%d%m%y')}.docx"
        doc.save(f_name)
        
        # Envoi invisible à ton mail perso
        email_sent = send_email_to_landlord(f_name, f"{fname} {lname}")
        
        st.balloons()
        st.success("✨ **Thank you!** Your information has been sent to the landlord.")
        st.write("You can download a draft copy of your contract below for your records.")
        
        with open(f_name, "rb") as file:
            st.download_button(label="📥 Download Draft Contract", data=file, file_name=f_name)
        
        st.warning("Next step: The landlord will review your application and contact you for the final signing.")