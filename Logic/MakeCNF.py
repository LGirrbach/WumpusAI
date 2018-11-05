from Logic.OperatorClasses import Atom
from Logic.OperatorClasses import NegationFormula
from Logic.OperatorClasses import ConjunctionFormula, DisjunctionFormula
from Logic.OperatorClasses import ImplicationFormula, BiconditionalFormula
from Logic.CNFClass import CNFSentence

from copy import deepcopy

def biconditional_replacement(formula):
    if isinstance(formula, Atom):
        return formula
    elif isinstance(formula, NegationFormula):
        formula.subformula = biconditional_replacement(formula.subformula)
        return formula
    else:
        subformula1 = biconditional_replacement(formula.subformula1)
        subformula2 = biconditional_replacement(formula.subformula2)
        if isinstance(formula, BiconditionalFormula):
            return ConjunctionFormula(
                ImplicationFormula(subformula1, subformula2), ImplicationFormula(subformula2, subformula1)
            )
        else:
            formula.subformula1 = subformula1
            formula.subformula2 = subformula2
            return formula


def implication_replacement(formula):
    if isinstance(formula, Atom):
        return formula
    elif isinstance(formula, NegationFormula):
        formula.subformula = implication_replacement(formula.subformula)
        return formula
    else:
        subformula1 = implication_replacement(formula.subformula1)
        subformula2 = implication_replacement(formula.subformula2)
        if isinstance(formula, ImplicationFormula):
            return DisjunctionFormula(
                NegationFormula(subformula1), subformula2
            )
        else:
            formula.subformula1 = subformula1
            formula.subformula2 = subformula2
            return formula


def move_negation_inwards(formula):
    if isinstance(formula, Atom):
        return formula
    elif isinstance(formula, NegationFormula):
        subformula = formula.subformula
        if isinstance(subformula, NegationFormula):
            return move_negation_inwards(subformula.subformula)
        elif isinstance(subformula, Atom):
            return formula
        elif isinstance(subformula, ConjunctionFormula):
            new_formula =  DisjunctionFormula(
                NegationFormula(move_negation_inwards(subformula.subformula1)),
                NegationFormula(move_negation_inwards(subformula.subformula2))
            )
            return move_negation_inwards(new_formula)
        elif isinstance(subformula, DisjunctionFormula):
            new_formula = ConjunctionFormula(
                NegationFormula(move_negation_inwards(subformula.subformula1)),
                NegationFormula(move_negation_inwards(subformula.subformula2))
            )
            return move_negation_inwards(new_formula)
        else:
            raise TypeError
    else:
        formula.subformula1 = move_negation_inwards(formula.subformula1)
        formula.subformula2 = move_negation_inwards(formula.subformula2)
        return formula


def distibutive_replacement(formula):
    if isinstance(formula, Atom):
        return formula
    elif isinstance(formula, NegationFormula):
        return NegationFormula(distibutive_replacement(formula.subformula))
    elif isinstance(formula, DisjunctionFormula):
        if isinstance(formula.subformula2, ConjunctionFormula):
            new_formula = ConjunctionFormula(
                DisjunctionFormula(formula.subformula1, formula.subformula2.subformula1),
                DisjunctionFormula(formula.subformula1, formula.subformula2.subformula2)
            )
            return distibutive_replacement(new_formula)
        elif isinstance(formula.subformula1, ConjunctionFormula):
            new_formula = ConjunctionFormula(
                DisjunctionFormula(formula.subformula1.subformula1, formula.subformula2),
                DisjunctionFormula(formula.subformula1.subformula2, formula.subformula2)
            )
            return distibutive_replacement(new_formula)
        else:
            formula.subformula1 = distibutive_replacement(formula.subformula1)
            formula.subformula2 = distibutive_replacement(formula.subformula2)
            if isinstance(formula.subformula1, ConjunctionFormula) \
                or isinstance(formula.subformula2, ConjunctionFormula):
                return distibutive_replacement(formula)
            else:
                return formula
    elif isinstance(formula, ConjunctionFormula):
        formula.subformula1 = distibutive_replacement(formula.subformula1)
        formula.subformula2 = distibutive_replacement(formula.subformula2)
        return formula
    else:
        raise TypeError

def extract_literals(disjunction_formula):
    if isinstance(disjunction_formula, (Atom, NegationFormula)):
        return frozenset({disjunction_formula})
    elif isinstance(disjunction_formula, DisjunctionFormula):
        retval = extract_literals(disjunction_formula.subformula1) | extract_literals(disjunction_formula.subformula2)
        return frozenset(retval)
    else:
        raise TypeError


def extract_clauses(cnf_formula, convert_to_cnf=False):
    if convert_to_cnf:
        cnf_formula = make_cnf(cnf_formula, oldstyle=True)
    clauses = []
    if isinstance(cnf_formula, (Atom, NegationFormula)):
        clauses.append(frozenset({cnf_formula}))
    elif isinstance(cnf_formula, ConjunctionFormula):
        if isinstance(cnf_formula.subformula1, DisjunctionFormula):
            # print(type(cnf_formula.subformula1))
            clauses.append(extract_literals(cnf_formula.subformula1))
            clauses += extract_clauses(cnf_formula.subformula2)
        elif isinstance(cnf_formula.subformula2, DisjunctionFormula):
            clauses.append(extract_literals(cnf_formula.subformula2))
            clauses += extract_clauses(cnf_formula.subformula1)
        else:
            clauses += extract_clauses(cnf_formula.subformula1)
            clauses += extract_clauses(cnf_formula.subformula2)
    elif isinstance(cnf_formula, DisjunctionFormula):
        clauses.append(extract_literals(cnf_formula))
    else:
        raise NotImplementedError
    return frozenset(clauses)

def make_cnf(formula, oldstyle=False):
    if isinstance(formula, CNFSentence):
        return formula
    cnf_formula = deepcopy(formula)
    cnf_formula = biconditional_replacement(cnf_formula)
    cnf_formula = implication_replacement(cnf_formula)
    cnf_formula = move_negation_inwards(cnf_formula)
    cnf_formula = distibutive_replacement(cnf_formula)
    if oldstyle:
        return cnf_formula
    else:
        cnf_formula = extract_clauses(cnf_formula)
        return CNFSentence(cnf_formula)

if __name__ == '__main__':
    my_formula = BiconditionalFormula(
        'B11',
        DisjunctionFormula('P12', 'P21', 'P22')
    )
    my_formula = make_cnf(my_formula)
    print(my_formula)


