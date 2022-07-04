import pandas as pd
import random
print('JUEGOS CULIAOS QUE TENEMOS:')
print(' ')
juegos = pd.read_csv(r"Juegos.csv")
juegos = list(juegos['Juegos'])
print(juegos)
print(' ')
print("escribir 'si' para tirar el dado y 'no' para salir")
while input('¿Tiro el dado? ') == 'si':
    seleccion = random.choice(juegos)
    print(' ')
    print(' ')
    print('JUEGO CULIAO QUE VAMOS A JUGAR')
    print(' ')
    print(seleccion)
    print(' ')
    print(' ')
    print(' ')
    print(' ')
    print(' ')

