#Shane Houston (115477508)
class Element(object):
    def __init__(self, key, value, index):
        self.key = key
        self.value = value
        self.index = index

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key

    def __le__(self,other):
        return self.key <= other.key

    def wipe(self):
        temp_key = self.key
        temp_value = self.value
        self.key = None
        self.value = None
        self.index = None
        return temp_key, temp_value

    def __str__(self):
        desc = "%s: %s (%s)" % (self.value, self.key, self.index)
        return desc
        
class APQ(object):
    def __init__(self):
        self.size = 0
        self.body = []

    def left(self, elt):
        lindex = (elt.index*2)+1
        if lindex < self.size and lindex > 0:
            return self.body[lindex]

    def right(self, elt):
        rindex = (elt.index*2)+2
        if rindex < self.size and rindex > 0:
            return self.body[rindex]
        
    def parent(self, elt):
        pindex = (elt.index-1)//2
        if pindex >= 0:
            return self.body[pindex]

    def add(self, key, item):
        self.size += 1
        new = Element(key, item, self.size-1)
        self.body.append(new)
        self.bubbleUp(new)
        return new

    def swap(self, e1, e2):
        self.body[e1.index], self.body[e2.index] = self.body[e2.index], self.body[e1.index]
        e1.index, e2.index = e2.index, e1.index

    def bubbleDown(self, elt):
        finished = False 
        while not finished:
            if self.left(elt) is not None and self.right(elt) is not None:
                if self.left(elt) <= self.right(elt) and self.left(elt) < elt:
                    leftchild = self.left(elt)
                    self.swap(elt, leftchild)
                elif self.right(elt) < self.left(elt) and self.right(elt) < elt:
                    rightchild = self.right(elt)
                    self.swap(elt, rightchild)
                else:
                    finished = True
            elif self.left(elt) is not None and self.right(elt) is None and self.left(elt) < elt:
                leftchild = self.left(elt)
                self.swap(elt, leftchild)
                finished = True
            else:
                finished = True
        
    def bubbleUp(self, elt):
        while self.parent(elt) and self.parent(elt) > elt:
            parent = self.parent(elt)
            self.swap(elt, parent)

    def get_min(self):
        return self.body[0]

    def remove_min(self):
        mini = self.get_min()
        self.swap(mini, self.body[self.size-1])
        popped = self.body.pop()
        self.size -= 1
        if self.size > 0:
            top = self.get_min()
            self.bubbleDown(top)
        return popped

    def is_empty(self):
        return self.size == 0

    def length(self):
        return self.size

    def update_key(self, element, newkey):
        leftchild = self.left(element)
        rightchild = self.right(element)
        parent = self.parent(element)
        if element in self.body:
            element.key = newkey
            if parent and element < parent:
                self.bubbleUp(element)
            elif leftchild and element > leftchild:
                self.bubbleDown(element)
            elif rightchild and element > rightchild:
                self.bubbleDown(element)

    def get_key(self, element):
        if element in self.body:
            return element.key

    def remove(self, element):
        last = self.body[self.size-1]
        self.swap(element, last)
        if element < parent:
            self.bubbleUp(element)
        elif element > leftchild or element > rightchild:
            self.bubbleDown(element)
        return element.wipe()

    def __str__(self):
        desc = ""
        for i in self.body:
            if i != self.body[0]:
                desc += " - "
            desc += str(i)
        return desc
        
            
            
        
