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

        # Obtener payload real
        payload = data.get("RECIBIDO", {})

        # Variables
        archivo_url = payload.get("file")
        unidad_negocio = payload.get("unidad_negocio")

        print("Archivo:", archivo_url)
        print("Unidad:", unidad_negocio)

        # Descargar Excel
        response = requests.get(archivo_url)

        # Guardar temporal
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

        print("Datos finales:", datos)

        # Ejecutar motor
        resultados = clasificar(datos)

        return {
            "datos_recibidos": datos,
            "tecnologias": ", ".join(resultados)
        }

    except Exception as e:

        return {
            "error": str(e)
        }
