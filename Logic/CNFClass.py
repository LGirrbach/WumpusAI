from Logic.OperatorClasses import Atom
from Logic.OperatorClasses import NegationFormula

from functools import reduce


class Literal:
    def __init__(self, literal):
        if isinstance(literal, Atom):
            self.atomic_variable_name = literal.name
            self.negative = False
        elif isinstance(literal, NegationFormula):
            if isinstance(literal.subformula, Atom):
                self.atomic_variable_name = literal.subformula.name
                self.negative = True
            else:
                print('Kein Literal:', literal)
                raise TypeError
        else:
            print('Kein Literal:', literal)
            raise TypeError

    def __str__(self):
        if self.negative:
            return '~' + self.atomic_variable_name
        else:
            return self.atomic_variable_name

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def symbols(self):
        return {self.atomic_variable_name}

    def negate(self):
        if self.negative:
            return Literal(Atom(self.atomic_variable_name))
        else:
            return Literal(NegationFormula(self.atomic_variable_name))


class Clause:
    literalClasses = (Atom, NegationFormula, Literal)

    def __init__(self, *literals):
        if any(not isinstance(literal, Clause.literalClasses) for literal in literals):
            print('Ungültige Literale:')
            for literal in literals:
                print(literal, type(literal), isinstance(literal, self.literalClasses), end=', ')
            print(type(literals))
            print()
            raise TypeError

        self.__literals = frozenset((Literal(literal) if not isinstance(literal, Literal) else literal)
                                    for literal in literals)
        self.__symbols = reduce(
            lambda symbs, lit: symbs | lit.symbols(),
            self.__literals,
            set()
        )
        # self.hash_string = ''.join(sorted(str(literal) for literal in self.__literals))

    def __str__(self):
        return '{' + ', '.join(str(literal) for literal in self.__literals) + '}'

    def __repr__(self):
        return str(self)

    def __iter__(self):
        for literal in self.__literals:
            yield literal

    def __hash__(self):
        return hash(self.__literals)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __contains__(self, item):
        return item in self.__literals

    def __bool__(self):
        return bool(self.__literals)

    def __sub__(self, other):
        if not isinstance(other, Literal):
            if isinstance(other, (Atom, NegationFormula)):
                other = Literal(other)
            else:
                print('Kein Literal:', other)
                raise TypeError
        return Clause(*tuple(self.__literals - {other}))

    def __add__(self, other):
        if isinstance(other, Clause):
            return Clause(*tuple(self.__literals | other.allLiterals))

    def literals(self):
        for literal in self.__literals:
            yield literal

    def get_literals(self):
        return self.__literals

    def symbols(self):
        return self.__symbols

    allSymbols = property(symbols)
    allLiterals = property(get_literals)


class CNFSentence:
    def __init__(self, clauses):
        self.__clauses = set()
        for clause in clauses:
            if isinstance(clause, Clause):
                self.__clauses.add(clause)
            else:
                try:
                    clause = Clause(*tuple(clause))
                    self.__clauses.add(clause)
                except TypeError:
                    print(clause)
                    raise TypeError
        self.__clauses = frozenset(self.__clauses)

    def __str__(self):
        return '{' + ', '.join(str(clause) for clause in self.__clauses) + '}'

    def __eq__(self, other):
        for clause in other.clauses():
            if clause not in self.__clauses:
                return False
        else:
            return True

    def __hash__(self):
        return hash(frozenset(self.__clauses))

    def __contains__(self, item):
        return item in self.__clauses

    def clauses(self):
        for clause in self.__clauses:
            yield clause


if __name__ == '__main__':
    my_clause1 = Clause(Atom('B11'), NegationFormula('C34'), Atom('A12'))
    my_clause2 = Clause(NegationFormula('S12'), Atom('K33'))
    print(my_clause1 == Clause(Atom('B11'), Atom('A12'), NegationFormula('C34')))
    print(my_clause1)
    print()
    print(my_clause1 - Atom('B11'))
    print()
    print(my_clause1 + my_clause2)




