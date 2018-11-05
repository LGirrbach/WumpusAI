def tt_check_all(kb, alpha, symbols, model):
    if not symbols:
        if kb.pl_true(model):
            return alpha.pl_true(model)
        else:
            return True
    else:
        p = symbols.pop()
        model[p] = True
        res1 = tt_check_all(kb, alpha, symbols.copy(), model)
        model[p] = False
        res2 = tt_check_all(kb, alpha, symbols.copy(), model)
        return res1 and res2


def tt_entails(knowledge_base, formula):
    return tt_check_all(knowledge_base, formula, knowledge_base.symbols | formula.symbols(), dict())


if __name__ == '__main__':
    pass