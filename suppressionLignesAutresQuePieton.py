import pandas as pd

# Charger le fichier contenant la colonne 'gravité_pieton'
df = pd.read_csv("dataset_modifie_avec_jour_semaine.csv", sep=';', encoding='utf-8-sig')

# Supprimer les lignes où la gravité piéton est exactement égale à 0
df = df[df["gravité_pieton"] != "0"]

# Sauvegarder le fichier filtré
df.to_csv("dataset_sans_gravite_pieton_0.csv", sep=';', index=False, encoding='utf-8-sig')

print("✅ Lignes avec gravité_pieton = 0 supprimées. Fichier : 'dataset_sans_gravite_pieton_0.csv'")
