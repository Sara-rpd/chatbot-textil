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
        # VARIABLES LAND BOT
        # =========================

        archivo_url = data.get("file")
        unidad_negocio = data.get("unidad_negocio")

        print("\nArchivo URL:")
        print(archivo_url)

        print("\nUnidad negocio:")
        print(unidad_negocio)

        # =========================
        # VALIDAR ARCHIVO
        # =========================

        if not archivo_url:

            return {
                "mensaje": "No se recibió el archivo Excel."
            }

        # =========================
        # DESCARGAR EXCEL
        # =========================

        response = requests.get(archivo_url)

        if response.status_code != 200:

            return {
                "mensaje": "No fue posible descargar el archivo."
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
                    "mensaje": f"El archivo no contiene la columna requerida: {col}"
                }

        # =========================
        # CONVERTIR A DICCIONARIO
        # =========================

        datos = {}

        for _, row in df.iterrows():

            prueba = str(row["Prueba"]).strip()
            valor = row["Valor"]

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

        print("\nRESULTADOS:")
        print(resultados)

        # =========================
        # VALIDAR RESULTADOS
        # =========================

        if not resultados:

            return {
                "mensaje": (
                    "No se encontraron tecnologías "
                    "compatibles con las pruebas cargadas."
                )
            }

        # =========================
        # CONSTRUIR RESPUESTA
        # =========================

        mensaje = (
            "Según las pruebas cargadas, "
            "estas son las tecnologías recomendadas:\n\n"
        )

        # TOP 5
        for item in resultados[:5]:

            tecnologia = item["tecnologia"]
            confianza = item["confianza"]

            mensaje += (
                f"• {tecnologia} "
                f"({confianza}%)\n"
            )

        # =========================
        # RESPUESTA FINAL
        # =========================

        return {
            "mensaje": mensaje
        }

    except Exception as e:

        print("\nERROR GENERAL:")
        print(str(e))

        return {
            "mensaje": f"Ocurrió un error: {str(e)}"
        }
