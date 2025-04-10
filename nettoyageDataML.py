import pandas as pd
from collections import Counter

# Chargement du fichier CSV avec le séparateur ;
df = pd.read_csv("DATA_accidents-corporels-de-la-circulation-millesime.csv", sep=';', encoding='utf-8', low_memory=False)

# Nettoyage de la colonne "Gravité"
df['Gravité'] = df['Gravité'].fillna('')
df['Gravité_list'] = df['Gravité'].apply(lambda x: [g.strip() for g in x.split(',') if g.strip() != ''])

# Identification de toutes les classes uniques dans la colonne Gravité
all_classes = Counter([item for sublist in df['Gravité_list'] for item in sublist])
classes_uniques = list(all_classes.keys())

# Création d'une colonne pour chaque classe
for classe in classes_uniques:
    df[f'Gravité_{classe}'] = df['Gravité_list'].apply(lambda gravs: gravs.count(classe))

# Réorganiser les colonnes pour placer les nouvelles à côté de "Gravité"
colonnes = list(df.columns)
index_gravite = colonnes.index('Gravité')
new_cols = [f'Gravité_{classe}' for classe in classes_uniques]

# Supprimer les colonnes nouvellement créées de la liste originale (elles sont ajoutées après)
for col in new_cols:
    colonnes.remove(col)

# Insérer les nouvelles colonnes juste après "Gravité"
colonnes = colonnes[:index_gravite + 1] + new_cols + colonnes[index_gravite + 1:]

# Réorganiser le DataFrame
df = df[colonnes]

# Sauvegarde dans un nouveau fichier CSV avec ; comme séparateur
df.to_csv("DATA_accidents_pour_ml.csv", index=False, sep=';', encoding='utf-8-sig')

# Charger le fichier enrichi avec les colonnes de gravité
df = pd.read_csv("DATA_accidents_pour_ml.csv", sep=';', encoding='utf-8')

# Nettoyage
df['Catégorie véhicule'] = df['Catégorie véhicule'].fillna('')
df['Vehicules_list'] = df['Catégorie véhicule'].apply(lambda x: [v.strip() for v in x.split(',') if v.strip() != ''])

# Fonction pour classer chaque type
def regrouper_vehicule(vehicules):
    voiture = 0
    pieton = 0
    deux_roues = 0
    camion = 0
    for v in vehicules:
        v = v.lower()
        if 'piéton' in v:
            pieton += 1
        elif 'vl' in v or 'voiture' in v:
            voiture += 1
        elif 'scooter' in v or 'moto' in v or 'cyclomoteur' in v or 'vélo' in v:
            deux_roues += 1
        elif 'pl' in v or 'utilitaire' in v or 'camion' in v or 'camionnette' in v:
            camion += 1
    return pd.Series([voiture, pieton, deux_roues, camion])

# Application du regroupement
df[['Nb_Voiture', 'Nb_Pieton', 'Nb_2Roues', 'Nb_Camion']] = df['Vehicules_list'].apply(regrouper_vehicule)

# Réorganisation des colonnes (juste après "Catégorie véhicule")
index_vehicule = df.columns.get_loc('Catégorie véhicule')
new_cols = ['Nb_Voiture', 'Nb_Pieton', 'Nb_2Roues', 'Nb_Camion']
cols = list(df.columns)
for col in new_cols:
    cols.remove(col)
cols = cols[:index_vehicule + 1] + new_cols + cols[index_vehicule + 1:]
df = df[cols]

# Sauvegarde du fichier final
df.to_csv("DATA_accidents_pour_ml.csv", index=False, sep=';', encoding='utf-8-sig')