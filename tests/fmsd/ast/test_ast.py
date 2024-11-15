from fmsd.ast.node import Node, VarNode


def test_eq():
    a = VarNode("a")
    b = VarNode("b")
    assert a != b
    assert a == a

    tree1 = Node(a, Node(a, b))
    tree2 = Node(VarNode("a"), Node(a, VarNode("b")))
    tree3 = Node(VarNode("b"), Node(a, b))
    tree4 = Node()
    assert tree1 == tree1
    assert tree1 == tree2
    assert tree1 != tree3
    assert tree1 != tree4
    assert tree4 == tree4


def test_variables():
    tree = Node(VarNode("a"), VarNode("b"), Node(VarNode("a")))
    assert tree.varnodes() == {VarNode("a"), VarNode("b")}


def test_eval():
    a = VarNode("a")
    b = VarNode("b")
    tree = Node(a, b, Node(a))
    assert tree.eval({a: b, b: a}) == Node(b, a, Node(b))


def test_match():
    a = VarNode("a")
    b = VarNode("b")
    tree1 = Node(a, b, Node(a))
    tree2 = Node(b, a, Node(b))
    assert tree1.match(tree2, {}) == {a: b, b: a}
    tree3 = Node(a, a, Node(a))
    assert tree1.match(tree3, {}) == {a: a, b: a}
    tree4 = Node(a, Node(a))
    assert tree1.match(tree4, {}) is None
    tree5 = Node(a, b, Node(b))
    assert tree1.match(tree5, {}) is None


def test_get():
    a = VarNode("a")
    b = VarNode("b")
    tree = Node(a, b, Node(b))
    assert tree.get([]) == tree
    assert tree.get([0]) == a
    assert tree.get([2, 0]) == b


def test_set():
    a = VarNode("a")
    b = VarNode("b")
    tree = Node(a, b, Node(b))
    assert tree.replace([1], Node(a)) == Node(a, Node(a), Node(b))
    assert tree.replace([2, 0], a) == Node(a, b, Node(a))


def test_diff():
    a = VarNode("a")
    b = VarNode("b")

    tree1 = Node(Node(a, Node(a, b)))
    tree2 = Node(Node(a, Node(b, a)))
    tree3 = Node(Node(b, Node(a, b)))

    assert tree1.diff(tree2) == [0, 1]
    assert tree1.diff(tree1) is None
    assert tree1.diff(tree3) == [0, 0]
    assert a.diff(b) == []


def test_weak_diff():
    a = VarNode("a")
    b = VarNode("b")

    tree1 = Node(Node(a, Node(a, b)))
    tree2 = Node(Node(a, Node(b, a)))

    assert tree1.weak_diff(tree2) == [0, 1, 0]
    assert a.weak_diff(b) == []


def test_flatten():
    a = VarNode("a")
    b = VarNode("b")

    class Node1(Node):
        pass

    tree = Node(a, Node(b, Node1(a, b), a))
    assert tree.flatten() == [a, b, Node1(a, b), a]
