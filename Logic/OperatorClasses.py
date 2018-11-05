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


class NegationFormula:
    def __init__(self, formula):
        if isinstance(formula, str):
            self.__subformula = Atom(formula)
        else:
            self.__subformula = formula

    def __str__(self):
        return '~'+str(self.__subformula)

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        if not isinstance(other, (Atom, NegationFormula, ConjunctionFormula, DisjunctionFormula,
                                  ImplicationFormula, BiconditionalFormula)):
            raise TypeError
        elif isinstance(other, Atom):
            return False
        elif isinstance(other, NegationFormula):
            return self.__subformula == other.subformula
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
        return not self.__subformula.pl_true(model)

    def symbols(self):
        return self.__subformula.symbols()

    def get_subformula(self):
        return self.__subformula

    def set_subformula(self, formula):
        if isinstance(formula, (Atom, NegationFormula, ConjunctionFormula, DisjunctionFormula,
                                BiconditionalFormula, ImplicationFormula)):
            self.__subformula = formula
    subformula = property(get_subformula, set_subformula)


class Formula:
    def __init__(self, formula_type, repr_symb, funct, *subformulas):
        self.__subformula1 = subformulas[-1]
        if len(subformulas) > 2:
            self.__subformula2 = formula_type(*subformulas[:-1])
        else:
            self.__subformula2 = subformulas[0]
        if isinstance(self.__subformula1, str):
            self.__subformula1 = Atom(self.__subformula1)
        if isinstance(self.__subformula2, str):
            self.__subformula2 = Atom(self.__subformula2)

        self.__subformula1, self.__subformula2 = self.__subformula2, self.__subformula1

        self.repr_symb = repr_symb
        self.ret_funct = funct

    def __str__(self):
        return "(" + str(self.__subformula1) + self.repr_symb + str(self.__subformula2) + ")"

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        if not isinstance(other, (Atom, NegationFormula, ConjunctionFormula, DisjunctionFormula,
                                  ImplicationFormula, BiconditionalFormula)):
            raise TypeError
        elif isinstance(other, Atom):
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
                    print(mdl, self.pl_true(mdl), other.pl_true(mdl))
                    return False
            else:
                return True

    def pl_true(self, model):
        return self.ret_funct(self.__subformula1, self.__subformula2, model)

    def symbols(self):
        return self.__subformula1.symbols() | self.__subformula2.symbols()

    def get_subformula1(self):
        return self.__subformula1

    def get_subformula2(self):
        return self.__subformula2

    def set_subformula1(self, formula):
        if isinstance(formula, (Atom, NegationFormula, ConjunctionFormula, DisjunctionFormula,
                                BiconditionalFormula, ImplicationFormula)):
            self.__subformula1 = formula
        else:
            raise TypeError

    def set_subformula2(self, formula):
        # if isinstance(formula, (Atom, NegationFormula, ConjunctionFormula, DisjunctionFormula,
        #                        BiconditionalFormula, ImplicationFormula)):
        self.__subformula2 = formula
        # else:
        #    raise TypeError

    subformula1 = property(get_subformula1, set_subformula1)
    subformula2 = property(get_subformula2, set_subformula2)


class ConjunctionFormula(Formula):
    def __init__(self, *subformulas):
        super().__init__(ConjunctionFormula, " and ", lambda a, b, model: a.pl_true(model) and b.pl_true(model),
                         *subformulas)


class DisjunctionFormula(Formula):
    def __init__(self, *subformulas):
        super().__init__(DisjunctionFormula, " or ", lambda a, b, model: a.pl_true(model) or b.pl_true(model),
                         *subformulas)

class ImplicationFormula(Formula):
    def __init__(self, *subformulas):
        super().__init__(ImplicationFormula, " => ", lambda a, b, model: (not a.pl_true(model)) or b.pl_true(model),
                         *subformulas)


class BiconditionalFormula(Formula):
    def __init__(self, *subformulas):
        super().__init__(BiconditionalFormula, " <=> ", lambda a, b, model: a.pl_true(model) == b.pl_true(model),
                         *subformulas)


if __name__ == '__main__':
    A = Atom('A')
    B = NegationFormula(A)
    print(NegationFormula(B) == NegationFormula(A))
    my_set = {A, B, DisjunctionFormula('C', 'D')}
    for x in (my_set - {NegationFormula(A)}):
        print(x)


