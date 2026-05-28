from fastapi import FastAPI, UploadFile, File
import pandas as pd
from motor import clasificar

app = FastAPI()

@app.get("/")
def home():

    return {
        "mensaje": "API chatbot textil funcionando"
    }


@app.post("/clasificar")
async def clasificar_tecnologia(
    file: UploadFile = File(...)
):

    try:

        # Leer Excel
        df = pd.read_excel(file.file)

        # Convertir tabla a diccionario
        # Formato esperado:
        # | Prueba | Valor |

        datos = dict(
            zip(
                df["Prueba"],
                df["Valor"]
            )
        )

        # Ejecutar motor de reglas
        resultados = clasificar(datos)

        return {
            "datos_recibidos": datos,
            "tecnologias": resultados
        }

    except Exception as e:

        return {
            "error": str(e)
        }
