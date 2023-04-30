grammar = {
    'statement': ['type identifier assignment_operator value semicolon'],
    'type': ['"Num"', '"Char"', '"Bool"'],
    'identifier': ['"a"', '"b"', '"c"'],
    'value': ['integer', 'char', 'boolean'],
    'integer': ['digit' , 'digit+'],
    'char': ['\' "letter" \''],
    'boolean': ['"true"', '"false"'],
    'digit': ['"0"', '"1"', '"2"', '"3"', '"4"', '"5"', '"6"', '"7"', '"8"', '"9"'],
    'letter': ['"a"', '"b"', '"c"', '"d"', '"e"', '"f"', '"g"', '"h"', '"i"', '"j"', '"k"', '"l"', '"m"',
                '"n"', '"o"', '"p"', '"q"', '"r"', '"s"', '"t"', '"u"', '"v"', '"w"', '"x"', '"y"', '"z"'],
    'assignment_operator': ['"="'] , 
    'semicolon' :['";"']
}

# Compute the first sets for each non-terminal symbol
first_sets = {}

def first(symbol):
    if symbol in first_sets:
        return first_sets[symbol]
    
    first_set = set()
    for production in grammar[symbol]:
        for term in production.split():
            if term in grammar:
                first_set |= first(term)
                if '' not in first(term):
                    break
            else:
                first_set.add(term)
                break
    first_sets[symbol] = first_set
    return first_set

# Compute the follow sets for each non-terminal symbol
follow_sets = {}

def follow(symbol, call_stack=None):
    if call_stack is None:
        call_stack = []
    if symbol in follow_sets:
        return follow_sets[symbol]

    follow_set = set()
    if symbol == 'statement':
        follow_set.add('$')
    for nonterminal, production in grammar.items():
        for prod in production:
            if symbol in prod.split():
                idx = prod.split().index(symbol)
                if idx < len(prod.split()) - 1:
                    follow_set |= first(prod.split()[idx+1])
                    if '' in first(prod.split()[idx+1]) and nonterminal not in call_stack:
                        call_stack.append(nonterminal)
                        follow_set |= follow(nonterminal, call_stack)
                elif nonterminal not in call_stack:
                    call_stack.append(nonterminal)
                    follow_set |= follow(nonterminal, call_stack)
    follow_sets[symbol] = follow_set
    return follow_set

# Test the first() and follow() functions
followlist= {}
firstlist = {}

for i in grammar:
    followlist[i] = follow(i)
    firstlist[i] = first(i)

