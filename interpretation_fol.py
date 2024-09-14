"""This module is designed to define interpretations for first-order logic.
For example, the following piece of code creates an object representing an interpretation for the formula
(∀x((P(a, x, f(b, y)) ∧ R(f(g(b), y))) ⟶ P(a, x, f(b, y)))).

interpretation1 = Interpretation(domain = {1, 2, 3},
                  predicates = {'P':{(1,1,1), (2,3,1), (3,1,2), (3,3,2)},
                                'R':{(1, 2), (2,1), (2,2), (2,3), (3,3)}},
                  functions = {'f':{(1,1):1, (1,2):2, (1,3):1, (2,1):1, (2,2):3, (2,3):2, (3,1):1, (3,2):2, (3,3):3},
                               'g':{(1,): 2, (2,): 3, (3,): 2}},
                  constants = {'a': 1, 'b': 3},
                  variables = {'x' : 2, 'y': 1}
                  )

Note that we use a dictionary to represent the interpretation of a function.
"""

from fol_formula import And, Atom, Exists, ForAll, Implies, Not, Or
from term import Var, Con, Fun


class Interpretation:
    def __init__(self, domain, predicates, functions, constants, variables):
        self.domain = domain
        self.predicates = predicates
        self.functions = functions
        self.constants = constants
        self.variables = variables

    def interpretation_term(self, term):
        """Returns the the interpretation of term in a interpretation.
        For example, let interpretation1 be the interpretation defined in the first lines of this file.

        interpretation1.interpretation_term(Fun('g', [Fun('f', [Var('x'), Con('a')])]))

        must return 2
        """
        if isinstance(term, Var):
            return self.variables[term.name]
        elif isinstance(term, Con):
            return self.constants[term.name]
        elif isinstance(term, Fun):
            fun = self.functions[term.name]
            args = tuple(self.interpretation_term(arg) for arg in term.args)
            return fun[args]

    def truth_value(self, formula):
        """Returns the the truth-value of an input first-order formula in a interpretation."""
        if isinstance(formula, Atom):
            predicate = self.predicates[formula.name]
            args = tuple(self.interpretation_term(arg) for arg in formula.args)
            return args in predicate
        elif isinstance(formula, Not):
            return not self.truth_value(formula.inner)
        elif isinstance(formula, Implies):
            return not self.truth_value(formula.left) or self.truth_value(formula.right)
        elif isinstance(formula, And):
            return self.truth_value(formula.left) and self.truth_value(formula.right)
        elif isinstance(formula, Or):
            return self.truth_value(formula.left) and self.truth_value(formula.right)
        elif isinstance(formula, ForAll):
            var = self.variables.get(formula.var, None)
            for term in self.domain:
                self.variables[formula.var] = term
                if not self.truth_value(formula.inner):
                    if var is not None:
                        self.variables[formula.var] = var
                    else:
                        del self.variables[formula.var]
                    return False
            if var is not None:
                self.variables[formula.var] = var
            else:
                del self.variables[formula.var]
            return True
        elif isinstance(formula, Exists):
            var = self.variables.get(formula.var, None)
            for term in self.domain:
                self.variables[formula.var] = term
                if self.truth_value(formula.inner):
                    if var is not None:
                        self.variables[formula.var] = var
                    else:
                        del self.variables[formula.var]
                    return True
            if var is not None:
                self.variables[formula.var] = var
            else:
                del self.variables[formula.var]
            return False
