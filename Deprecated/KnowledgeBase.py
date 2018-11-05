from Logic.OperatorClasses import *
from Logic.MakeCNF import extract_clauses

from itertools import product
from functools import lru_cache
# from time import sleep


class KB:
    def __init__(self, *formulas):
        self.supported_formula_types = (Atom, NegationFormula, ConjunctionFormula, DisjunctionFormula,
                                        ImplicationFormula, BiconditionalFormula)
        self.__formulas = {formula for formula in formulas if isinstance(formula, self.supported_formula_types)}
        self._symbols = set()
        for formula in self.__formulas:
            self._symbols |= formula.symbols()

        self.__cnf_clauses = set()
        for formula in self.__formulas:
            self.__cnf_clauses |= extract_clauses(formula)

    def ask(self, alpha):
        @lru_cache(maxsize=None)
        def pl_resolve(clause_i, clause_j):
            resolvents_ij = set()
            for literal in clause_i:
                if NegationFormula(literal) in clause_j:
                    resolvent = frozenset((clause_i - {literal}) | (clause_j - {NegationFormula(literal)}))
                    resolvents_ij.add(resolvent)
            return resolvents_ij

        if isinstance(alpha, str):
            alpha = Atom(alpha)
        if alpha in self.__formulas:
            return True

        alpha_symbols = alpha.symbols()
        # relevant_formulas = {formula for formula in self.__formulas if
        #                     any((symb in alpha_symbols) for symb in formula.symbols())}
        kb_and_alpha = self.__formulas | {NegationFormula(alpha)}
        kb_and_alpha = ConjunctionFormula(*tuple(kb_and_alpha))
        old_clauses = extract_clauses(kb_and_alpha)
        new_clauses = old_clauses.copy()
        all_clauses = old_clauses.copy()
        while True:
            print("Neue Runde", len(new_clauses))
            new = set()
            for clause_1, clause_2 in product(old_clauses, new_clauses):
                resolvents = pl_resolve(clause_1, clause_2)
                if frozenset() in resolvents:
                    return True
                new |= resolvents

            if new <= all_clauses:
                return False
            old_clauses |= new_clauses
            all_clauses |= new_clauses | new
            new_clauses = new

    def tell(self, formula):
        if not isinstance(formula, self.supported_formula_types):
            if isinstance(formula, str):
                formula = Atom(formula)
            else:
                raise TypeError
        if formula not in self.__formulas:
            self.__formulas.add(formula)
        self._symbols |= formula.symbols()
        self.__cnf_clauses |= extract_clauses(formula)

    def pl_true(self, model):
        return all(formula.pl_true(model) for formula in self.__formulas)

    def symbols(self):
        return self._symbols.copy()

    Symbols = property(symbols)


if __name__ == '__main__':
    A1 = BiconditionalFormula('B11', DisjunctionFormula('P12', 'P21'))
    A2 = NegationFormula('B11')
    Alpha = NegationFormula('B1')

    my_kb = KB(A1, A2)
    print(my_kb.ask(Alpha))
