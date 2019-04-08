import re
from operator import add
from operator import sub


class Polynomial(object):
    def __init__(self, coeffs):
        if isinstance(coeffs, list) or isinstance(coeffs, tuple):
            self.coeffs = coeffs
        else:
            if isinstance(coeffs, Polynomial):
                self.coeffs = coeffs.coeffs
            else:
                raise ValueError("Incorrect format of values for polynomial coefficients")

    @property
    def coeffs(self):
        return self._coeffs

    @coeffs.setter
    def coeffs(self, cff):
        copy = list(cff)
        while copy and copy[0] == 0:
            del copy[0]
        for c in copy:
            if not isinstance(c, int):
                raise ValueError("Incorrect format of values for polynomial coefficients")
        if not copy:
            self._coeffs = (0,)
        else:
            self._coeffs = list(copy)

    def __repr__(self):
        return 'Polynomial({})'.format(self.coeffs)

    def __str__(self):
        res = ''
        if self.coeffs == (0,) or self.coeffs == [0, ]:
            return '0'
        for i in range(len(self.coeffs) - 1):
            if (self.coeffs[i] > 0):
                res += '+ ' + str(self.coeffs[i]) + 'x^' + str(len(self.coeffs) - i - 1) + ' '
            if (self.coeffs[i] < 0):
                res += '- ' + str(abs(self.coeffs[i])) + 'x^' + str(len(self.coeffs) - i - 1) + ' '
        if (self.coeffs[-1] != 0):
            if (self.coeffs[-1] > 0):
                res += '+ '
            else:
                res += '- '
            res += str(abs(self.coeffs[-1]))
        if res == '':
            return '0'
        if res[0] == '+':
            res = res[1:]
        res = re.sub('x\\^1\\b', 'x', res)
        return res.replace(' 1x', ' x')

    def __add__(self, other):
        if isinstance(other, int):
            c = list(self.coeffs)
            c[-1] += other
            return Polynomial(c)

        if isinstance(other, Polynomial):
            if len(self.coeffs) > len(other.coeffs):
                cff1 = len(other.coeffs)
                cff2 = list(reversed(self.coeffs))[cff1:]
            else:
                cff1 = len(self.coeffs)
                cff2 = list(reversed(other.coeffs))[cff1:]
            return Polynomial(
                (list(map(add, list(reversed(self.coeffs))[:cff1], list(reversed(other.coeffs))[:cff1])) + cff2)[
                ::-1])

        raise ValueError("Incorrect argument")

    def __radd__(self, other):
        if isinstance(other, int):
            c = list(self.coeffs)
            c[-1] += other
            return Polynomial(c)

        raise ValueError("Incorrect argument")

    def __sub__(self, other):
        if isinstance(other, int):
            c = list(self.coeffs)
            c[-1] -= other
            return Polynomial(c)

        if isinstance(other, Polynomial):
            if len(self.coeffs) > len(other.coeffs):
                cff1 = len(other.coeffs)
                cff2 = list(reversed(self.coeffs))[cff1:]
            else:
                cff1 = len(self.coeffs)
                cff2 = list(reversed(other.coeffs))[cff1:]
                cff2 = [i * (-1) for i in cff2]
            return Polynomial(
                (list(map(sub, list(reversed(self.coeffs))[:cff1], list(reversed(other.coeffs))[:cff1])) + cff2)[
                ::-1])

        raise ValueError("Incorrect argument")

    def __rsub__(self, other):
        if isinstance(other, int):
            c = [(-1) * c for c in self.coeffs]
            c[-1] += other
            return Polynomial(c)

        raise ValueError("Incorrect argument")

    def __mul__(self, other):
        if isinstance(other, int):
            return Polynomial([c * other for c in self.coeffs])

        if isinstance(other, Polynomial):
            c = [0] * (len(self.coeffs) + len(other.coeffs) - 1)
            for i1, c1 in enumerate(self.coeffs):
                for i2, c2 in enumerate(other.coeffs):
                    c[i1 + i2] += c1 * c2
            return Polynomial(c)

        raise ValueError("Incorrect argument")

    def __rmul__(self, other):
        if isinstance(other, int):
            return Polynomial([c * other for c in self.coeffs])

        raise ValueError("Incorrect argument")

    def __eq__(self, other):
        return self.coeffs == other.coeffs

    def __lt__(self, other):
        if len(self.coeffs) == len(other.coeffs):
            return self.coeffs < other.coeffs
        else:
            return len(self.coeffs) < len(other.coeffs)

    def __le__(self, other):
        return self.__lt__(other) or self.coeffs == other.coeffs

    def __ne__(self, other):
        return self.coeffs != other.coeffs

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def calc(self, value):
        result = 0
        for i in range(len(self.coeffs) - 1):
            result += self.coeffs[i] * pow(value, len(self.coeffs) - i - 1)
        return result + self.coeffs[-1]


if __name__ == "__main__":
    p1 = Polynomial([-10, 2, 3, -1, -5, 1, 0, 0, 0, 0, 0, 0, 0, 1])
    p2 = Polynomial([1, 2])
    p4 = Polynomial([1, 2])

    print(p1)
    print(p2)
    print(p4)
    print(p2.__repr__())
    print(-1 * p1)
    print(p2 <= p4)
    print(p2.calc(2))
