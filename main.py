from fastapi import FastAPI
import pandas as pd
import requests
from motor import clasificar
import tempfile

app = FastAPI()

@app.get("/")
def home():

    return {
        "mensaje": "API chatbot textil funcionando"
    }


@app.post("/clasificar")
def clasificar_tecnologia(data: dict):

    try:

        # Obtener datos desde Landbot
        archivo_url = data.get("file")
        unidad_negocio = data.get("unidad_negocio")

        # Descargar archivo Excel
        response = requests.get(archivo_url)

        # Guardar temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:

            tmp.write(response.content)

            ruta_temp = tmp.name

        # Leer Excel
        df = pd.read_excel(ruta_temp)

        # Convertir a diccionario
        datos = dict(
            zip(
                df["Prueba"],
                df["Valor"]
            )
        )

        # Agregar unidad negocio
        datos["unidad_negocio"] = unidad_negocio

        # Ejecutar motor de reglas
        resultados = clasificar(datos)
        
        # Extraer nombres
        nombres_tecnologias = [
            item["tecnologia"]
            for item in resultados
        ]
        
        return {
            "datos_recibidos": datos,
            "ranking": resultados,
            "tecnologias": ", ".join(nombres_tecnologias)
        }

    except Exception as e:

        return {
            "error": str(e)
        }
