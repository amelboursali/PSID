import pandas as pd

# Charger le fichier contenant la colonne 'gravité_pieton'
df = pd.read_csv("DATA_accidents_pour_ml.csv", sep=';', encoding='utf-8-sig')

# Supprimer les lignes où la gravité piéton est exactement égale à 0
df = df[df["gravité_pieton"] != "0"]

# Sauvegarder le fichier filtré
df.to_csv("DATA_accidents_pour_ml.csv", sep=';', index=False, encoding='utf-8-sig')

print("✅ Lignes avec gravité_pieton = 0 supprimées. Fichier : 'dataset_sans_gravite_pieton_0.csv'")


# Chargement du fichier
df = pd.read_csv("DATA_accidents_pour_ml.csv", sep=';', encoding='utf-8', low_memory=False)

# Fonction pour retourner le sexe au format texte
def normaliser_sexe(sexe):
    sexe = sexe.strip().lower()
    if sexe == 'masculin':
        return 'Masculin'
    elif sexe == 'féminin':
        return 'Féminin'
    else:
        return 'Inconnu'

# Fonction pour extraire le sexe du premier piéton trouvé
def extraire_sexe_pieton(row):
    try:
        usagers = str(row["Catégorie d'usager"]).split(',')
        sexes = str(row["Sexe"]).split(',')

        for i, usager in enumerate(usagers):
            if usager.strip().lower() == 'piéton':
                if i < len(sexes):
                    return normaliser_sexe(sexes[i])
                else:
                    return 'Inconnu'
        return 0  # Aucun piéton
    except:
        return 0  # Erreur ou données incomplètes

# Application
df['sexe_pieton'] = df.apply(extraire_sexe_pieton, axis=1)

# Export avec accents gérés pour Excel
df.to_csv("DATA_accidents_pour_ml.csv", index=False, sep=';', encoding='utf-8-sig')

print("✅ Colonne 'sexe_pieton' ajoutée avec succès (une seule valeur ou 0 si aucun piéton).")
