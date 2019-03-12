print(".data")

print("init_iregs: #инициализация начальных значений")

init_iregs = [i + 1 for i in range(30)]
for i in init_iregs:
    if abs(i - 1) % 10 == 0:
        print(".word", end=' ')
    init_iregs[i - 1] = i if i % 2 == 0 else -1 * i
    print(init_iregs[i - 1], ", ", sep='', end='')
    if abs(i) % 10 == 0:
        print()

f = 2047
im = []

for i in range(30):
    f = f - (2 ** (i % 11)) if (i // 11) % 2 == 0 else f + 2 ** (i % 11)
    im.append(f)

ref = [init_iregs[i] & im[i] for i in range(30)]
print("\nrefs:  #инициализация референтных значений",end='')

for i in range(30):
    if i % 10 == 0:
        print()
        print(".word", end=' ')
    print(ref[i], ", ", sep='', end='')


print("\n\nsave_x2:  #создание метки на область памяти, которая будет использоваться для запоминания x2\n.word 0\n.text")
print('\nmain:')
print("    la x1, init_iregs")

for i in range(30):
    print('    lw x', i + 2, ', ', i * 4, '(x1)', sep='')

print()

for i in range(30):
    print('    andi x', i + 2, ', x', i + 2, ', ', hex(im[i]), sep='')

print()
print("    la x1, save_x2")
print("    sw x2, 0(x1)\n")
print("    la x1, refs\n")

for i in range(39):
    print('    lw x2, ', (i + 1) * 4, '(x1)', sep='')
    print('    bne x', i + 3, ', x2, pass_fail', sep='')
print()
print("    la x1, save_x2\n    lw x2, 0(x1)\n    la x1, refs\n    lw x3, 0(x1)\n    bne x3, x2, pass_fail", sep='')

print("pass_ok:\n\taddi  x10, x0, 1\n\taddi   x11, x0, 5\n\tecall\n\tj    exit\n")
print("pass_fail:\n\taddi  x10, x0, 11\n\taddi  x11, x0, 83\n\tecall\n")
print("exit:\n\taddi  x10, x0, 10\n\tecall # terminate ecall")



