##preparar texto
##se prepara la lista glob que sirve para trabajar con carpetas
import glob
## se define que lista_files es una lista con los nombres de los archivos 
##los cuales están seleccionados como los txt que se encuentran dentro de primer periodo
lista_files = glob.glob(r'/home/felipe/WINDOWS/Código útil/Intentos de trabajos/Lingüística Computacional Final/Primer periodo/Primer periodo/Valdivia/*.txt')
##se define un diccionario donde en los keys se encuentran los nombres y en los values el texto
corpus = {}
##por cada archivo en la lista de archivos
for file in lista_files:
##este se abre con encoding utf-8 y queda definido como file_input
    with open(file, 'r', encoding="utf-8") as file_input:
##se toman los nombres de los textos y se le quitan los primeros 15 caracteres (el nombre de la carpeta)
        corpus[file[125:-4]]=file_input.read()
print('Nombre de los textos')
print(corpus.keys()) 
print('  ')     
print('  ')     



##Limpieza texto

def remover_puntuacion(s): 
    for c in string.punctuation:
        s=s.replace(c,"")
        s=s.replace('\t','')
    return s

#toma el corpus subido y crea una lista vacía
corpus_misional = []
##por cada uno de los keys en corpus.keys se agrega a corpus_misional el value
for key in corpus.keys():
    corpus_misional += [corpus[key]]
import string

## se hace un string para poner todos los values de corpus con el objetivo de trabajarlo como un solo texto grande
string_corpus_misional=' '.join(corpus_misional)

##luego se usa .split para dividir el texto por \n
string_corpus_misional = string_corpus_misional.split('\n')

##Se define una lista como vacio para poder ingresar cada una de las oraciones del corpus sin espacios en blanco
vacio=[oracion for oracion in string_corpus_misional if len(oracion)>0]

##por cada una de estas oraciones en vacio se le saca la puntuación y se bajan las mayúsculas
sin_puntos = []
for oracion in vacio:
    oracion_limpia = remover_puntuacion(oracion)
    sin_puntos += [oracion_limpia.lower()]

##Se toma la lista palabras y luego se ingresan cada una de las palabras de oración que están separadas por comillas
palabras = []
for oracion in sin_puntos:
    palabras += [oracion.split(' ')]

##Cuantificación

print('Resultados')
print('  ')     
 

print('Cantidad de palabras')


tokens = []
for oracion in palabras:
    for palabra in oracion:
        tokens += [palabra]
print(len(tokens))
print('  ')     


print('Cantidad de palabras únicas')


print(len(set(tokens)))
print('  ')     

print('relación')
    

print(len(set(tokens))/len(tokens))
print('  ')     

#contabilizar yem
# =============================================================================
# 
# Yem = {'yem':0,'ema':0,'em':0} 
# for key in Yem.keys():
#     Yem[key]=tokens.count(key)
# 
# print('Cantidad de yem')
#  
# 
# print(Yem)
# print('  ')     
# print('  ')     
# print('Oraciones con -ema')
# print('  ')
# import re
# x= re.findall(r"(?i)((?:\S+\s+){0,3})\bema[^a-z,A-Z,ñ]", str(sin_puntos))
# cantidades = dict.fromkeys(x, 'ema')
# for key, value in cantidades.items():
#     print(key, ' : ', value)
# print('  ')
# print('Cantidad:', len(x))
# print(' ')
# print(' ')
# print('Oraciones con -yem')
# print('  ')
# y= re.findall(r"(?i)((?:\S+\s+){0,3})\byem[^a-z,A-Z,ñ]", str(sin_puntos))
# cantidades = dict.fromkeys(y, 'yem')
# for key, value in cantidades.items():
#     print(key, ' : ', value)
# print('  ')
# print('Cantidad:', len(y))
# print(' ')
# print(' ')
# print('Oraciones con -em')
# print('  ')
# z= re.findall(r"(?i)((?:\S+\s+){0,3})\bem[^a-z,A-Z,ñ]", str(sin_puntos))
# cantidades = dict.fromkeys(x, 'em')
# for key, value in cantidades.items():
#     print(key, ' : ', value)
# print('  ')
# print('Cantidad:', len(z))
# print(' ')
# print(' ')
# 
# input('Presionar ENTER para cerrar')
# =============================================================================
