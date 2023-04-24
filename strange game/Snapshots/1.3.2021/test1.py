""" for i in range(len(funcs)): 
  if i == 0:
    funcs[i](4)
  else:
    funcs[i]("text") """

"""CHANGING GLOBAL VARIABLES WITH FUNCS"""
""" a = True
b = False

def test():
  global a
  global b
  if a:
    a = False
  if not b:
    b = True

print("Before - a:",a,"b:",b)
test()
print("After -  a:",a,"b:",b) """

"""CHANGING GLOBAL VARIABLES WITH FUNCS"""
i = 50
mystr="I'll"
if "I'll" in mystr:
  i = 3
else:
  i = 4

print("FIRST:",i)
def test():
  global i
  if i == 3:
    i = 1
  else:
    i = 0

test()
print("SECOND:",i)


