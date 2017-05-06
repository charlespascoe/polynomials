
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


print(Polynomial(1, 2, 3))
print(Polynomial())

pol1 = Polynomial(0, 1, 1, 0)
print('f(x) = {}, order = {}, f({}) = {}'.format(pol1, pol1.order, 5, pol1(5)))

print(list(pol1[0:10]))
