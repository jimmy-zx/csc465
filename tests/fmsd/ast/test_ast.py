from fmsd.ast.node import Variable, Node


def test_eq():
    a = Variable("a")
    b = Variable("b")
    assert a != b
    assert a == a

    tree1 = Node(a, Node(a, b))
    tree2 = Node(Variable("a"), Node(a, Variable("b")))
    tree3 = Node(Variable("b"), Node(a, b))
    tree4 = Node()
    assert tree1 == tree1
    assert tree1 == tree2
    assert tree1 != tree3
    assert tree1 != tree4
    assert tree4 == tree4


def test_copy():
    a = Variable("a")
    a_copy = a.copy()
    assert a is not a_copy
    a = Variable("a")
    tree = Node(Node(a, a), Node(a))
    tree_copy = tree.copy()
    for lhs, rhs in zip(tree.walk_preorder(), tree_copy.walk_preorder()):
        assert lhs is not rhs


def test_variables():
    tree = Node(Variable("a"), Variable("b"), Node(Variable("a")))
    assert tree.variables() == {"a", "b"}


def test_eval():
    a = Variable("a")
    b = Variable("b")
    tree = Node(a, b, Node(a))
    assert tree.eval({"a": b, "b": a}) == Node(b, a, Node(b))


def test_match():
    a = Variable("a")
    b = Variable("b")
    tree1 = Node(a, b, Node(a))
    tree2 = Node(b, a, Node(b))
    assert tree1.match(tree2, {}) == {"a": b, "b": a}
    tree3 = Node(a, a, Node(a))
    assert tree1.match(tree3, {}) == {"a": a, "b": a}
    tree4 = Node(a, Node(a))
    assert tree1.match(tree4, {}) is None
    tree5 = Node(a, b, Node(b))
    assert tree1.match(tree5, {}) is None


def test_get():
    a = Variable("a")
    b = Variable("b")
    tree = Node(a, b, Node(b))
    assert tree.get([]) == tree
    assert tree.get([0]) == a
    assert tree.get([2, 0]) == b


def test_set():
    a = Variable("a")
    b = Variable("b")
    tree = Node(a, b, Node(b))
    assert tree.set([1], Node(a)) == b
    assert tree.get([1]) == Node(a)
    assert tree.set([1, 0], b) == a
    assert tree.get([1]) == Node(b)


def test_diff():
    a = Variable("a")
    b = Variable("b")

    tree1 = Node(Node(a, Node(a, b)))
    tree2 = Node(Node(a, Node(b, a)))
    tree3 = Node(Node(b, Node(a, b)))

    assert tree1.diff(tree2) == [0, 1]
    assert tree1.diff(tree1) is None
    assert tree1.diff(tree3) == [0, 0]
    assert a.diff(b) == []


def test_weak_diff():
    a = Variable("a")
    b = Variable("b")

    tree1 = Node(Node(a, Node(a, b)))
    tree2 = Node(Node(a, Node(b, a)))

    assert tree1.weak_diff(tree2) == [0, 1, 0]
    assert a.weak_diff(b) == []


def test_flatten():
    a = Variable("a")
    b = Variable("b")

    class Node1(Node):
        pass

    tree = Node(a, Node(b, Node1(a, b), a))
    assert tree.flatten() == [a, b, Node1(a, b), a]


def test_validate():
    a = Variable("a")
    b = Variable("b")
    tree = Node(Node(a, b), b)
    assert tree.validate()
