import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Asistente de Financiamiento para Startups")
        self.geometry("600x800")

        # Añadir un contenedor para la barra de desplazamiento
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Añadir una barra de desplazamiento
        self.canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Sección explicativa
        tk.Label(self.scrollable_frame, text="Bienvenido al Asistente de Financiamiento para Startups", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.scrollable_frame, text="Complete los campos a continuación para estimar el capital necesario para su startup.\nElija el sector adecuado y proporcione las métricas financieras correctas.", wraplength=500).pack(pady=10)

        # Botón de Ayuda
        tk.Button(self.scrollable_frame, text="Ayuda", command=self.mostrar_ayuda).pack(pady=10)

        # Inputs para la información básica
        tk.Label(self.scrollable_frame, text="Nombre de la Empresa").pack()
        self.nombre_var = tk.StringVar()
        tk.Entry(self.scrollable_frame, textvariable=self.nombre_var).pack()

        tk.Label(self.scrollable_frame, text="Industria o Sector").pack()
        self.sector_var = tk.StringVar()
        self.sector_var.set("Tecnología")  # Valor por defecto
        opciones_sector = ["Tecnología", "Salud", "Fintech", "Retail", "Energía"]
        tk.OptionMenu(self.scrollable_frame, self.sector_var, *opciones_sector).pack()

        tk.Label(self.scrollable_frame, text="Etapa Actual").pack()
        self.etapa_var = tk.StringVar()
        self.etapa_var.set("Idea")  # Valor por defecto
        opciones_etapa = ["Idea", "MVP", "Producto en el mercado", "Escalamiento"]
        tk.OptionMenu(self.scrollable_frame, self.etapa_var, *opciones_etapa).pack()

        tk.Label(self.scrollable_frame, text="Misión de la Empresa").pack()
        self.mision_var = tk.StringVar()
        tk.Entry(self.scrollable_frame, textvariable=self.mision_var).pack()

        # Inputs para las métricas financieras
        tk.Label(self.scrollable_frame, text="Costo Operativo Mensual (USD)").pack()
        self.costo_operativo_var = tk.DoubleVar()
        tk.Entry(self.scrollable_frame, textvariable=self.costo_operativo_var).pack()

        tk.Label(self.scrollable_frame, text="Crecimiento Mensual (%)").pack()
        self.crecimiento_var = tk.DoubleVar()
        tk.Entry(self.scrollable_frame, textvariable=self.crecimiento_var).pack()

        # Botón para estimar capital
        tk.Button(self.scrollable_frame, text="Estimar Capital Necesario", command=self.controller.estimar_capital).pack(pady=20)

        # Display del resultado
        self.resultado_label = tk.Label(self.scrollable_frame, text="")
        self.resultado_label.pack()

        # Placeholder para el gráfico
        self.canvas_grafico = None

    def mostrar_ayuda(self):
        ayuda_texto = """
        - Nombre de la Empresa: Proporciona el nombre de tu startup.
        - Industria o Sector: Elige el sector en el que opera tu empresa. Esta selección afecta el costo operativo proyectado.
        - Etapa Actual: Selecciona la etapa de desarrollo en la que se encuentra tu startup. La etapa afecta los costos operativos y las necesidades de capital.
        - Costo Operativo Mensual (USD): El costo promedio mensual que incurre tu empresa para operar.
        - Crecimiento Mensual (%): Tasa de crecimiento mensual estimada de tu empresa.
        """
        tk.messagebox.showinfo("Ayuda", ayuda_texto)

    def mostrar_resultado(self, capital_estimado, df_resultados):
        # Mostrar resultado numérico
        self.resultado_label.config(text=f"Capital estimado necesario: ${capital_estimado:.2f}\n\nEste capital es estimado en función de los costos operativos mensuales, el sector, y la etapa actual de tu startup.")

        # Mostrar el gráfico
        fig, ax = plt.subplots(figsize=(5, 4))
        df_resultados.plot(kind='bar', x='Mes', y='Costo Operativo Mensual', ax=ax, color='skyblue')
        ax.set_title('Proyección del Costo Operativo Mensual')
        ax.set_ylabel('USD')

        if self.canvas_grafico:
            self.canvas_grafico.get_tk_widget().pack_forget()
        
        self.canvas_grafico = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        self.canvas_grafico.draw()
        self.canvas_grafico.get_tk_widget().pack()

        # Mostrar la tabla de resultados
        tk.Label(self.scrollable_frame, text="Tabla de Proyección de Costos:", font=("Arial", 12)).pack(pady=10)
        tabla_texto = df_resultados.to_string(index=False)
        tabla_label = tk.Label(self.scrollable_frame, text=tabla_texto, font=("Courier", 10), justify="left")
        tabla_label.pack()

        # Añadir recomendaciones de financiamiento
        recomendacion_texto = self.controller.obtener_recomendaciones()
        tk.Label(self.scrollable_frame, text=f"Recomendación de Financiamiento:\n\n{recomendacion_texto}", wraplength=500, justify="left").pack(pady=10)
