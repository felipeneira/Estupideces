#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# 
# =============================================================================
import pandas as pd
import re
# =============================================================================
# 
# =============================================================================
datos = pd.read_csv("/home/felipe/Descargas/inventario3.csv", sep='delimiter', header=None)
lista = [str(item) for item in datos[0]]
columnas = [item for item in lista[3:7]]
header =  [item for item in lista[0:3]]
lista = [re.sub(r"([a-zA-Z0-9])  ", r"\1;  ", item) for item in lista[7:len(lista)]]
lista = [re.sub(r"([A-Z]+ [0-9\.\/\,]*); ([a-zA-Z\s]*;+)", r"\1 \2 ", item) for item in lista]
lista = [re.sub("( ; )", "  ", item) for item in lista]
lista = [re.sub(r"([0-9]+) ([a-zA-Z]+)", r"\1; \2", item) for item in lista]
lista = [re.sub(r"([0-9]+) (\$)", r"\1; \2", item) for item in lista]
lista = [re.sub(r"([0-9]+)(\$)", r"\1; \2", item) for item in lista]
lista = [re.sub(r"([A-Z]+);  ([A-Z]+)", r"\1 \2", item) for item in lista]
columnas = [re.sub(r"([a-zA-Z0-9\.])  ", r"\1;  ", item) for item in columnas]
columnas = [re.sub(r"([a-zA-Z]+) ([$a-zA-Z]+)", r"\1; \2", item) for item in columnas]
final = header+columnas+lista
dict = {None:final}
df = pd.DataFrame(dict,index=None)
df.to_csv('prueba.csv', index=False) 
