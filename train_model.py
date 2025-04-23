import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

# 1. Charger les données
df = pd.read_csv("DATA_accidents_pour_ml.csv", sep=";")

# 2. Garder les colonnes utiles et nettoyer
df = df[["sexe_pieton", "Département", "Conditions atmosphériques", "Jour_semaine", "Lumière", "gravité_pieton"]]
df.dropna(inplace=True)

# 3. Encoder les colonnes catégorielles (sauf la cible pour garder les labels)
for col in ["sexe_pieton", "Conditions atmosphériques", "Jour_semaine", "Lumière"]:
    df[col] = df[col].astype(str).factorize()[0]

# Encoder la target avec mapping explicite
df["gravité_pieton"] = df["gravité_pieton"].astype(str)
y_labels, uniques = pd.factorize(df["gravité_pieton"])
df["gravité_pieton"] = y_labels
label_mapping = dict(enumerate(uniques))

# Affichage du mapping des classes
print("🎯 Mapping des classes gravité_pieton :")
for i, label in label_mapping.items():
    print(f"Classe {i} ➜ {label}")

# 4. Séparer les features et la target
X = df[["sexe_pieton", "Département", "Conditions atmosphériques", "Jour_semaine", "Lumière"]]
y = df["gravité_pieton"]

# 5. Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Entraînement du modèle avec class_weight équilibré
model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# 7. Évaluation
y_pred = model.predict(X_test)

# Récupérer les noms de classes dans l’ordre
target_names = [label_mapping[i] for i in sorted(label_mapping.keys())]

print("\n✅ Évaluation du modèle avec class_weight='balanced' :\n")
print("Accuracy :", accuracy_score(y_test, y_pred))
print("\nClassification Report :\n", classification_report(y_test, y_pred, target_names=target_names))
print("Matrice de confusion :\n", confusion_matrix(y_test, y_pred))

# 8. Sauvegarde du modèle
joblib.dump(model, "backend/api/ml_model.pkl")
print("\n✅ Modèle enregistré sous backend/api/ml_model.pkl")
