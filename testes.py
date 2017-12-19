import numpy as np

teste = [
    ['a', 'b', 0],
    ['d', 'e', 0],
    ['g', 'h', 0]
]


if len(np.unique(np.array(np.array(teste)[:,2], 'int'))) == 3:
    min_ = 0
else:
    min_ = np.array(np.array(teste)[:,2], 'int').min()


# print min


dict_ = dict({
             0 : ['askd', 'asdhu'],
             1 : 'asd',
             1 : 'ASH',
})

dict__ = dict([])
dict__[0] = dict_[0]

g = lambda x : x**2

x=[]
for i in range(10):
    x += [i]

print x
