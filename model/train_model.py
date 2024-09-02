import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

def train_and_save_model():
    # Simulación de un dataset con datos ficticios
    np.random.seed(42)

    data = {
        'Sector': np.random.choice(['Tecnología', 'Salud', 'Fintech', 'Retail', 'Energía'], 500),
        'Etapa': np.random.choice(['Idea', 'MVP', 'Producto en el mercado', 'Escalamiento'], 500),
        'Costo Operativo Mensual': np.random.uniform(10000, 100000, 500),
        'Crecimiento Mensual (%)': np.random.uniform(1, 10, 500),
        'Exito Financiamiento': np.random.choice([0, 1], 500, p=[0.4, 0.6])  # 0: No logró financiamiento, 1: Logró financiamiento
    }

    df = pd.DataFrame(data)

    # Codificación de variables categóricas
    le_sector = LabelEncoder()
    le_etapa = LabelEncoder()

    df['Sector'] = le_sector.fit_transform(df['Sector'])
    df['Etapa'] = le_etapa.fit_transform(df['Etapa'])

    # Variables independientes y dependiente
    X = df[['Sector', 'Etapa', 'Costo Operativo Mensual', 'Crecimiento Mensual (%)']]
    y = df['Exito Financiamiento']

    # Dividir los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenamiento del modelo
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluación del modelo
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy del modelo: {accuracy:.2f}")

    # Guardar el modelo y los codificadores
    with open('model/financiamiento_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    with open('model/le_sector.pkl', 'wb') as f:
        pickle.dump(le_sector, f)

    with open('model/le_etapa.pkl', 'wb') as f:
        pickle.dump(le_etapa, f)  # Aquí se eliminó el paréntesis extra

if __name__ == "__main__":
    train_and_save_model()
