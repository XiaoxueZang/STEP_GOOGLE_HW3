import sys
def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta *= 0.1
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def readPlus(line, index):
    token = {'type': 'PLUS','priority': 1}
    return token, index + 1


def readMinus(line, index):
    token = {'type': 'MINUS', 'priority': 1}
    return token, index + 1

def readMulti(line, index):
    token = {'type': 'MULTI', 'priority': 2}
    return token, index + 1

def readDivide(line, index):
    token = {'type': 'DIVIDE', 'priority': 2}
    return token, index + 1

def readLeftBracket(line, index):
    token =  {'type': 'LEFTBRACKET'}
    return token, index +1

def readRightBracket(line, index):
    token = {'type': 'RIGHTBRACKET','priority': 1}
    return token, index+1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMulti(line, index)
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
        elif line[index] == '(':
            (token, index) = readLeftBracket(line, index)
        elif line[index] == ')':
            (token, index) = readRightBracket(line, index)
        else:
            print 'Invalid character found: ' + line[index]
            sys.exit(1)
        tokens.append(token)
    return tokens

def calculate(operator, num1, num2):
    if operator['type']=='PLUS':
        return num1['number']+num2['number']
    elif operator['type']=='MINUS':
        return num1['number']-num2['number']
    elif operator['type']=='MULTI':
        return num1['number']*num2['number']
    elif operator['type']=='DIVIDE':
        return float(num1['number'])/num2['number']
    else:
        sys.exit('mistake occurs in function calculate. No valid operator found')

# if brackets are used, pick out the bracket part and do the calculation of that part first
# and return the result of the bracket part
def evaluate(tokens):
    stackNum = []
    stackOper = []
    newTokens = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            stackNum.append(tokens[index])
            index +=1
        elif tokens[index]['type']=='LEFTBRACKET':# if the token is '('
            numOfBracket = 1
            #numOfbracket is to search for the end of the corresponding ')'
            newTokens = []
            while numOfBracket!=0:
                index = index +1
                if tokens[index]['type'] == 'LEFTBRACKET':
                    numOfBracket+=1
                elif tokens[index]['type'] == 'RIGHTBRACKET':
                    numOfBracket-=1
                newTokens.append(tokens[index])
            index +=1
            calculationOfBracket = evaluate(newTokens)#calculate the result of the part in '()'
            stackNum.append({'type': 'NUMBER', 'number':calculationOfBracket})

        elif tokens[index]['type'] in ['PLUS', 'MINUS', 'MULTI', 'DIVIDE','RIGHTBRACKET']:
            if stackOper == [] or tokens[index]['priority'] > stackOper[-1]['priority']:
                stackOper.append(tokens[index])
                index +=1
            elif tokens[index]['priority'] <= stackOper[-1]['priority'] :
                num2 = stackNum.pop()
                num1 = stackNum.pop()
                operatorNow = stackOper.pop()
                stackNum.append({'type': 'NUMBER', 'number':calculate(operatorNow, num1, num2)})
        else:
              sys.exit("Invalid syntax")

    if len(stackNum)!= 1 or len(stackOper)!=1:
        print 'the stackOper is {0}'.format(stackOper)
        print 'the stackNum is {0}'.format(stackNum)
        sys.exit('the calculation is wrong')
    return stackNum[0]['number']



while True:
    print 'no space is allowed > '
    line = raw_input()
    tokens = tokenize(line)
    tokens.append({'type': 'PLUS','priority' : 1})
    answer = evaluate(tokens)
    print "answer = %f\n" % answer
