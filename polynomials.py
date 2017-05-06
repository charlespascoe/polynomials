
def to_superscript(number):
    supers = '⁰¹²³⁴⁵⁶⁷⁸⁹'
    return ''.join((supers[int(d)] for d in str(number)))


class Polynomial:
    def __init__(self, *coefficients):
        self.coefficients = list(coefficients)

    @property
    def order(self):
        highest_expression = 0

        for i in range(len(self.coefficients)):
            if self.coefficients[i] != 0:
                highest_expression = i

        return highest_expression

    def __getitem__(self, items):
        if isinstance(items, int):
            if items < len(self.coefficients):
                return self.coefficients[items]
            else:
                return 0
        elif isinstance(items, slice):
            return (self[i] for i in range(items.start, items.stop, items.step if items.step is not None else 1))
        else:
            raise TypeError('__getitem__ items must be an int or a slice')

    def __call__(self, x):
        result = 0
        expr = 1

        for coeff in self.coefficients:
            result += coeff * expr

            expr *= x

        return result

    def __str__(self):
        output = []

        for i in range(len(self.coefficients)):
            if self.coefficients[i] != 0:
                if i == 0:
                    output.append(str(self.coefficients[i]))
                else:
                    output.append('{}x{}'.format(self.coefficients[i] if self.coefficients[i] != 1 else '', to_superscript(i) if i != 1 else ''))

        output.reverse()

        if len(output) == 0:
            return '0'

        return ' + '.join(output)

    def __add__(self, other):
        if isinstance(other, int):
            return Polynomial(self[0] + other, *self.coefficients[1:])
        elif isinstance(other, Polynomial):
            coeffs = []

            for i in range(max(self.order, other.order) + 1):
                coeffs.append(self[i] + other[i])

            return Polynomial(*coeffs)
        else:
            raise TypeError('Only a Polynomial or an int can be added to a Polynomial (not {})'.format(other.__class__.__name__))

    def __iadd__(self, other):
        return self + other

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        if isinstance(other, int):
            return Polynomial(*(other * coeff for coeff in self.coefficients))
        elif isinstance(other, Polynomial):
            coeffs = [0 for _ in range(self.order + other.order + 1)]

            for i in range(self.order + 1):
                for j in range(other.order + 1):
                    coeffs[i + j] += self[i] * other[j]

            return Polynomial(*coeffs)
        else:
            raise TypeError('Only a Polynomial or an int can multiply a Polynomial (not {})'.format(other.__class__.__name__))

    def __imul__(self, other):
        return self * other

    def __rmul__(self, other):
        return self * other


print(Polynomial(1, 2, 3))
print(Polynomial())

pol1 = Polynomial(0, 1, 1, 0)
print('f(x) = {}, order = {}, f({}) = {}'.format(pol1, pol1.order, 5, pol1(5)))

print(list(pol1[0:10]))

pol2 = Polynomial(0, 0, 3)

pol3 = Polynomial(1, 2, 3, 4, 5)
print('({}) + ({}) = {}'.format(pol1, pol2, pol1 + pol2))
print('({}) + ({}) = {}'.format(pol1, 7, pol1 + 7))
print('({}) + ({}) = {}'.format(9, pol3, 9 + pol3))

pol3 += 1

print(pol3)

pol4 = Polynomial(1, 2, 3)
pol5 = Polynomial(4, 5, 6, 7)

print('({}) * ({}) = {}'.format(pol4, pol5, pol4 * pol5))

print('{} * ({}) = {}'.format(3, pol4, 3 * pol4))
