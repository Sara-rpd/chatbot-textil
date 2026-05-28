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

    return {
        "RECIBIDO": data
    }

    try:

        archivo_url = data.get("file")

        unidad_negocio = data.get("unidad_negocio")

        # Convertir array a string
        if isinstance(unidad_negocio, list):
            unidad_negocio = unidad_negocio[0]

        print("Unidad negocio:", unidad_negocio)

        response = requests.get(archivo_url)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:

            tmp.write(response.content)

            ruta_temp = tmp.name

        df = pd.read_excel(ruta_temp)

        datos = dict(
            zip(
                df["Prueba"],
                df["Valor"]
            )
        )

        # Agregar unidad negocio
        datos["unidad_negocio"] = unidad_negocio

        print("Datos finales:", datos)

        resultados = clasificar(datos)

        return {
            "datos_recibidos": datos,
            "tecnologias": ", ".join(resultados)
        }

    except Exception as e:

        return {
            "error": str(e)
        }
