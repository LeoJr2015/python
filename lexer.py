#****************** Lexer ************************

tokenlist = []
currtoken = ("", "", 0)
keywords = set(["while", "endwhile", "if", "else", "endif", "print", "=", "==", "!=", "+", "-"])
symboltable = dict()

def nextToken():
    global currtoken, symboltable
    if(len(tokenlist) > 0):
        s = tokenlist.pop(0)
        if s in keywords:
            currtoken = (s, "", 0)
        elif s.isdigit():
            currtoken = ("digit", "", int(s))
        elif s.isalnum():
            symboltable[s] = 0
            currtoken = ("label", s, 0)
        else:
            print "syntax error: " + s
    else:
        currtoken = ("", "", 0)

def consume(expected):
    if currtoken[0] == expected:
        nextToken()
    else:
        print "expected " + expected + " not found" 

#****************** Parser ************************

def parseFile(filename):
    inputfile = open(filename, "r")
    inputstring = inputfile.read()
    global tokenlist
    tokenlist = inputstring.split()
    nextToken()
    return doStatementList()

def doStatementList():
    stmts = []
    newstmt = []
    
    while currtoken[0] in ["while", "if", "print", "label"]:
        if currtoken[0] == "while":
            # ["while", [condition], [statementlist]]
            consume("while")
            newstmt = ["while"]
            newstmt.append(doCondition())
            newstmt.append(doStatementList())
            consume("endwhile")
        elif currtoken[0] == "if":
            # ["if", [condition], [then part], [else part]]
            consume("if")
            newstmt = ["if"]
            newstmt.append(doCondition())
            newstmt.append(doStatementList())
            if currtoken[0] == "else":
                consume("else")
                newstmt.append(doStatementList())
            consume("endif")
        elif currtoken[0] == "print":
            # ["print", [expression]]
            consume("print")
            newstmt = ["print"]
            newstmt.append(doExpression())
        elif currtoken[0] == "label":
            # ["=", [expression], [expression]]
            label = [currtoken[1]]
            nextToken()
            consume("=")
            newstmt = ["="]
            newstmt.append(label)
            newstmt.append(doExpression())
        else:
            print "invalid statement: " + currtoken[0]
        stmts.append(newstmt)
    return stmts

def doCondition():
    exp = doExpression()
    # ["==|!=", [left side], [right side]]
    if currtoken[0] in ["==", "!="]:
        retval = [currtoken[0]]
        retval.append(exp)
        nextToken()
        retval.append(doExpression())
    else:
        print "expected == or != not found"
    return retval
    
def doExpression():
    term = doTerm()
    # carry the term in case there's no +|-
    exp = term
    # ["+|-", [left side], [right side]]
    while currtoken[0] in ["+", "-"]:
        exp = [currtoken[0]]
        nextToken()
        exp.append(term)
        exp.append(doExpression())
    return exp

def doTerm():
    if currtoken[0] == "label":
        retval = currtoken[1]
        nextToken()
    elif currtoken[0] == "digit":
        retval = currtoken[2]
        nextToken()
    return [retval]

#****************** Interpreter ************************

stack = []

def execStatementList(pgm):
    for stmt in pgm:
        execStatement(stmt)
        
def execStatement(stmt):
    if stmt[0] == "while":
        execCondition(stmt[1])
        while stack.pop():
            execStatementList(stmt[2])
            execCondition(stmt[1])
    elif stmt[0] == "if":
        execCondition(stmt[1])
        if stack.pop():
            execStatementList(stmt[2])
        elif len(stmt) == 4:
            execStatementList(stmt[3])
    elif stmt[0] == "=":
        execExpression(stmt[2])
        symboltable[stmt[1][0]] = stack.pop()
    elif stmt[0] == "print":
        execExpression(stmt[1])
        print "output:" + str(stack.pop())
    else:
        print "invalid statement"
    
def execCondition(cond):
    execExpression(cond[1])
    execExpression(cond[2])
    if cond[0] == "==":
        stack.append(stack.pop() == stack.pop())
    elif cond[0] == "!=":
        stack.append(stack.pop() != stack.pop())

def execExpression(exp):
    if len(exp) == 3:
        execExpression(exp[1])
        execExpression(exp[2])
        if exp[0] == "+":
            stack.append(stack.pop() + stack.pop())
        else:
            stack.append(stack.pop() - stack.pop())
    else:
        if type(exp[0]) == int:
            stack.append(exp[0])
        else:
            stack.append(symboltable[exp[0]])
