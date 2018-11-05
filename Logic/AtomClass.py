from Logic.OperatorClasses import NegationFormula
from Logic.OperatorClasses import ConjunctionFormula, DisjunctionFormula
from Logic.OperatorClasses import ImplicationFormula, BiconditionalFormula


class Atom:
    def __init__(self, name):
        if isinstance(name, Atom):
            self.name = name.name
        else:
            self.name = str(name)

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, (Atom, NegationFormula, ConjunctionFormula, DisjunctionFormula,
                                  ImplicationFormula, BiconditionalFormula)):
            print(other)
            raise TypeError
        elif isinstance(other, Atom):
            return self.name == other.name
        elif isinstance(other, NegationFormula) and isinstance(other.subformula, Atom):
            return False
        else:
            symbols = self.symbols() | other.symbols()
            models = [dict()]
            for symbol in symbols:
                new_models = []
                for model in models:
                    for true_false_value in (True, False):
                        model[symbol] = true_false_value
                        new_models.append(model.copy())
                models = new_models
            for mdl in models:
                if self.pl_true(mdl) != other.pl_true(mdl):
                    return False
            else:
                return True

    def pl_true(self, model):
        if self.name in model:
            return model[self.name]
        else:
            return None

    def symbols(self):
        return {self.name}