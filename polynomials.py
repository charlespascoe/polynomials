
def to_superscript(number):
    supers = '⁰¹²³⁴⁵⁶⁷⁸⁹'
    return ''.join((supers[int(d)] for d in str(number)))


def format_coefficient(coeff, allow_one = False):
    if coeff == 1 and not allow_one:
        return ''

    if coeff % 1 == 0:
        return str(int(coeff))

    return str(coeff)


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

    @staticmethod
    def single_expr(coeff, order):
        return Polynomial(*(0 for _ in range(order)), coeff)

    def __len__(self):
        return self.order

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
        output = ''

        first = True

        for i in range(len(self.coefficients) - 1, -1, -1):
            if self.coefficients[i] != 0:
                if self.coefficients[i] < 0:
                    output += '-' if first else ' - '
                elif not first:
                    output += ' + '

                first = False

                if i == 0:
                    output += format_coefficient(abs(self.coefficients[i]), True)
                else:
                    output += '{}x{}'.format(format_coefficient(abs(self.coefficients[i])), to_superscript(i) if i != 1 else '')

        if len(output) == 0:
            return '0'

        return output

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

    def __sub__(self, other):
        if isinstance(other, int):
            return Polynomial(self[0] - other, *self.coefficients[1:])
        elif isinstance(other, Polynomial):
            coeffs = []

            for i in range(max(self.order, other.order) + 1):
                coeffs.append(self[i] - other[i])

            return Polynomial(*coeffs)
        else:
            raise TypeError('Only a Polynomial or an int can be subtracted from a Polynomial (not {})'.format(other.__class__.__name__))

    def __isub__(self, other):
        return self - other

    def __rsub__(self, other):
        if isinstance(other, int):
            return Polynomial(other) - self
        else:
            raise TypeError('Only a Polynomial or an int can be subtracted from a Polynomial (not {})'.format(other.__class__.__name__))

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

    def __divmod__(self, other):
        if isinstance(other, Polynomial):
            dividendOrd = self.order
            divisorOrd = other.order

            if dividendOrd < divisorOrd:
                return (Polynomial(), self)

            quotient = Polynomial.single_expr(self[dividendOrd] / other[divisorOrd], dividendOrd - divisorOrd)

            quot, rem = divmod(self - (other * quotient), other)

            return (quot + quotient, rem)
        elif isinstance(other, int):
            return self / Polynomial(other)
        else:
            raise TypeError('Only a Polynomial or an int can divide a Polynomial (not {})'.format(other.__class__.__name__))

    def __floordiv__(self, other):
        quot, rem = divmod(self, other)

        return quot

    def __mod__(self, other):
        quot, rem = divmod(self, other)

        return rem


print(Polynomial(1, 2, -3))
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

print('({}) - ({}) = {}'.format(pol3, Polynomial(1, 2), pol3 - Polynomial(1, 2)))

pol4 = Polynomial(1, 2, 3)
pol5 = Polynomial(4, 5, 6, 7)

print('({}) * ({}) = {}'.format(pol4, pol5, pol4 * pol5))

print('{} * ({}) = {}'.format(3, pol4, 3 * pol4))

print(Polynomial.single_expr(123, 5))

pol6 = Polynomial(2, 1)
pol7 = Polynomial(-10, -3, 1)

print('({}) / ({}) = {} remainder {}'.format(pol7, pol6, pol7 // pol6, pol7 % pol6))
