import streamlit as st
import json
import os
from datetime import datetime
from docxtpl import DocxTemplate
from num2words import num2words

# --- CONFIGURATION ---
CHAMBRES = {
    "1E": {"id": "1E", "etage": "1e", "prix": 570, "charges": 30, "gar_norm": 1000, "gar_red": 600},
    "GRISE": {"id": "Grise", "etage": "deuxième", "prix": 540, "charges": 50, "gar_norm": 1080, "gar_red": 500},
    "ROUGE": {"id": "Rouge", "etage": "troisième", "prix": 550, "charges": 40, "gar_norm": 1100, "gar_red": 550}
}
FILE_REF = "ref_counter.json"

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

# --- INTERFACE LOCATAIRE (ANGLAIS) ---
st.set_page_config(page_title="Etterbeek Rental Form", page_icon="🏠")
st.title("Rental Information Form")
st.info("The official contract is in French. This form collects your data in English for processing.")

with st.form("main_form"):
    st.subheader("1. Identity")
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Title", ["Mr.", "Ms."])
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
    with col2:
        natio = st.text_input("Nationality")
        bday = st.text_input("Birth Date (DD/MM/YYYY)")
        bplace = st.text_input("Place of Birth")

    st.subheader("2. Contact & ID")
    addr = st.text_area("Current Permanent Address")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    id_type = st.selectbox("ID Type", ["Identity Card", "Passport"])
    id_num = st.text_input("ID Number")

    st.subheader("3. Lease info")
    room = st.selectbox("Room", ["1E", "GRISE", "ROUGE"])
    start = st.date_input("Start Date")
    end = st.date_input("End Date")

    submit = st.form_submit_button("Generate Draft Contract")

if submit:
    ch = CHAMBRES[room]
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
        "chambre_desc": f"chambre meublée (dite 'chambre {room.lower()}')" if room != "1E" else "chambre au 1e étage",
        "etage": ch["etage"],
        "debut_bail": start.strftime("%d/%m/%Y"),
        "fin_bail": end.strftime("%d/%m/%Y"),
        "loyer_total": format_prix(ch["prix"]),
        "charges": format_prix(ch["charges"]),
        "total_mensuel": f"{ch['prix'] + ch['charges']} €",
        "garantie_normale": format_prix(ch["gar_norm"]),
        "garantie_reduite": format_prix(ch["gar_red"]),
        "prix_invite": "cinquante euros (50 euros)",
        "forfait_nettoyage": "soixante-dix euro (70 euro)",
        "pot_commun": "Cinq euro (5 euro)",
        "date_signature": datetime.now().strftime("%d/%m/%Y")
    }

    doc = DocxTemplate("Contrat de location - Template.docx")
    doc.render(context)
    
    # Nom de fichier : Prix - Chambre - Contrat - Nom Prenom Date.docx
    f_name = f"{ch['prix']} - {room} - Contrat - {lname.upper()} {fname} {start.strftime('%d%m%y')}.docx"
    doc.save(f_name)
    
    st.success("✅ Information received!")
    with open(f_name, "rb") as f:
        st.download_button("📥 Download your draft contract", f, file_name=f_name)