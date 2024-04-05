#########################################
# assembler (compiler?) to befunge lmao #
# why did i do this                     #
#########################################


def readProgram(filename):
    labels = {}
    instructions = []

    pc = 0

    with open(filename) as f:
        for line in f:
            if line[0] == '#':
                continue
            s = line.strip()
            if s == '':
                continue
            if s[-1] == ':':
                labels[s[:-1]] = pc
            else:
                toks = s.split(' ')
                instructions.append(toks)
                pc += 1
    # pass 2
    resolved = []
    for instr in instructions:
        result = [instr[0]]
        for op in instr[1:]:
            if op in labels:
                result.append(labels[op])
            else:
                result.append(int(op))
        resolved.append(result)

    labels_in_order = [i for _, i in labels.items()]
    labels_in_order.sort()
    return resolved, labels_in_order


def pushNumber(num):
    # encode to octal
    s = oct(num)[2:]
    return '0' + '8*'.join(c + '+' for c in s)


def getRegister(reg):
    # registers at y 0, x reg + 1
    return f'{reg + 1}0g'


def setRegister(reg):
    # registers at y 0, x reg + 1
    return f'{reg + 1}0p'


def generateBefunge(instrs, labels):
    prelude = "vRRRRRRRR\n" + ">" * (len(labels) + 5) + "v\n>>v\n"

    code = ""
    pc = 0
    for instr in instrs:
        line1 = "^ 1"
        line2 = "^ -# "  # arbitrary jump
        line3 = "^ :  "  # normal jump
        line4 = "^v_$ "  # instruction
        line5 = "^>v  "  # normal return
        for label in labels:
            if label == pc:
                line4 += '>'
            else:
                line4 += ' '
            line2 += ' '
            line5 += ' '
        line2 += ' '
        line4 += '>'
        line5 += 'v'

        instrCode = ''

        match instr[0]:
            case 'add':
                instrCode += getRegister(instr[2])
                instrCode += getRegister(instr[3])
                instrCode += '+'
                instrCode += setRegister(instr[1])
            case 'sub':
                instrCode += getRegister(instr[2])
                instrCode += getRegister(instr[3])
                instrCode += '-'
                instrCode += setRegister(instr[1])
            case 'mul':
                instrCode += getRegister(instr[2])
                instrCode += getRegister(instr[3])
                instrCode += '*'
                instrCode += setRegister(instr[1])
            case 'div':
                instrCode += getRegister(instr[2])
                instrCode += getRegister(instr[3])
                instrCode += '/'
                instrCode += setRegister(instr[1])
            case 'mod':
                instrCode += getRegister(instr[2])
                instrCode += getRegister(instr[3])
                instrCode += '%'
                instrCode += setRegister(instr[1])
            case 'mov':
                instrCode += pushNumber(instr[2])
                instrCode += setRegister(instr[1])
            case 'push':
                instrCode += getRegister(instr[1])
            case 'pop':
                instrCode += setRegister(instr[1])
            case 'jeq':
                instrCode += getRegister(instr[1])
                instrCode += getRegister(instr[2])
                instrCode += '-!|'
                for label in labels:
                    if label == instr[3]:
                        if label > pc:
                            line3 += 'v'
                        else:
                            line3 += '^'
                    else:
                        line3 += ' '
                line3 += ' ' * (len(instrCode))
                line3 += '<'
            case 'jle':
                instrCode += getRegister(instr[1])
                instrCode += getRegister(instr[2])
                instrCode += '`!|'
                for label in labels:
                    if label == instr[3]:
                        if label > pc:
                            line3 += 'v'
                        else:
                            line3 += '^'
                    else:
                        line3 += ' '
                line3 += ' ' * (len(instrCode))
                line3 += '<'
            case 'jmp':
                instrCode += '^'
                for label in labels:
                    if label == instr[1]:
                        if label > pc:
                            line3 += 'v'
                        else:
                            line3 += '^'
                    else:
                        line3 += ' '
                line3 += ' <'
            case 'call':
                instrCode += pushNumber(pc + 2)
                instrCode += '^'
                for label in labels:
                    if label == instr[1]:
                        if label > pc:
                            line3 += 'v'
                        else:
                            line3 += '^'
                    else:
                        line3 += ' '
                line3 += ' ' * (len(instrCode))
                line3 += '<'
            case 'ret':
                line2 += '<'
                instrCode += '^'
            case 'hlt':
                instrCode += '@'
            case 'read_in':
                instrCode += '~'
                instrCode += setRegister(instr[1])
            case 'write_out':
                instrCode += getRegister(instr[1])
                instrCode += ','

        instrCode += 'v'

        line4 += instrCode
        line5 += '<' * (len(line4) - len(line5))
        pc += 1

        code += line1 + '\n'
        code += line2 + '\n'
        code += line3 + '\n'
        code += line4 + '\n'
        code += line5 + '\n'
    return prelude + code


def main():
    prog, labels = readProgram('prog.txt')
    print(generateBefunge(prog, labels))


main()
