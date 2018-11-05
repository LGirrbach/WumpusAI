from Logic.OperatorClasses import *
from Logic.MakeCNF import extract_clauses

from itertools import product

class KB2:

    supportedFormulaTypes = (Atom, NegationFormula, ConjunctionFormula, DisjunctionFormula,
                             ImplicationFormula, BiconditionalFormula)

    def __init__(self):
        self.formulas = set()
        self.all_resolvents = set()

    def ask(self, query_formula):
        if not isinstance(query_formula, self.supportedFormulaTypes):
            raise  TypeError

        clauses_negated_query_formula = extract_clauses(NegationFormula(query_formula), convert_to_cnf=True)
        negation_is_consistent, _ = self.pl_resolution(clauses_negated_query_formula)
        return not negation_is_consistent

    def tell(self, new_formula):
        if not isinstance(new_formula, self.supportedFormulaTypes):
            raise TypeError

        if new_formula not in self.formulas:
            clauses_new_formula = extract_clauses(new_formula, convert_to_cnf=True)
            new_formula_is_consistent, computed_resolvents = self.pl_resolution(clauses_new_formula)
            if new_formula_is_consistent:
                self.all_resolvents = computed_resolvents
                self.formulas.add(new_formula)
                # print('Formel:', new_formula, 'wurde hinzugefügt.')
            else:
                pass
                # print('Formel:', new_formula, 'wurde nicht hinzugefügt.')


    def pl_resolution(self, new_clauses):
        def pl_resolve(clause_i, clause_j):
            resolvents_ij = set()
            for literal in clause_i:
                if NegationFormula(literal) in clause_j:
                    resolvent = frozenset((clause_i - {literal}) | (clause_j - {NegationFormula(literal)}))
                    if not is_tautology(resolvent):
                        resolvents_ij.add(resolvent)
            return resolvents_ij

        def is_tautology(clause):
            for literal_clause in clause:
                if NegationFormula(literal_clause) in clause:
                    return True

        all_clauses = self.all_resolvents.copy()
        old_new = new_clauses
        while True:
            new = set()
            # print(len(new_clauses), len(all_clauses))
            for clause_1, clause_2 in product(new_clauses, all_clauses | old_new):
                resolvents = pl_resolve(clause_1, clause_2)
                # for cl in resolvents:
                #     print('{', end=' ')
                #     for lit in cl:
                #         print(lit, end=', ')
                #     print('}')
                if set() in resolvents:
                    return False, all_clauses
                new |= resolvents
            if new <= all_clauses:
                return True, all_clauses | new_clauses
            all_clauses |= new_clauses
            new_clauses = new - all_clauses
            old_new = new - all_clauses


if __name__ == '__main__':
    kb = KB2()
    R1 = NegationFormula('P11')
    R2 = BiconditionalFormula('B11', DisjunctionFormula('P12', 'P21'))
    R3 = BiconditionalFormula('B21', DisjunctionFormula('P11', 'P21', 'P31'))
    R4 = NegationFormula('B11')
    R5 = Atom('B21')

    kb.tell(R1)
    kb.tell(R2)
    kb.tell(R3)
    kb.tell(R4)
    kb.tell(R5)

    print(kb.ask(NegationFormula('P12')))




