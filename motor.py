import pandas as pd

# =========================
# LEER ARCHIVO EXCEL
# =========================

reglas = pd.read_excel("Reglas.xlsx")

# Verificar nombres columnas
print("COLUMNAS DEL EXCEL:")
print(reglas.columns)


# =========================
# FUNCIÓN EVALUAR REGLAS
# =========================

def evaluar_regla(valor_usuario, operador, valor_regla):

    if operador == ">=":
        return valor_usuario >= valor_regla

    elif operador == "<=":
        return valor_usuario <= valor_regla

    elif operador == ">":
        return valor_usuario > valor_regla

    elif operador == "<":
        return valor_usuario < valor_regla

    elif operador == "==":
        return valor_usuario == valor_regla

    return False


# =========================
# FUNCIÓN PRINCIPAL
# =========================

def clasificar(data):

    resultados = {}

    # Unidad negocio enviada desde API
    unidad_negocio_usuario = data.get("unidad_negocio")

    print("\n=========================")
    print("DATOS RECIBIDOS:")
    print(data)

    # Recorrer reglas Excel
    for _, row in reglas.iterrows():

        try:

            # =========================
            # LEER COLUMNAS EXCEL
            # =========================

            unidad_negocio_regla = row["Unidad de Negocio"]
            tecnologia = row["Tecnología"]
            variable = row["Variable"]
            operador = row["Operador"]
            valor_regla = row["Valor"]
            peso = row["Peso"]

            # =========================
            # DEBUG
            # =========================

            print("\n-------------------")
            print("Tecnología:", tecnologia)
            print("Variable:", variable)

            # =========================
            # FILTRAR UNIDAD NEGOCIO
            # =========================

            if unidad_negocio_regla != unidad_negocio_usuario:
                continue

            # =========================
            # VALIDAR VARIABLE
            # =========================

            if variable not in data:

                print("Variable NO encontrada en JSON")
                continue

            valor_usuario = data[variable]

            print("Valor usuario:", valor_usuario)
            print("Operador:", operador)
            print("Valor regla:", valor_regla)

            # =========================
            # EVALUAR REGLA
            # =========================

            cumple = evaluar_regla(
                valor_usuario,
                operador,
                valor_regla
            )

            print("Cumple:", cumple)

            # =========================
            # SUMAR SCORE
            # =========================

            if cumple:

                if tecnologia not in resultados:
                    resultados[tecnologia] = 0

                resultados[tecnologia] += peso

        except Exception as e:

            print("ERROR EN FILA:")
            print(row)
            print(e)

    # =========================
    # CONSTRUIR RANKING
    # =========================

    ranking = []

    for tecnologia, score in resultados.items():

        ranking.append({
            "tecnologia": tecnologia,
            "confianza": round(score, 2)
        })

    # =========================
    # ORDENAR
    # =========================

    ranking = sorted(
        ranking,
        key=lambda x: x["confianza"],
        reverse=True
    )

    print("\n=========================")
    print("RESULTADOS:")
    print(ranking)

    return ranking
