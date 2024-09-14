from fol_formula import Atom, Not, Implies, And, Or, ForAll, Exists
from term import Con, Var, Fun


def length_fol(formula):
    """Determines the length of a formula in first-order logic."""
    if isinstance(formula, Atom):
        return 1
    if isinstance(formula, Not):
        return length_fol(formula.inner) + 1
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return length_fol(formula.left) + length_fol(formula.right) + 1
    if isinstance(formula, ForAll) or isinstance(formula, Exists):
        return 1 + length_fol(formula.inner)


def subformulas_fol(formula):
    """Returns the set of all subformulas of a first-order formula"""
    if isinstance(formula, Atom):
        subformulas = set()
        subformulas.add(formula)
        for arg in formula.args:
            subformulas = subformulas.union(subformulas_fol(arg))
        return subformulas
    elif isinstance(formula, Not):
        subformulas = set()
        subformulas.add(formula)
        subformulas = subformulas.union(subformulas_fol(formula.inner))
        return subformulas
    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        subformulas = set()
        subformulas.add(formula)
        subformulas = subformulas.union(subformulas_fol(formula.left))
        subformulas = subformulas.union(subformulas_fol(formula.right))
        return subformulas
    elif isinstance(formula, ForAll) or isinstance(formula, Exists):
        subformulas = set()
        subformulas.add(formula)
        subformulas = subformulas.union(subformulas_fol(formula.inner))
        return subformulas
    return set()


def constants_from_term(term):
    """Returns the set of all constant occurring in a term"""
    if isinstance(term, Con):
        return {term}
    if isinstance(term, Var):
        return set()
    if isinstance(term, Fun):
        constants = set()
        for arg in term.args:
            constants = constants.union(constants_from_term(arg))
        return constants


def variables_from_term(term):
    """Returns the set of all variables occurring in a term"""
    if isinstance(term, Con):
        return set()
    if isinstance(term, Var):
        return {term}
    if isinstance(term, Fun):
        variables = set()
        for inner_term in term.args:
            variables = variables.union(variables_from_term(inner_term))
        return variables


def function_symbols_from_term(term):
    """Returns the set of all function symbols occurring in a term
    For example, function_symbols_from_term(Fun('f', [Var('x'), Con('a')]))
    must return {'f'}

    and

    function_symbols_from_term(Fun('g', [Fun('f', [Var('x'), Con('a')])]))
    must return {'f', 'g'}
    """
    if isinstance(term, Con):
        return set()
    elif isinstance(term, Var):
        return set()
    elif isinstance(term, Fun):
        functions = set()
        functions.add(term.name)
        for arg in term.args:
            functions = functions.union(function_symbols_from_term(arg))
        return functions


def all_constants(formula):
    """Returns the set of all constant occurring in a formula"""
    if isinstance(formula, Con):
        return {formula}
    elif isinstance(formula, Fun):
        constants = set()
        for arg in formula.args:
            constants = constants.union(all_constants(arg))
        return constants
    elif isinstance(formula, Atom):
        constants = set()
        for arg in formula.args:
            constants = constants.union(all_constants(arg))
        return constants
    elif isinstance(formula, Not):
        return all_constants(formula.inner)
    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        constants = set()
        constants = constants.union(all_constants(formula.left))
        constants = constants.union(all_constants(formula.right))
        return constants
    elif isinstance(formula, ForAll) or isinstance(formula, Exists):
        return all_constants(formula.inner)
    return set()


def predicate_symbols(formula):
    """Returns the set of all predicate symbols occurring in a formula.
    For example, predicate_symbols(Or(Atom('P', [Con('a')]), Atom('R', [Var('x')])))
    must return {'P', 'R'}
    """
    if isinstance(formula, Atom):
        predicates = set()
        predicates.add(formula.name)
        return predicates
    elif isinstance(formula, Not):
        return predicate_symbols(formula.inner)
    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        predicates = set()
        predicates = predicates.union(predicate_symbols(formula.left))
        predicates = predicates.union(predicate_symbols(formula.right))
        return predicates
    elif isinstance(formula, ForAll) or isinstance(formula, Exists):
        return predicate_symbols(formula.inner)
    return set()


def function_symbols(formula):
    """Returns the set of all function symbols occurring in a formula.
    For example, predicate_symbols(Or(Atom('P', [Fun('f', [Con('b'), Var('y')])]),
                                      Atom('P', [Fun('g', [Var('y')])])
                                      )
                                   )
    must return {'f', 'g'}
    """
    if isinstance(formula, Fun):
        functions = set()
        functions.add(formula.name)
        for arg in formula.args:
            functions = functions.union(function_symbols(arg))
        return functions
    elif isinstance(formula, Atom):
        functions = set()
        for arg in formula.args:
            functions = functions.union(function_symbols(arg))
        return functions
    elif isinstance(formula, Not):
        return function_symbols(formula.inner)
    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        functions = set()
        functions = functions.union(function_symbols(formula.left))
        functions = functions.union(function_symbols(formula.right))
        return functions
    elif isinstance(formula, ForAll) or isinstance(formula, Exists):
        return function_symbols(formula.inner)
    return set()


def atoms_fol(formula):
    """Returns the set of all atomic suformulas of a first-order formula"""
    if isinstance(formula, Fun):
        atoms = set()
        for arg in formula.args:
            atoms = atoms.union(atoms_fol(arg))
        return atoms
    elif isinstance(formula, Atom):
        return {formula}
    elif isinstance(formula, Not):
        return atoms_fol(formula.inner)
    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        atoms = set()
        atoms = atoms.union(atoms_fol(formula.left))
        atoms = atoms.union(atoms_fol(formula.right))
        return atoms
    elif isinstance(formula, ForAll) or isinstance(formula, Exists):
        atoms = set()
        atoms = atoms.union(atoms_fol(formula.inner))
        return atoms
    return set()


def free_variables(formula):
    """Returns the set of all free variables of a formula"""
    if isinstance(formula, Var):
        return {formula}
    elif isinstance(formula, Fun):
        free_vars = set()
        for arg in formula.args:
            free_vars = free_vars.union(free_variables(arg))
        return free_vars
    elif isinstance(formula, Atom):
        free_vars = set()
        for arg in formula.args:
            free_vars = free_vars.union(free_variables(arg))
        return free_vars
    elif isinstance(formula, Not):
        return free_variables(formula.inner)
    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        free_vars = set()
        free_vars = free_vars.union(free_variables(formula.left))
        free_vars = free_vars.union(free_variables(formula.right))
        return free_vars
    elif isinstance(formula, ForAll) or isinstance(formula, Exists):
        free_vars = set()
        free_vars = free_vars.union(free_variables(formula.inner))
        if formula.var in free_vars:
            free_vars.remove(formula.var)
        return free_vars
    return set()


def bounded_variables(formula):
    """Returns the set of all bounded variables of a formula"""
    if isinstance(formula, Fun):
        bounded_vars = set()
        for arg in formula.args:
            bounded_vars = bounded_vars.union(bounded_variables(arg))
        return bounded_vars
    elif isinstance(formula, Atom):
        bounded_vars = set()
        for arg in formula.args:
            bounded_vars = bounded_vars.union(bounded_variables(arg))
        return bounded_vars
    elif isinstance(formula, Not):
        return bounded_variables(formula.inner)
    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        bounded_vars = set()
        bounded_vars = bounded_vars.union(bounded_variables(formula.left))
        bounded_vars = bounded_vars.union(bounded_variables(formula.right))
        return bounded_vars
    elif isinstance(formula, ForAll) or isinstance(formula, Exists):
        bounded_vars = set()
        bounded_vars.add(formula.var)
        bounded_vars.union(bounded_variables(formula.inner))
        return bounded_vars
    return set()


def universal_closure(formula):
    """Returns the universal closure of a formula"""
    result = formula
    free_vars = free_variables(formula)
    for var in free_vars:
        result = ForAll(var, result)
    return result


def existential_closure(formula):
    """Returns the existential closure of a formula"""
    result = formula
    free_vars = free_variables(formula)
    for var in free_vars:
        result = Exists(var, result)
    return result


def number_free_occurrences(var, formula):
    """Returns the number of free occurrences of variable var in formula.
    For example, number_free_occurrences(Var('x'),
                                         ForAll(Var('y'), Implies(And(Atom('P', [Var('x')]),
                                                                      Atom('Q', [Var('y')])),
                                                                  ForAll(Var('x'), Atom('Q', [Var('x')]))
                                                                 )
                                               )
                                        )
    must return 1
    """
    if isinstance(formula, Var):
        if formula == var:
            return 1
    elif isinstance(formula, Fun):
        num_vars = 0
        for arg in formula.args:
            num_vars += number_free_occurrences(var, arg)
        return num_vars
    elif isinstance(formula, Atom):
        num_vars = 0
        for arg in formula.args:
            num_vars += number_free_occurrences(var, arg)
        return num_vars
    elif isinstance(formula, Not):
        return number_free_occurrences(var, formula.inner)
    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return number_free_occurrences(var, formula.left) + number_free_occurrences(var, formula.right)
    elif isinstance(formula, ForAll) or isinstance(formula, Exists):
        if formula.var != var:
            return number_free_occurrences(var, formula.inner)
    return 0


# scope?
# quantifier-free
# closed term / ground terms
# closed formula / sentence
