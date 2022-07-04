import pandas as pd
todas_las_lenguas = pd.read_csv(r'C:/Users/fneir/OneDrive/Escritorio/Código útil/Intentos de trabajos/Wals/languages.csv')
values = pd.read_csv(r'C:/Users/fneir/OneDrive/Escritorio/Código útil/Intentos de trabajos/Wals/values.csv')
lenguas_sudamerica_code = ['South America']
lenguas_sudamerica= todas_las_lenguas[todas_las_lenguas.Macroarea.isin(lenguas_sudamerica_code)]
df = pd.read_csv(r'C:/Users/fneir/OneDrive/Escritorio/Código útil/Intentos de trabajos/Wals/Lenguas.csv')
df[['Language','CODE']] = df['Language;CODE'].str.split(';', expand=True)
Lenguas_Andinas=df.drop(['Language;CODE'], axis=1)
Features = pd.read_csv(r"C:/Users/fneir/OneDrive/Escritorio/Código útil/Intentos de trabajos/Wals/codes.csv")

while True:
    ##ingresar el input a buscar
    feature_buscado = input("Feature buscado: ")
    ##convertirlo en una lista
    features_buscados = [feature_buscado]

    for item in features_buscados:
        features= Features[Features.Parameter_ID.isin(features_buscados)]

    Feature_Wals = {list(features['Name'])[i]: list(features['Number'])[i] for i in range(len(list(features['Name'])))}

    print(Feature_Wals)

    Muestra = input("Lenguas: ")

    for item in features_buscados:
        value_por_lengua= values[values.Parameter_ID.isin(features_buscados)]

    Lenguas_Sudamerica_Negacion = set(list(lenguas_sudamerica['ID'])) & set(list(value_por_lengua['Language_ID']))
    Todas_las_lenguas = list(todas_las_lenguas['ID'])
    Resultados_lengua= value_por_lengua[value_por_lengua.Language_ID.isin(Lenguas_Sudamerica_Negacion)]

    Turco = []
    for item in list(features['Name']):
        Turco += '0'
    Turco = [int(x) for x in Turco]
    Cantidades_Nombres = {list(features['Name'])[i]: Turco[i] for i in range(len(list(features['Name'])))}
    Cantidades_numericas = {list(features['Number'])[i]: Turco[i] for i in range(len(list(features['Name'])))}
    if Muestra == "Sudamerica":
        for item in list(features_buscados):
            value_por_lengua= values[values.Parameter_ID.isin(list(features_buscados))]
            Lenguas_Sudamerica_Negacion = set(list(lenguas_sudamerica['ID'])) & set(list(value_por_lengua['Language_ID']))
            Resultados_lengua_Sudamerica = value_por_lengua[value_por_lengua.Language_ID.isin(Lenguas_Sudamerica_Negacion)]
            print(Resultados_lengua_Sudamerica[['ID','Language_ID', 'Parameter_ID', 'Value']])
        for key in Cantidades_numericas.keys():
            Cantidades_numericas[key]+=(list(Resultados_lengua_Sudamerica['Value'])).count(key)

        Cantidades = dict(zip(Cantidades_Nombres.keys(),Cantidades_numericas.values()))
        
    if Muestra == "Muestra":
        for item in features_buscados:
            value_por_lengua= values[values.Parameter_ID.isin(features_buscados)]
            Lenguas_Sudamerica_Negacion = set(list(Lenguas_Andinas['CODE'])) & set(list(value_por_lengua['Language_ID']))
            Resultados_lengua_Muestra= value_por_lengua[value_por_lengua.Language_ID.isin(Lenguas_Sudamerica_Negacion)]
            print(Resultados_lengua_Muestra[['ID','Language_ID', 'Parameter_ID', 'Value']]) 
        for key in Cantidades_numericas.keys():
            Cantidades_numericas[key]+=(list(Resultados_lengua_Muestra['Value'])).count(key)

    if Muestra == "WALS":
        for item in list(features_buscados):
            value_por_lengua= values[values.Parameter_ID.isin(list(features_buscados))]
            Lenguas_todas = set(Todas_las_lenguas) & set(list(value_por_lengua['Language_ID']))
            Resultados_lengua_WALS = value_por_lengua[value_por_lengua.Language_ID.isin(Lenguas_todas)]
            print(Resultados_lengua_WALS[['ID','Language_ID', 'Parameter_ID', 'Value']])
        for key in Cantidades_numericas.keys():
            Cantidades_numericas[key]+=(list(Resultados_lengua_WALS['Value'])).count(key)
            
    Cantidades = dict(zip(Cantidades_Nombres.keys(),Cantidades_numericas.values()))
    print(" ")
    print("Cantidades")
    print(" ")
    print(Cantidades)

    total = sum(Cantidades.values())
    Cantidades.update((x, y*100) for x, y in Cantidades.items())
    Cantidades.update((x, y/int(total)) for x, y in Cantidades.items())
    print(" ")
    print("porcentajes")
    print(" ")
    print(Cantidades)
    print(" ")
    if not input ("¿Cerrar? ").lower().startswith("no"):
        break