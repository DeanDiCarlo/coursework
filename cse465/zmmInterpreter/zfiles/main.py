import sys

RESERVED = {"PRINT", "FOR", "ENDFOR"}

def norm(name) :
    return name.upper()

def checkInt(token) :
    if token.startswith(("+", "-")) and len(token) > 1 :
        return token[1:].isdigit()
    return token.isdigit()

def value(token, memory) :
    if checkInt(token) :
        return int(token)
    v = norm(token)
    if v in RESERVED :
        print(f"RUNTIME ERROR: reserved word used as variable, ({v})")
        sys.exit(1)
    if v not in memory :
        print(f"RUNTIME ERROR: variable used before assignment, ({v})")
        sys.exit(1)
    return memory[v]

def findEnd(tokens, i) :
    while i < len(tokens) :
        t = tokens[i].upper()
        if t == "FOR" :
            print("RUNTIME ERROR: Nested loops not supported")
            sys.exit(1)
        if t == "ENDFOR":
            return i
        i += 1
    print("RUNTIME ERROR: missing ENDFOR")
    sys.exit(1)

def runLine(tokens, i, memory) :
    while i < len(tokens) :
        t = tokens[i].upper()

        if t == "ENDFOR" :
            return i

        if t == "PRINT" :
            var = tokens[i + 1]
            semi = tokens[i + 2]
            if semi != ";" :
                print("RUNTIME ERROR: missing ';'")
                sys.exit(1)
            print(value(var, memory))
            i += 3
            continue
            
        if t == "FOR" :
            countTok = tokens[i + 1]
            if not checkInt(countTok) :
                print("RUNTIME ERROR: FOR count must be integer")
                sys.exit(1)
            count = int(countTok)

            loopStart = i + 2
            loopEnd = findEnd(tokens, loopStart)
            loopCode = tokens[loopStart:loopEnd]

            for i in range(count) :
                runLine(loopCode, 0, memory)

            i = loopEnd + 1
            continue
            
        if i + 3 >= len(tokens) :
            print("RUNTIME ERROR: Incomplete assignment of value")
            sys.exit(1)
        
        var = tokens[i]
        operation = tokens[i + 1]
        num = tokens[i + 2]
        semi = tokens[i + 3]

        if semi != ";" :
            print("RUNTIME ERROR: Missing ';'")
            sys.exit(1)

        v = norm(var)
        if v in RESERVED :
            print(f"RUNTIME ERROR: reserved word used as variable: ({var})")

        val = value(num, memory)

        if operation == "=" :
            memory[v] = val
        elif operation == "+=" :
            if v not in memory: 
                print(f"RUNTIME ERROR: variable used before assignment, ({var})")
                sys.exit(1)
            memory[v] += val
        elif operation == "-=" :
            if v not in memory: 
                print(f"RUNTIME ERROR: variable used before assignment, ({var})")
                sys.exit(1)
            memory[v] -= val
        elif operation == "*=" :
            if v not in memory: 
                print(f"RUNTIME ERROR: variable used before assignment, ({var})")
                sys.exit(1)
            memory[v] *= val
        else :
            print(f"RUNTIME ERROR: unknown operator ({operation})")

        i += 4
    
    return i


def main() :
    if len(sys.argv) != 2:
        print("Usage: python3 main.py file.zmm")
        sys.exit(2)

    path = sys.argv[1]
    try: 
        with open(path, "r") as f:
            text = f.read()
    except Exception as e:
        print(f"Error: Could not open file ({path})")
        print(e)
        sys.exit(2)

    tokens = text.split()
    memory = {}
    runLine(tokens, 0, memory)


main()