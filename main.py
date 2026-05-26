from fastapi import FastAPI
from motor import clasificar

app = FastAPI()

@app.get("/")
def home():

    return {
        "mensaje": "API chatbot textil funcionando"
    }


@app.post("/clasificar")
def clasificar_tecnologia(data: dict):

    resultados = clasificar(data)

    return {
        "tecnologias": resultados
    }