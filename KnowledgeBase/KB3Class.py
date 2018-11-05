from Logic.CNFClass import CNFSentence, Clause
from Logic.MakeCNF import make_cnf
from Logic.OperatorClasses import Atom
from Logic.OperatorClasses import NegationFormula
from Logic.OperatorClasses import ConjunctionFormula, DisjunctionFormula
from Logic.OperatorClasses import ImplicationFormula, BiconditionalFormula

from copy import deepcopy

class KB3:
    def __init__(self):
        self.all_resolvents = dict()
        self.all_resolvents_set = set()

    def ask(self, query_formula):
        negative_query_formula = make_cnf(NegationFormula(query_formula))
        query_formula = make_cnf(query_formula)
        if all((clause in self.all_resolvents_set) for clause in query_formula.clauses()):
            return True
        found_inconsistency, changes = self.resolution(negative_query_formula)

        for clause in changes:
            self.all_resolvents_set.remove(clause)
            for literal in clause.allSymbols:
                self.all_resolvents[literal].remove(clause)

        return found_inconsistency

    def tell(self, new_formula):
        new_formula = make_cnf(new_formula)
        found_inconsistency, changes = self.resolution(new_formula)
        if found_inconsistency:
            for clause in changes:
                self.all_resolvents_set.remove(clause)
                for literal in clause.allLiterals:
                    self.all_resolvents[literal].remove(clause)

            print('Inkonsistent mit:', new_formula)

    def resolution(self, cnf_formula):
        def resolve(clause_i, clause_j, literal_clause_i):
            return (clause_i - literal_clause_i) + (clause_j - literal_clause_i.negate())

        def is_tautology(taut_clause):
            for ltrl in taut_clause:
                if ltrl.negate() in taut_clause:
                    return True
            else:
                return False

        new_resolvents = {clause for clause in cnf_formula.clauses()}
        new_clauses = set()
        while True:
            # print()
            for clause in new_resolvents:
                for literal in clause.allLiterals:
                    if literal in self.all_resolvents:
                        self.all_resolvents[literal].add(clause)
                    else:
                        self.all_resolvents[literal] = {clause}

            new = set()
            for new_clause in new_resolvents:
                if new_clause in self.all_resolvents_set:
                    continue
                for literal in new_clause.allLiterals:
                    if literal not in self.all_resolvents:
                        self.all_resolvents[literal] = set()
                    negated_literal = literal.negate()
                    if negated_literal not in self.all_resolvents:
                        self.all_resolvents[negated_literal] = set()
                    # print(negated_literal, self.all_resolvents[negated_literal])
                    for old_clause in self.all_resolvents[negated_literal]:
                        resolvent = resolve(new_clause, old_clause, literal)
                        if not resolvent:
                            print('Stelle1', resolvent)
                            return True, new_clauses # Leere Klausel -> Widerspruch/Inkonsistent
                        if is_tautology(resolvent):
                            continue
                        if resolvent not in (self.all_resolvents_set | new_resolvents | new):
                            new.add(resolvent)
            print(len(new))
            if new <= (self.all_resolvents_set | new_resolvents):
                return False, new_clauses # Alle Resolventen generiert -> Kein Widerspruch/Inkonsistenz
            self.all_resolvents_set |= new_resolvents
            new_clauses |= new_resolvents
            new_resolvents = new



if __name__ == '__main__':
    kb = KB3()
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


