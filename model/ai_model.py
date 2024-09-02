import pickle
import numpy as np

class AIModel:
    def __init__(self):
        # Cargar el modelo y los codificadores
        with open('model/financiamiento_model.pkl', 'rb') as f:
            self.model = pickle.load(f)

        with open('model/le_sector.pkl', 'rb') as f:
            self.le_sector = pickle.load(f)

        with open('model/le_etapa.pkl', 'rb') as f:
            self.le_etapa = pickle.load(f)

    def predecir(self, sector, etapa, costo_operativo, crecimiento):
        # Codificación de variables categóricas
        sector_encoded = self.le_sector.transform([sector])[0]
        etapa_encoded = self.le_etapa.transform([etapa])[0]

        # Crear el array de entrada
        input_data = np.array([[sector_encoded, etapa_encoded, costo_operativo, crecimiento]])

        # Hacer la predicción
        prediccion = self.model.predict(input_data)
        probabilidad = self.model.predict_proba(input_data)[0][1]  # Probabilidad de éxito

        return prediccion[0], probabilidad
