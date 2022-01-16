from pathlib import Path

Path(r'C:\Users\mauri-Pc\Desktop\holamundo.txt').stat()
file_size = Path(r'C:\Users\mauri-Pc\Desktop\holamundo.txt').stat().st_size
print("The file size is:", file_size, "bytes")

f = open('holamundo.txt', 'r')

f = f.readlines()

#
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


tamBloque = 3  # byte
tamMensaje = 7
tamLlave = 0

x = ''
for linea in f:

    linBin = bytearray(linea, "utf8")
    for letra in linBin:
        binario = format(letra, '08b')
        x = x + binario

i = 0
listaBloq = []
while i * tamBloque * 8 < len(x):
    listaBloq.append(x[tamBloque * i * 8:tamBloque * 8 * (i + 1)])
    i += 1

for bloque in listaBloq:
    n = len(bloque)
    if n == tamBloque * 8:
        mitad = int(n / 2)
        L1 = bloque[0:mitad]
        R1 = bloque[mitad:n]
        cod = xor(L1, R1)
