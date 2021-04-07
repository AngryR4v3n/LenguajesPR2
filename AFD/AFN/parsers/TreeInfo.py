
def compute_first(tree):
    if(tree.root == "|"):
        arr1 = tree.left.first_pos 
        arr2 = tree.right.first_pos
        unified = union(arr1, arr2)
        tree.first_pos = unified
        return unified

    elif(tree.root == "." and (is_nullable(tree.left))):
        arr1 = tree.left.first_pos 
        arr2 = tree.right.first_pos
        unified = union(arr1, arr2)
        tree.first_pos = unified
        return unified
    elif(tree.root == "." and not (is_nullable(tree.left))):
        arr1 = tree.left.first_pos 
        tree.first_pos = arr1
        return arr1

    elif(tree.root == "*"):
        arr1 = tree.left.first_pos
        tree.first_pos = arr1
        return arr1
    
    
    else:
        #si es un simbolo..
        tree.first_pos = [tree.number]
        first_pos = [tree.number]
        return [tree.number]

def compute_last(tree):
    if(tree.root == "|"):
        arr1 = tree.left.last_pos 
        arr2 = tree.right.last_pos
        unified = union(arr1, arr2)
        tree.last_pos = unified
        return unified

    elif(tree.root == "." and (is_nullable(tree.right))):
        arr1 = tree.left.last_pos 
        arr2 = tree.right.last_pos
        unified = union(arr1, arr2)
        tree.last_pos = unified
        return unified
    elif(tree.root == "." and not (is_nullable(tree.right))):
        arr1 = tree.right.last_pos 
        tree.last_pos = arr1
        return arr1

    elif(tree.root == "*"):
        arr1 = tree.left.last_pos 
        tree.last_pos = arr1
        return arr1
    
    
    else:
        #si es un simbolo..
        tree.last_pos = [tree.number]
        last_pos = [tree.number]
        return [tree.number]



def union( arr1, arr2):
    res = arr1.copy()
    for elem in arr2:
        if elem not in res:
            res.append(elem)
    return res

def is_nullable( node):
    if node:
        if node.root == "*":
            node.nullable = True
            return True
        elif node.root == "&":
            node.nullable = True
            return True
        elif node.root == "|":
            left = node.left.nullable
            right = node.right.nullable
            node.nullable = left or right
            return left or right

        elif node.root == ".":
            left = node.left.nullable
            right = node.right.nullable
            node.nullable = left and right
            return left and right

        #es un simbolo.
        else:
            node.nullable = False
            return False


