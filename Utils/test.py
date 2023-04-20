def test(test, **kwargs):
    print(test, kwargs)

    print(list(kwargs.items())[:-1])
    print(tuple(kwargs.keys()))
    print(tuple(kwargs.values()))
    print(len(kwargs))



a = 1
b = 2
c = 4
h = 'dd'
j = 7
test('asda', a=a, b=b, c=c, h=h, j=j)
