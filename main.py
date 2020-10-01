import sys

import ply.lex as lex

tokens = [
    'OPER', 'SEPR', 'ID'
]

t_OPER = r'(:-)|(,)|(;)'

t_SEPR = r'(\.)|(\()|(\))'

t_ID = r'[a-zA-Z_]*'

t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def to_lex(text: str):
    lexer = lex.lex()
    lexer.input(text)
    while True:
        token = lexer.token()
        if not token:
            while True:
                yield None
        token.lexpos = token.lexpos - text.rfind('\n', 0, token.lexpos)
        yield token


class parser:

    def __init__(self, string):
        self.lexer = to_lex(string)
        self.tok = next(self.lexer)
        while self.tok is not None:
            answer = self.DEF()
            if not answer:
                return
        print("OK")

    def accept(self, node):
        if self.tok is None:
            return False
        elif self.tok.value == node:
            self.tok = next(self.lexer)
            return True
        return False

    def expect(self, node):
        if self.tok.value == node:
            self.tok = next(self.lexer)
            return True
        print("Expected", node, f'at line: {self.tok.lineno}, 'f'pos: {self.tok.lexpos}')
        return False

    def HEAD(self):
        if self.accept('('):
            if self.DISJ() and self.expect(')'):
                return True
            return False
        elif str(self.tok.type) != 'ID':
            print(f'Expected head at line: {self.tok.lineno}, 'f'pos: {self.tok.lexpos}')
            return False
        self.tok = next(self.lexer)
        return True

    def DISJ(self):
        if not self.CONJ():
            return False
        elif self.accept(';'):
            if not self.DISJ():
                return False
            return True
        return True

    def CONJ(self):
        if not self.HEAD():
            return False
        elif self.accept(','):
            if not self.CONJ():
                return False
            return True
        return True

    def DEF(self):
        if not self.HEAD():
            return False
        elif self.accept(':-'):
            if self.DISJ() and self.expect('.'):
                return True
            return False
        elif not self.expect('.'):
            return False
        return True


def main(name):
    with open(name, 'r') as file:
        data = file.read()
    parser(data)


if __name__ == "__main__":
    main(sys.argv[1])
