import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE


# Charger le fichier CSV
data = pd.read_csv('DATA_accidents-corporels-de-la-circulation-millesime.csv', sep=';')

# Afficher les premières lignes
print(data.head())

# Supprimer les colonnes inutiles
data = data.drop(columns=["Identifiant de l'accident", "Date et heure", "Adresse", "Code Postal", "Nom Officiel Département", "Nom Officiel Région"])

# Gérer les valeurs manquantes
data = data.dropna()

# Encoder la colonne 'Gravité' pour conserver toutes les classes
label_encoder = LabelEncoder()
data['Gravité'] = label_encoder.fit_transform(data['Gravité'])

# Vérifier la distribution des classes après encodage
print("Distribution des classes après encodage :")
print(data['Gravité'].value_counts())

# Supprimer les classes avec moins de 5 échantillons
class_counts = data['Gravité'].value_counts()
valid_classes = class_counts[class_counts >= 5].index
data = data[data['Gravité'].isin(valid_classes)]

# Vérifier la distribution après suppression des classes rares
print("Distribution des classes après suppression des classes rares :")
print(data['Gravité'].value_counts())

# Encoder les colonnes catégorielles avec LabelEncoder
categorical_columns = data.select_dtypes(include=['object']).columns

# Afficher les colonnes catégorielles et leur nombre
print(f"Colonnes catégorielles encodées : {list(categorical_columns)}")
print(f"Nombre de colonnes catégorielles encodées : {len(categorical_columns)}")

# Appliquer le LabelEncoder à chaque colonne catégorielle
for col in categorical_columns:
    data[col] = label_encoder.fit_transform(data[col])

# Séparer les caractéristiques et la cible
X = data.drop('Gravité', axis=1)
y = data['Gravité']

# Appliquer SMOTE pour équilibrer les classes avec k_neighbors=1
smote = SMOTE(random_state=42, k_neighbors=1)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Vérifier la distribution des classes après SMOTE
print("Distribution des classes après SMOTE :")
print(pd.Series(y_resampled).value_counts())

# Diviser les données équilibrées en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Initialiser le modèle
model = DecisionTreeClassifier(class_weight='balanced')

# Entraîner le modèle
model.fit(X_train, y_train)

# Prédire sur l'ensemble de test
y_pred = model.predict(X_test)

# Évaluer la précision
accuracy = accuracy_score(y_test, y_pred)
print(f'Précision : {accuracy}')

# Rapport de classification
print(classification_report(y_test, y_pred))

# Sauvegarder le modèle
joblib.dump(model, 'accident_model.pkl')
