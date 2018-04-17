L = [2 ** x for x in range(7)]
X = 5
V = 2 ** X
if V in L:
    print('at index', L.index(V))
else:
    print(X, 'not found')
