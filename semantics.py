"""The goal in this module is to define functions associated with the semantics of formulas in propositional logic. """


from formula import *
from functions import atoms


def truth_value(formula, interpretation):
    """Determines the truth value of a formula in an interpretation (valuation).
    An interpretation may be defined as dictionary. For example, {'p': True, 'q': False}.
    """
    
    if isinstance(formula, Atom):
        if formula.name not in interpretation:
            raise ValueError(f"{formula.name} not in interpretation.")
        return interpretation.get(formula.name)
    elif isinstance(formula, Not):
        return not truth_value(formula.inner, interpretation)
    elif isinstance(formula, And):
        return truth_value(formula.left, interpretation) and truth_value(formula.right, interpretation)
    elif isinstance(formula, Implies):
        return not truth_value(formula.left, interpretation) or truth_value(formula.right, interpretation)
    elif isinstance(formula, Or):
        return truth_value(formula.left, interpretation) or truth_value(formula.right, interpretation)


def is_logical_consequence(premises, conclusion):  # function TT-Entails? in the book AIMA.
    """Returns True if the conclusion is a logical consequence of the set of premises. Otherwise, it returns False."""
    
    symbols = atoms(conclusion)
    for formula in premises:
        symbols = symbols.union(atoms(formula))
    
    symbols = [ symb.name for symb in symbols ]

    def PL_TRUE(KB, model):
        for sen in KB:
            if not truth_value(sen, model): return False
        return True
    
    def TT_CHECK_ALL(KB, a, symbols, model):
        if len(symbols) == 0:
            if PL_TRUE(KB, model):
                return PL_TRUE([a], model)
            else:
                return True
        else:
            p = symbols[0]
            rest = symbols[1:]
            return (TT_CHECK_ALL(KB, a, rest, {**model, p : True})
                    and TT_CHECK_ALL(KB, a, rest, {**model, p : False}))

    return TT_CHECK_ALL(premises, conclusion, symbols, {})

def is_logical_equivalence(formula1, formula2):
    """Checks whether formula1 and formula2 are logically equivalent."""
    
    symbols = atoms(formula1)
    symbols = [ formula.name for formula in symbols ]

    def check_both(form1, form2, symbols, model):
        if len(symbols) == 0:
            return truth_value(form1, model) == truth_value(form2, model)
        p = symbols[0]
        rest = symbols[1:]
        return (check_both(form1, form2, rest, {**model, p : True})
                and check_both(form1, form2, rest, {**model, p : False}))

    return check_both(formula1, formula2, symbols, {})


def is_valid(formula):
    """Returns True if formula is a logically valid (tautology). Otherwise, it returns False"""

    symbols = atoms(formula)
    symbols = [symb.name for symb in symbols]

    def check_all(form, symbols, model):
        if len(symbols) == 0:
            return truth_value(form, model)
        p = symbols[0]
        rest = symbols[1:]
        return (check_all(form, rest, {**model, p : True}) and
                check_all(form, rest, {**model, p : False}))
    
    return check_all(formula, symbols, {})


def satisfiability_brute_force(formula):
    """Checks whether formula is satisfiable.
    In other words, if the input formula is satisfiable, it returns an interpretation that assigns true to the formula.
    Otherwise, it returns False."""

    symbols = atoms(formula)
    symbols = [symb.name for symb in symbols]

    def check_all(form, symbols, model):
        if len(symbols) == 0:
            return model if truth_value(form, model) else False
        p = symbols[0]
        rest = symbols[1:]
        left = check_all(form, rest, {**model, p : True})
        return left if left else check_all(form, rest, {**model, p : False})
    
    return check_all(formula, symbols, {})