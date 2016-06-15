#include <iostream>
#include <vector>
#include <stack>
using namespace std;

class unit{
public:
    unit(){};
    unit(double num, string tp){number = num; type = tp;}
    double number;
    string type;
};
void readNumber(string line, int &index, vector<shared_ptr<unit>> &tokens)
{
	double number;
    string::size_type sz;
    number = stod(line, &sz);
    index += sz;
    auto newUnit = make_shared<unit>();
    newUnit->number= number;
    (newUnit->type).append("NUMBER");
    tokens.push_back(newUnit);
}

void readPlus(vector<shared_ptr<unit>> &tokens, int& index){
    auto newUnit = make_shared<unit>();
    newUnit->number= 1;
    (newUnit->type)+="+";
    tokens.push_back(newUnit);
    index = index + 1;
}

void readMinus(vector<shared_ptr<unit>> &tokens, int& index){
    auto newUnit = make_shared<unit>();
    newUnit->number= 1;
    (newUnit->type)+='-';
    tokens.push_back(newUnit);
    index = index + 1;
}

void readMulti(vector<shared_ptr<unit>> &tokens, int& index){
    auto newUnit = make_shared<unit>();
    newUnit->number= 2;
    (newUnit->type)+='*';
    tokens.push_back(newUnit);
    index = index + 1;
}

void readDivide(vector<shared_ptr<unit>> &tokens, int& index){
    auto newUnit = make_shared<unit>();
    newUnit->number= 2;
    (newUnit->type)+='/';
    tokens.push_back(newUnit);
    index = index + 1;
}

void readLeftBracket(vector<shared_ptr<unit>> &tokens,int& index){
    auto newUnit = make_shared<unit>();
    (newUnit->type).append("LEFTBRACKET");
    tokens.push_back(newUnit);
    index = index + 1;
}

void readRightBracket(vector<shared_ptr<unit>> &tokens,int& index){
    auto newUnit = make_shared<unit>();
    (newUnit->type).append("RIGHTBRACKET");
    tokens.push_back(newUnit);
    index = index + 1;
}

void tokenize(vector<shared_ptr<unit>> &tokens, string str){
    int index = 0;
    while (index<str.length()){
        if(isdigit(str[index])){
            readNumber(str.substr(index), index, tokens);
        }
        else {
            switch (str[index]) {
                case ('+'):
                    readPlus(tokens, index);
                    break;
                case ('-'):
                    readMinus(tokens, index);
                    break;
                case ('*'):
                    readMulti(tokens, index);
                    break;
                case ('/'):
                    readDivide(tokens, index);
                    break;
                case ('('):
                    readLeftBracket(tokens, index);
                    break;
                case (')'):
                    readRightBracket(tokens, index);
                    break;
                default:
                    cout << str[index] << endl;
                    cout << "invalid input here" << endl;
                    exit(1);
            }
        }
    }
}




double calculate(double num1, double num2, char oper) {
    switch(oper) {
        case ('+'):
            return num1 + num2;
        case ('-'):
            return num1 - num2;
        case ('*'):
            return num1 * num2;
        case ('/'):
            return num1 / num2;
    }
    cout << "invalid operator" << endl;
    exit(-1);
}

double evaluate(vector<shared_ptr<unit>>& tokens, int& index) {
    stack<double> stackNum;
    stack<pair<char, int>> stackOper;
    int numOfBracket = 0;
    while(tokens[index]!=NULL){
        if(tokens[index]->type == "NUMBER"){
            stackNum.push(tokens[index]->number);
            index += 1;
        }
        else if(tokens[index]->type == "LEFTBRACKET"){
            numOfBracket += 1;
            index += 1;
            double answerOfBracket = evaluate(tokens, index);
            stackNum.push(answerOfBracket);
        }//if it is the '(', then start the new calculation of the part after '('
            //if it is the ')', then it means the finish of bracket and return the value inside the bracket
            else if(tokens[index]->type == "RIGHTBRACKET"){
            double num2 = stackNum.top();
            stackNum.pop();
            double num1 = stackNum.top();
            stackNum.pop();
            stackNum.push(calculate(num1, num2, stackOper.top().first));
            stackOper.pop();
            index += 1;
            return stackNum.top();
        }
        else {
            if(stackOper.empty()){
                stackOper.push(make_pair((tokens[index]->type)[0],int(tokens[index]->number)));
                index += 1;
                continue;
            }
            else if (stackOper.top().second< (tokens[index]->number)) {
                stackOper.push(make_pair((tokens[index]->type)[0],int(tokens[index]->number)));
                index += 1;
                continue;
            }
            else if (stackOper.top().second>= (tokens[index]->number)){
                double num2 = stackNum.top();
                stackNum.pop();
                double num1 = stackNum.top();
                stackNum.pop();
                stackNum.push(calculate(num1, num2, stackOper.top().first));
                stackOper.pop();
            }
        }
    }
    if (stackNum.size()!=1 || stackOper.size()!=1){
        cout << stackNum.top() << endl;
        cout << "the calculation is wrong" << endl;
        exit(1);
    }
   return stackNum.top();
}
int main ()
{
    while(true) {
        string line;
        cout << "<";
        cin >> line;
        vector<shared_ptr<unit>> tokens;
        tokenize(tokens, line);
        int index = 0;
        shared_ptr<unit> end = make_shared<unit>(unit(1,"+"));
        tokens.push_back(end);
        double answer = evaluate(tokens, index);
        cout << answer << endl;
    }
}
