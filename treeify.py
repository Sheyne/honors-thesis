from string import whitespace

# https://gist.github.com/pib/240957
atom_end = set('()"\'') | set(whitespace)

def parse(sexp):
    stack, i, length = [[]], 0, len(sexp)
    while i < length:
        c = sexp[i]
        reading = type(stack[-1])
        if reading == list:
            if   c == '(': stack.append([])
            elif c == ')': 
                stack[-2].append(stack.pop())
                if stack[-1][0] == ('quote',): stack[-2].append(stack.pop())
            elif c == '"': stack.append('')
            elif c == "'": stack.append([('quote',)])
            elif c in whitespace: pass
            else: stack.append((c,))
        elif reading == str:
            if   c == '"': 
                stack[-2].append(stack.pop())
                if stack[-1][0] == ('quote',): stack[-2].append(stack.pop())
            elif c == '\\': 
                i += 1
                stack[-1] += sexp[i]
            else: stack[-1] += c
        elif reading == tuple:
            if c in atom_end:
                atom = stack.pop()
                if atom[0][0].isdigit(): stack[-1].append(eval(atom[0]))
                else: stack[-1].append(atom)
                if stack[-1][0] == ('quote',): stack[-2].append(stack.pop())
                continue
            else: stack[-1] = ((stack[-1][0] + c),)
        i += 1
    return stack.pop()


def to_operator(t):
    return r"{}".format(t)

def print_step(tupe):
    if isinstance(tupe, tuple) or isinstance(tupe, list):
        [head], *rest = tupe
        return "{}{}{}{}".format(
            to_operator(head),
            r"\left(\begin{aligned}",
            r"\\".join(print_step(r) for r in rest),
            r"\end{aligned}\right)")
    else: 
        return to_operator(tupe)

while True:
    try:
        i = input()
    except EOFError:
        break
    print(r"\begin{align*}")
    print(print_step(parse(i)))
    print(r"\end{align*}")

