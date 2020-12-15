from Interpreter.Expressions.expression import Expression


class Arithmetic(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def getValue(self, env):
        pass

    def isNumeric(self, value):
        return isinstance(value, int) or isinstance(value, float)


class Addition(Arithmetic):
    def __init__(self, left, right):
        Arithmetic.__init__(self, left, right)

    def getValue(self, env):
        leftValue = self.left.getValue(env)
        rightValue = self.right.getValue(env)
        areNums = self.isNumeric(leftValue) and self.isNumeric(rightValue)

        if areNums:
            return leftValue + rightValue


class Subtraction(Arithmetic):
    def __init__(self, left, right):
        Arithmetic.__init__(self, left, right)

    def getValue(self, env):
        leftValue = self.left.getValue(env)
        rightValue = self.right.getValue(env)
        areNums = self.isNumeric(leftValue) and self.isNumeric(rightValue)

        if areNums:
            return leftValue - rightValue


class Multiplication(Arithmetic):
    def __init__(self, left, right):
        Arithmetic.__init__(self, left, right)

    def getValue(self, env):
        leftValue = self.left.getValue(env)
        rightValue = self.right.getValue(env)
        areNums = self.isNumeric(leftValue) and self.isNumeric(rightValue)

        if areNums:
            return leftValue * rightValue


class Division(Arithmetic):
    def __init__(self, left, right):
        Arithmetic.__init__(self, left, right)

    def getValue(self, env):
        leftValue = self.left.getValue(env)
        rightValue = self.right.getValue(env)
        areNums = self.isNumeric(leftValue) and self.isNumeric(rightValue)

        if areNums:
            return leftValue / rightValue


class Power(Arithmetic):
    def __init__(self, left, right):
        Arithmetic.__init__(self, left, right)

    def getValue(self, env):
        leftValue = self.left.getValue(env)
        rightValue = self.right.getValue(env)
        areNums = self.isNumeric(leftValue) and self.isNumeric(rightValue)

        if areNums:
            return leftValue ** rightValue


class Modulo(Arithmetic):
    def __init__(self, left, right):
        Arithmetic.__init__(self, left, right)

    def getValue(self, env):
        leftValue = self.left.getValue(env)
        rightValue = self.right.getValue(env)
        areNums = self.isNumeric(leftValue) and self.isNumeric(rightValue)

        if areNums:
            return leftValue % rightValue
