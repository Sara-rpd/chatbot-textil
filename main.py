from fastapi import FastAPI
import pandas as pd
import requests
from motor import clasificar
import tempfile

app = FastAPI()


# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "mensaje": "API chatbot textil funcionando"
    }


# =========================
# ENDPOINT CLASIFICAR
# =========================

@app.post("/clasificar")
def clasificar_tecnologia(data: dict):

    try:

        print("\n=========================")
        print("JSON RECIBIDO:")
        print(data)

        # =========================
        # OBTENER VARIABLES LAND BOT
        # =========================

        archivo_url = data.get("file")
        unidad_negocio = data.get("unidad_negocio")

        print("\nArchivo URL:")
        print(archivo_url)

        print("\nUnidad negocio:")
        print(unidad_negocio)

        # =========================
        # VALIDAR URL
        # =========================

        if not archivo_url:

            return {
                "error": "No se recibió archivo"
            }

        # =========================
        # DESCARGAR EXCEL
        # =========================

        response = requests.get(archivo_url)

        if response.status_code != 200:

            return {
                "error": "No se pudo descargar el archivo"
            }

        # =========================
        # GUARDAR TEMPORAL
        # =========================

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".xlsx"
        ) as tmp:

            tmp.write(response.content)

            ruta_temp = tmp.name

        print("\nArchivo temporal:")
        print(ruta_temp)

        # =========================
        # LEER EXCEL
        # =========================

        df = pd.read_excel(ruta_temp)

        print("\nDATAFRAME:")
        print(df)

        # =========================
        # VALIDAR COLUMNAS
        # =========================

        columnas_requeridas = ["Prueba", "Valor"]

        for col in columnas_requeridas:

            if col not in df.columns:

                return {
                    "error": f"Falta columna: {col}"
                }

        # =========================
        # CONVERTIR A DICCIONARIO
        # =========================

        datos = {}

        for _, row in df.iterrows():

            prueba = str(row["Prueba"]).strip()
            valor = row["Valor"]

            # Convertir numpy/int/float
            try:

                if pd.notna(valor):

                    valor = float(valor)

                    if valor.is_integer():
                        valor = int(valor)

            except:
                pass

            datos[prueba] = valor

        # =========================
        # AGREGAR UNIDAD NEGOCIO
        # =========================

        datos["unidad_negocio"] = unidad_negocio

        print("\nDATOS FINALES:")
        print(datos)

        # =========================
        # EJECUTAR MOTOR
        # =========================

        resultados = clasificar(datos)

        print("\nRESULTADOS MOTOR:")
        print(resultados)

        # =========================
        # EXTRAER TECNOLOGIAS
        # =========================

        nombres_tecnologias = []

        for item in resultados:

            if isinstance(item, dict):

                tecnologia = item.get("tecnologia")

                if tecnologia:
                    nombres_tecnologias.append(
                        str(tecnologia)
                    )

            else:

                nombres_tecnologias.append(
                    str(item)
                )

        # =========================
        # RESPUESTA FINAL
        # =========================

        return {

            "datos_recibidos": datos,

            "ranking": resultados,

            "tecnologias": ", ".join(nombres_tecnologias)

        }

    except Exception as e:

        print("\nERROR GENERAL:")
        print(str(e))

        return {
            "error": str(e)
        }
