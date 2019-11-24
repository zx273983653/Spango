from multidict import CIMultiDict

a = CIMultiDict()

a['abc'] = '123'
a['DEF'] = '456'

print(a['ABC'])
print(a['def'])
