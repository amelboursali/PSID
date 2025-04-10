import pandas as pd

# Fonction pour corriger les caractères accentués mal encodés
def corriger_accents_foireux(texte):
    try:
        return texte.encode('latin1').decode('utf-8')
    except:
        return texte

# Étape 1 : lire les données avec encodage ISO-8859-1
df = pd.read_csv("dataset_avec_gravite_pieton.csv", sep=';', encoding='ISO-8859-1')

# Étape 2 : corriger les noms de colonnes
df.columns = [corriger_accents_foireux(col) for col in df.columns]

# Étape 3 : corriger les valeurs des colonnes texte
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].apply(corriger_accents_foireux)

# Étape 4 : conversion en datetime
df["Date et heure"] = pd.to_datetime(df["Date et heure"], utc=True, errors='coerce')

# Étape 5 : extraire le jour de la semaine
df["Jour_semaine"] = df["Date et heure"].dt.day_name()
jours_fr = {
    "Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi",
    "Thursday": "Jeudi", "Friday": "Vendredi", "Saturday": "Samedi", "Sunday": "Dimanche"
}
df["Jour_semaine"] = df["Jour_semaine"].map(jours_fr)

# Étape 6 : insérer "Jour_semaine" après la colonne "Jour"
cols = df.columns.tolist()
index_jour = cols.index("Jour")
cols.insert(index_jour + 1, cols.pop(cols.index("Jour_semaine")))
df = df[cols]

# Étape 7 : sauvegarde avec encodage compatible Excel
df.to_csv("dataset_modifie_avec_jour_semaine.csv", sep=';', index=False, encoding='utf-8-sig')

print("✅ Fichier prêt : accents OK partout, 'Jour_semaine' ajouté, compatible Excel.")
