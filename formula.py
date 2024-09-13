"""This module is designed to define formulas in propositional logic.
For example, the following piece of code creates an object representing (p v s).

formula1 = Or(Atom('p'), Atom('s'))


As another example, the piece of code below creates an object that represents (p → (p v s)).

formula2 = Implies(Atom('p'), Or(Atom('p'), Atom('s')))
"""

class Formula:
    def __init__(self):
        pass

    def __repr__(self):
        return str(self)


class Atom(Formula):
    """
    This class represents propositional logic variables.
    """

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __str__(self):
        return str(self.name)

    def __eq__(self, other: Formula):
        return isinstance(other, Atom) and other.name == self.name

    def __hash__(self):
        return hash((self.name, 'atom'))


class Implies(Formula):
    def __init__(self, left: Formula, right: Formula):
        super().__init__()
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} \u2192 {self.right})"

    def __eq__(self, other: Formula):
        return isinstance(other, Implies) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((hash(self.left), hash(self.right), 'implies'))


class Not(Formula):
    def __init__(self, inner: Formula):
        super().__init__()
        self.inner = inner

    def __str__(self):
        return f"(\u00ac{self.inner})"

    def __eq__(self, other: Formula):
        return isinstance(other, Not) and other.inner == self.inner

    def __hash__(self):
        return hash((hash(self.inner), 'not'))


class And(Formula):
    def __init__(self, left: Formula, right: Formula):
        super().__init__()
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} \u2227 {self.right})"

    def __eq__(self, other: Formula):
        return isinstance(other, And) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((hash(self.left), hash(self.right), 'and'))


class Or(Formula):
    def __init__(self, left: Formula, right: Formula):
        super().__init__()
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} \u2228 {self.right})"

    def __eq__(self, other: Formula):
        return isinstance(other, Or) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((hash(self.left), hash(self.right), 'or'))


class Iff(Formula):
    def __init__(self, left: Formula, right: Formula):
        super().__init__()
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} \u2194 {self.right})"

    def __eq__(self, other: Formula):
        return isinstance(other, Iff) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((hash(self.left), hash(self.right), 'iff'))


class Xor(Formula):      
    def __init__(self, left: Formula, right: Formula):
        super().__init__()
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} \u2295 {self.right})"

    def __eq__(self, other: Formula):
        return isinstance(other, Xor) and other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash((hash(self.left), hash(self.right), 'xor'))