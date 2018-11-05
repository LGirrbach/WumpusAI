class Formula:
    def __init__(self, mode, *formulas):
        if mode.lower() not in ('negation', 'conjunction', 'disjunction',
                                'implication', 'biconditional', 'atom'):
            raise NotImplementedError
        if mode.lower() in ('negation', 'atom') and len(formulas) != 1:
            raise TypeError

        self.mode = mode
        self.subformulas = formulas

    def __str__(self):
        operator_dict = {
            'negation': '~',
            'conjunction': ') and ',
            'disjunction': ') or ',
            'implication': ') => ',
            'biconditional': ') <=> ',
            'atom': ''
        }
        if self.mode == 'negation':
            return operator_dict[self.mode] + str(self.subformulas[0])
        elif self.mode == 'atom':
            return str(self.subformulas[0])
        else:
            return '(' * (len(self.subformulas)) +\
                   operator_dict[self.mode].join(str(proposition) for proposition in self.subformulas) + ')'

    def symbols(self):
        if self.mode == 'atom':
            return {str(self.subformulas[0])}
        else:
            symbols = set()
            for subformula in self.subformulas:
                symbols |= subformula.symbols()
            return symbols

    def pl_true(self, model):
        if self.mode == 'negation':
            return not self.subformulas[0].pl_true(model)
        elif self.mode == 'atom':
            return model[str(self.subformulas[0])]
        elif self.mode == 'conjunction':
            return all([formula.pl_true(model) for formula in self.subformulas])
        elif self.mode == 'disjunction':
            return any([formula.pl_true(model) for formula in self.subformulas])
        elif self.mode == 'implication':
            current_val = self.subformulas[0].pl_true(model)
            for formula in self.subformulas[1:]:
                next_val = formula.pl_true(model)
                if not current_val:
                    current_val = True
                elif not next_val:
                    current_val = False
            return current_val
        elif self.mode == 'biconditional':
            current_val = self.subformulas[0].pl_true(model)
            for formula in self.subformulas[1:]:
                if formula.pl_true(model) == current_val:
                    current_val = True
                else:
                    current_val = False
            return current_val



if __name__ == '__main__':
    my_prop = Formula('biconditional', Formula('conjunction', Formula('atom', 'A'), Formula('atom', 'B')),
                      Formula('atom', 'B'))
    for x in (True, False):
        for y in (True, False):
            d = {'A': x, 'B': y}
            print(x, y, 'ergibt:', my_prop.pl_true(d))
    print(my_prop.symbols())
