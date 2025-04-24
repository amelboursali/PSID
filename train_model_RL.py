import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

# 1. Charger les données
df = pd.read_csv("DATA_accidents_pour_ml.csv", sep=";")

# 2. Garder les colonnes utiles et nettoyer
df = df[["sexe_pieton", "Département", "Conditions atmosphériques", "Jour_semaine", "Lumière", "gravité_pieton"]]
df.dropna(inplace=True)

# 3. Encoder les colonnes catégorielles sauf la target
for col in ["sexe_pieton", "Conditions atmosphériques", "Jour_semaine", "Lumière"]:
    df[col] = df[col].astype(str).factorize()[0]

# Encoder la variable cible (gravité) avec mapping explicite
df["gravité_pieton"] = df["gravité_pieton"].astype(str)
y_labels, uniques = pd.factorize(df["gravité_pieton"])
df["gravité_pieton"] = y_labels
label_mapping = dict(enumerate(uniques))  # Exemple : {0: 'Indemne', 1: 'Blessé', 2: 'Tué'}

# 4. Séparer les variables d'entrée et la cible
X = df[["sexe_pieton", "Département", "Conditions atmosphériques", "Jour_semaine", "Lumière"]]
y = df["gravité_pieton"]

# 5. Diviser en ensemble d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Entraîner un modèle de régression logistique (multiclass, équilibré)
model = LogisticRegression(
    multi_class='multinomial',
    solver='lbfgs',
    class_weight='balanced',
    max_iter=1000,
    random_state=42
)
model.fit(X_train, y_train)

# 7. Évaluer le modèle
y_pred = model.predict(X_test)
target_names = [label_mapping[i] for i in sorted(label_mapping.keys())]

print("✅ Évaluation du modèle Logistic Regression :\n")
print("Accuracy :", accuracy_score(y_test, y_pred))
print("\nClassification Report :\n", classification_report(y_test, y_pred, target_names=target_names))
print("Matrice de confusion :\n", confusion_matrix(y_test, y_pred))

# 8. Sauvegarder le modèle
joblib.dump(model, "backend/api/ml_model_logreg.pkl")
print("\n✅ Modèle enregistré sous backend/api/ml_model_logreg.pkl")