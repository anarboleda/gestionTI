from model.business_logic import BusinessLogic
from view.main_view import MainView
from model.ai_model import AIModel

class MainController:
    def __init__(self):
        self.view = MainView(self)
        self.data = {}
        self.ai_model = AIModel()

    def obtener_datos(self):
        self.data = {
            "nombre": self.view.nombre_var.get(),
            "sector": self.view.sector_var.get(),
            "etapa": self.view.etapa_var.get(),
            "mision": self.view.mision_var.get(),
            "costo_operativo_mensual": self.view.costo_operativo_var.get(),
            "crecimiento": self.view.crecimiento_var.get()
        }

    def estimar_capital(self):
        self.obtener_datos()
        logic = BusinessLogic(self.data)
        capital, df_resultados = logic.estimar_capital()

        # Usar el modelo de IA para predecir el éxito de financiamiento
        prediccion, probabilidad = self.ai_model.predecir(
            self.data["sector"],
            self.data["etapa"],
            self.data["costo_operativo_mensual"],
            self.data["crecimiento"]
        )

        exito = "alta" if prediccion == 1 else "baja"
        self.view.mostrar_resultado(capital, df_resultados)
        self.view.resultado_label.config(text=f"{self.view.resultado_label.cget('text')}\n\nSegún el modelo de IA, hay una {exito} probabilidad de obtener financiamiento (Probabilidad: {probabilidad:.2f}).")

    def obtener_recomendaciones(self):
        logic = BusinessLogic(self.data)
        return logic.obtener_recomendaciones()

    def iniciar(self):
        self.view.mainloop()
