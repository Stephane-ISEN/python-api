import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

URL_API = "http://127.0.0.1:8081/api"

st.title("📚 Suivi des étudiants")

tab1, tab2 = st.tabs(["🎓 Étudiants", "📊 Analyse des notes"])

# ----------------------------
# Onglet 1 : Liste des étudiants
# ----------------------------

with tab1:
    # 1. Récupérer tous les étudiants
    response = requests.get(f"{URL_API}/etudiants/noms")
    if response.status_code == 200:
        etudiants = response.json()
    else:
        st.error("Impossible de récupérer la liste des étudiants.")
        st.stop()

    # 2. Liste déroulante avec tous les noms
    options = {f"{e['nom']} {e['prenom']}": e["id"] for e in etudiants}
    choix = st.selectbox("Choisissez un étudiant :", list(options.keys()))

    if choix:
        id_etudiant = options[choix]

        # 3. Afficher les infos de l’étudiant
        res = requests.get(f"{URL_API}/etudiants/{id_etudiant}")
        if res.status_code == 200:
            etu = res.json()
            st.subheader("Informations")
            st.info(f"👤 {etu['prenom']} {etu['nom']}\n\n"
                    f"🎂 Âge : {etu['age']}\n\n"
                    f"🏫 Classe : {etu['classe']}")
        else:
            st.error("Impossible de récupérer les infos de l’étudiant.")
        
        # 4. Afficher les notes
        res_notes = requests.get(f"{URL_API}/etudiants/{id_etudiant}/notes")
        if res_notes.status_code == 200:
            notes_data = res_notes.json()
            notes = notes_data.get("notes", [])
            moyenne = notes_data.get("moyenne")
            
            if notes:
                df = pd.DataFrame(notes)
                st.subheader("📊 Notes")
                st.table(df)
                st.success(f"⭐ Moyenne générale : {moyenne}/20")
            else:
                st.warning("Aucune note enregistrée.")
        
# ----------------------------
# Onglet 2 : Analyse des notes
# ----------------------------
with tab2:
    st.subheader("Toutes les notes par matière")

    res = requests.get(f"{URL_API}/notes")
    if res.status_code == 200:
        notes = res.json()
        df = pd.DataFrame(notes)

        if not df.empty:
            # Tableau global
            st.dataframe(df)

            # Moyennes par étudiant
            moyennes_etudiants = df.groupby("nom")["note"].mean().reset_index()

            # Moyenne de la classe
            moyenne_classe = df["note"].mean()

            st.write(f"⭐ Moyenne générale de la classe : **{round(moyenne_classe,2)} / 20**")

            # Histogramme
            fig, ax = plt.subplots()
            ax.bar(moyennes_etudiants["nom"], moyennes_etudiants["note"], label="Moyenne étudiant")
            ax.axhline(moyenne_classe, color="red", linestyle="--", label="Moyenne de classe")
            ax.set_ylabel("Note / 20")
            ax.set_title("Comparaison des moyennes par étudiant")
            ax.legend()
            st.pyplot(fig)
        else:
            st.warning("Aucune note enregistrée pour la classe.")
    else:
        st.error("Impossible de récupérer les notes.")
