class A:
    def __init__(self):
        print("-" * 20, "a")
        self.value = 1


class B:
    def __init__(self):
        print("-" * 20, "b")
        self.value = 2

    def log(self):
        print("|> value", self.value)


class C(A, B):
    pass


c = C()

c.log()
