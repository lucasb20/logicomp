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
        symbols.union(atoms(formula))
    
    def TT_CHECK_ALL(KB, a, symbols : set, model : dict):
        if len(symbols) == 0:
            if truth_value(KB, model):
                return truth_value(a, model)
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
    pass
    # ======== YOUR CODE HERE ========


def is_valid(formula):
    """Returns True if formula is a logically valid (tautology). Otherwise, it returns False"""
    pass
    # ======== YOUR CODE HERE ========


def satisfiability_brute_force(formula):
    """Checks whether formula is satisfiable.
    In other words, if the input formula is satisfiable, it returns an interpretation that assigns true to the formula.
    Otherwise, it returns False."""
    pass
    # ======== YOUR CODE HERE ========


