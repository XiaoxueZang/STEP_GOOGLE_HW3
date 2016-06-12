import sys
#readNumber module is the same with the sample
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

#add priority to each operators.
#'*' and '/' have high priority(priority =2)
# than '+' and '-'(priority = 1) in calculation
def readPlus(line, index):
    token = {'type': 'PLUS','priority': 1}
    return token, index + 1

def readMinus(line, index):
    token = {'type': 'MINUS', 'priority': 1}
    return token, index + 1

#readMulti module is to read '*'
def readMulti(line, index):
    token = {'type': 'MULTI', 'priority': 2}
    return token, index + 1

#readDivide module is to read '/'
def readDivide(line, index):
    token = {'type': 'DIVIDE', 'priority': 2}
    return token, index + 1

#divide the input into tokens
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
        else:
            sys.exit('Invalid character found: {0}'.format(line[index]))
        tokens.append(token)
    return tokens

#this module is to do the calculation "num1 operator num2"
#and return the result of calculation
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
        sys.exit('mistake occurs in module calculate. No valid operator found')

#analyze tokens
def evaluate(tokens):
    stackNum = []#stack to store numbers
    stackOper = []#stack to store operators
    newTokens = []
    index = 0
    while index < len(tokens):
        #if isnumber push it to the stack of number
        if tokens[index]['type'] == 'NUMBER':
            stackNum.append(tokens[index])
            index +=1
        #if isoperator
        if tokens[index]['type'] != 'NUMBER':

            #if the stack of operator is empty or
            #the operator's priority is higher than the previous operator,
            #then push it to the stack of operator
            if not stackOper or tokens[index]['priority'] > stackOper[-1]['priority']:
                stackOper.append(tokens[index])
                index +=1

            #otherwise do the calculation of the numbers already stored in stack
            elif tokens[index]['priority'] <= stackOper[-1]['priority']:

                num2 = stackNum.pop()
                num1 = stackNum.pop()
                operatorPre = stackOper.pop()
                #pop out previous operator, do the calculation and push the result to stackNum
                stackNum.append({'type': 'NUMBER', 'number':calculate(operatorPre, num1, num2)})
    #this is for debugging I need to make sure that at the end of calculation,
    #stackNum has one element, which contains the result
    #stackOper contained one element, which is dummy '+' I added (read while loop at the bottom)
    if len(stackNum)!= 1 or len(stackOper)!=1:
        print 'the stackOper is {0}'.format(stackOper)
        print 'the stackNum is {0}'.format(stackNum)
        sys.exit('the calculation is wrong')
    return stackNum[0]['number']


while True:
    print '> '
    line = raw_input()
    tokens = tokenize(line)
    tokens.append({'type': '+','priority' : 1})
    # append dummy operator'+' to tokens to mark the end.
    # 'type' could be any name or just 'END', but priority must be set to be the lowest number
    answer =evaluate(tokens)
    print "answer = %f\n" % answer
