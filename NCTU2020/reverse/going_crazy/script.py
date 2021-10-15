# to execute : gdb -x solve.py
import gdb

gdb.execute('file gogo')

global breakpoint

gdb.execute('b *0x48e70a')
breakpoint = 1

flag = list('000000000000000000000000000000000000')
correct = 0

def find_index(input, times):
    global breakpoint

    gdb.execute('b *0x48e6b5')
    breakpoint += 1
    gdb.execute('''run < <(python -c 'print("''' + input + '''")')''')

    for _ in range(1, times):
        gdb.execute('c')
        gdb.execute('c')

    index = gdb.parse_and_eval("$rcx")
    print(index)
    gdb.execute('delete breakpoint ' + str(breakpoint))
    
    return int(index)

for number in range(1,37):
    for k in range(32,127):
        find = False

        if k == 32:
            index = find_index('x' + ','.join(flag) + 'x', number)

        flag[index] = str(k)
        input = 'x' + ','.join(flag) + 'x'

        gdb.execute('''run < <(python -c 'print("''' + input + '''")')''')
            
        for c in range(number):
            rcx = gdb.parse_and_eval("$rcx")
            rdx = gdb.parse_and_eval("$rdx")

            if rcx == rdx :
                gdb.execute('c')
            else:
                break

            if c == number - 1:
                find = True
                break

        if find:
            break
    
print(''.join(list(map(chr,list(map(int,flag))))))
# FLAG{gogo_p0werr4ng3r!you_did_IT!!!}