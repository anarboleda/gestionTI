import numpy as np
import pandas as pd

class BusinessLogic:
    def __init__(self, data):
        self.data = data
    
    def estimar_capital(self):
        meses = 12  # Se considera un año de operaciones
        crecimiento_proyectado = 1 + (self.data["crecimiento"] / 100)

        # Ajuste de costo operativo según el sector
        if self.data["sector"] == "Tecnología":
            factor_sector = 1.2
        elif self.data["sector"] == "Salud":
            factor_sector = 1.3
        elif self.data["sector"] == "Fintech":
            factor_sector = 1.1
        elif self.data["sector"] == "Retail":
            factor_sector = 1.15
        elif self.data["sector"] == "Energía":
            factor_sector = 1.25
        else:
            factor_sector = 1.0

        # Ajuste de costo operativo según la etapa
        if self.data["etapa"] == "Idea":
            factor_etapa = 0.8
        elif self.data["etapa"] == "MVP":
            factor_etapa = 1.0
        elif self.data["etapa"] == "Producto en el mercado":
            factor_etapa = 1.2
        elif self.data["etapa"] == "Escalamiento":
            factor_etapa = 1.5
        else:
            factor_etapa = 1.0

        # Cálculo del capital necesario
        capital_necesario = 0
        costo_mensual = self.data["costo_operativo_mensual"] * factor_sector * factor_etapa
        proyeccion_costos = []

        for mes in range(1, meses + 1):
            capital_necesario += costo_mensual
            proyeccion_costos.append({"Mes": mes, "Costo Operativo Mensual": costo_mensual})
            costo_mensual *= crecimiento_proyectado

        df_resultados = pd.DataFrame(proyeccion_costos)
        return capital_necesario, df_resultados

    def obtener_recomendaciones(self):
        # Aquí puedes incluir lógica para proporcionar recomendaciones basadas en el sector y etapa
        # Por simplicidad, devolveré un texto estático, pero podrías ampliar esto para obtener datos de sitios web
        if self.data["sector"] == "Tecnología":
            return "Para startups de tecnología, considera acercarte a fondos de venture capital especializados en tech. Busca en sitios como Crunchbase, AngelList, y TechCrunch para identificar potenciales inversores."
        elif self.data["sector"] == "Salud":
            return "Las startups de salud pueden beneficiarse de programas de aceleración especializados en biotecnología o tecnología médica. Consulta sitios como BioPharmaDive y MedTech Innovator."
        elif self.data["sector"] == "Fintech":
            return "Para fintech, los fondos y aceleradoras como Y Combinator, 500 Startups, y Techstars pueden ser buenas opciones. Explora también plataformas como Finextra."
        elif self.data["sector"] == "Retail":
            return "Las startups en retail pueden explorar asociaciones estratégicas y financiamiento en sitios como RetailDive o consultoras especializadas."
        elif self.data["sector"] == "Energía":
            return "En el sector de energía, considera buscar fondos que apoyen la transición energética. Visita Cleantech Group o consulta la red de inversores de energía renovable."
        else:
            return "Consulta sitios como AngelList, Crunchbase, o busca programas de aceleración que se alineen con tu industria."
