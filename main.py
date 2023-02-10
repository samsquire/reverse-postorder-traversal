class Ast:
  pass

class Add(Ast):
  def __init__(self, left, right):
    self.left = left
    self.right = right

  def postorder(self, items):
    self.left.postorder(items)
    self.right.postorder(items)
    items.append(("add", self))
    
  @classmethod
  def accept(self, stack):
    if len(stack) >= 2 and type(stack[0][1]) in [LiteralValue, Add, Mul] and \
    type(stack[1][1]) in [LiteralValue, Add, Mul] and stack[0][0] == "add":
      return True
    else:
      return False
      
  @classmethod
  def create(self, stack):
    print("creating add")
    return ("add", Add(stack.pop(0)[1], stack.pop(0)[1]))
                 
  def __repr__(self):
    return "Add {} {}".format(self.left, self.right)

class Mul(Ast):
  def __init__(self, left, right):
    self.left = left
    self.right = right

  def __repr__(self):
    return "Mul {} {}".format(self.left, self.right)
    
  def postorder(self, items):
    self.left.postorder(items)
    self.right.postorder(items)
    items.append(("mul", self))

  @classmethod
  def create(self, stack):
    return ("mul", Mul(stack.pop(0), stack.pop(0)))

  @classmethod
  def accept(self, stack):
    if len(stack) >= 2 and type(stack[0][1]) in [LiteralValue, Add, Mul] and \
    type(stack[1][1]) in [LiteralValue, Add, Mul] and stack[0][0] == "mul":
      return True
    else:
      return False

class LiteralValue(Ast):
  def __init__(self, value):
    self.value = value

  def postorder(self, items):
    items.append(("value", self))

  def __repr__(self):
    return "Literal {}".format(self.value)

  @classmethod
  def create(self, stack):
    return ("value", LiteralValue(stack.pop(0)[1].value))

  @classmethod
  def accept(self, stack):
    
    if type(stack[0][1]) == LiteralValue:
      print("Found literal value")
      return True
    else:
      print("Not a literal value {}".format(stack[0]))
      return False
    

order = \
  Add(Mul(LiteralValue(6), LiteralValue(7)),
      Mul(LiteralValue(5), LiteralValue(8)))

def recreatetree(items):
  stack = []
  
  for item in items:
    print("Processing {}".format(item))
    stack.append(item)
    for clazz in [LiteralValue, Mul, Add]:
      
      if clazz.accept(stack):
        tree = clazz.create(stack)
        print("created {}".format(tree))
        stack.insert(0, tree)
      

  print("Stack at end")
  print(stack)
  for clazz in [LiteralValue, Mul, Add]:
    if clazz.accept(stack):
      tree = clazz.create(stack)
      print("created {}".format(tree))
      stack.insert(0, tree)

  return stack

items = []
order.postorder(items)
print(items)
tree = recreatetree(items)
print(tree)


