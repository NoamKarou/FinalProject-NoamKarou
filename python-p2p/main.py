class test:
    def __init__(self, a):
        self.a = a


test_objects = list()
for i in range(10):
    test_objects.append(test(i))

print([a.a for a in test_objects])