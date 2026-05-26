import pandas as pd

# Leer Excel
reglas = pd.read_excel("Reglas.xlsx")


def evaluar_regla(valor_usuario, operador, valor_regla):

    if operador == ">=":
        return valor_usuario >= valor_regla

    if operador == "<=":
        return valor_usuario <= valor_regla

    if operador == ">":
        return valor_usuario > valor_regla

    if operador == "<":
        return valor_usuario < valor_regla

    if operador == "==":
        return valor_usuario == valor_regla

    return False


def clasificar(data):

    resultados = {}

    # Unidad de negocio seleccionada
    unidad_negocio_usuario = data.get("unidad_negocio")

    for _, row in reglas.iterrows():

        # Leer columnas Excel
        unidad_negocio_regla = row["Unidad de Negocio"]
        tecnologia = row["TecnologÍa"]
        variable = row["Variable"]
        operador = row["Operador"]
        valor_regla = row["Valor"]
        peso = row["Peso"]

        # FILTRO unidad negocio
        if unidad_negocio_regla != unidad_negocio_usuario:
            continue

        # Validar existencia variable
        if variable not in data:
            continue

        valor_usuario = data[variable]

        cumple = evaluar_regla(
            valor_usuario,
            operador,
            valor_regla
        )

        if cumple:

            if tecnologia not in resultados:
                resultados[tecnologia] = 0

            resultados[tecnologia] += peso

    ranking = []

    for tecnologia, score in resultados.items():

        ranking.append({
            "tecnologia": tecnologia,
            "confianza": score
        })

    ranking = sorted(
        ranking,
        key=lambda x: x["confianza"],
        reverse=True
    )

    return ranking