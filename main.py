import hashlib
from pathlib import Path

Path(r'C:\Users\nico4\Downloads\Universidad\Sistemas De Comunicación\Laboratorio\Lab 3\Codigo\txt.txt').stat()
file_size = Path(r'C:\Users\nico4\Downloads\Universidad\Sistemas De Comunicación\Laboratorio\Lab 3\Codigo\txt.txt').stat().st_size
print("The file size is:", file_size, "bytes")

f = open('txt.txt', 'r')

f = f.readlines()

# Funcion que realiza la operacion entre 2 bloques del mismo tamaño de 0 y 1
def xor(a, b):
    i = 0
    codigo = ''

    while i < len(a):
        if a[i] == b[i]:
            codigo = codigo + '0'
        else:
            codigo = codigo + '1'
        i += 1

    return codigo

# Se generan sus llaves usando hash,
def generarsubllaves(llave, tamaño, cantidad):
    llaves = []
    hash = hashlib.blake2b(digest_size=tamaño)
    hash.update(llave.encode())
    subllave = hash.digest()
    llaves.append(subllave)

    i = 1
    while i < cantidad:
        hash.update(subllave)
        subllave = hash.digest()
        llaves.append(subllave)
        i = i + 1

    return llaves

# Funcion que transforma tanto el bloque ingresado como la subllave en valores numericos
# se suman y el resultado de la suma se tranforma a binario para obtener el bloque de salida
def funcion(subLlave, bloque):
    resultado = int(bloque, 2)                          # Se pasa el bloque a su valor numerico

    for bytes in subLlave:                              # Se suman los valores de cada byte de la llave
        resultado = resultado + bytes

    lenbloque = len(bloque)                             # Se obtiene el largo original del bloque

    while resultado > pow(2, len(bloque)):              # Si el resultado obtenido es mayor 2 elevado al tamaño del
        resultado = resultado - pow(2, len(bloque))     # Se resta para que su numero binario no posea mas bit
                                                        # De los necesarios
    resultado = format(resultado, "b")

    while len(resultado) < len(bloque):                 # Si les faltaran bit al resultado se rellenan con 0
        resultado = '0' + resultado

    return resultado


llave = "hola"      # Llave principal
tamBloque = 4       # Tamaño de los bloques en bytes (tamaño final len, tamBloque*8)
tamMensaje = 10     # Tamaño del mensaje en bytes
tamLlave = 4        # Tamaño de las subllaves en bytes

x = ''              # Lista vacia para almacenar mensaje en binario

for linea in f:
    linBin = bytearray(linea, "utf8")

    for letra in linBin:
        binario = format(letra, '08b')
        x = x + binario

listaBloq = []      # Se dividen los bloques a encriptar (Almacena)
i = 0

while i * tamBloque * 8 < len(x):
    listaBloq.append(x[tamBloque * i * 8:tamBloque * 8 * (i + 1)])
    i += 1

subllaves = generarsubllaves(llave, tamLlave, len(listaBloq))
tipo = 1                            # 0 para codificar / 1 para decodificar

final = ''
i=0
for bloque in listaBloq:
    rondas = 16
    n = len(bloque)
    mitad = int(n / 2)
    L0 = bloque[0:mitad]
    R0 = bloque[mitad:n]

    while rondas > 0:
        if tipo == 0:
            R0Aux = funcion(subllaves[i], R0)
            R1 = xor(R0Aux, L0)
            L0 = R0
            R0 = R1
        else:
            R0Aux = funcion(subllaves[len(subllaves)-i-1], R0)
            R1 = xor(R0Aux, L0)
            L0 = R0
            R0 = R1

        rondas = rondas - 1

    LF = R0
    RF = L0

    final = final + LF + RF

    i = i+1

print(final)        #Mensaje final en binario











