"""Module for word graphs, meant to support a word ladder game."""

from typing import TypeVar, Iterable
from queue import Queue
# This allows us to use `T` as a placeholder in type annotations.
# We can now describe some relationships between types without restricting
# ourselves to types known in advance.
T = TypeVar("T")
# Word describes a string consisting purely of (lowercase) alphabetic characters.
# Two words are considered similar (neighbors) if they are of the same length
# and can be transformed into each other via a one-character substitution.
Word = str
# Graph describes a general graph via adjacency sets. The type placeholder
# `T` denotes that each node maps to a set of other nodes.
Graph = dict[T, set[T]]
# WordGraph describes relationships between words. Neighboring words are
# connected by an edge. The graph is stored via adjacency sets.
WordGraph = dict[Word, set[Word]]
# WordPath describes a series of words where each word is a neighbor
# (in the sense outlined above) to its successor.
WordPath = list[Word]


def are_neighbors(word1: Word, word2: Word) -> bool:
    """Determine whether two words are neighbors in a word graph.

    Return True if the words are the same length and differ in exactly
    one position.

    >>> are_neighbors("  1", "1  ")
    False
    >>> are_neighbors("abc", "abd")
    True
    >>> are_neighbors("foo", "bar")
    False
    >>> are_neighbors("abcd", "abc")
    False
    >>> are_neighbors("foo", "foo")
    False
    """
    if len(word1) != len(word2):
        return False

    count = 0
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            count += 1
    return count == 1


def add_to_graph(graph: WordGraph, new_word: Word):
    """Add a new word to an existing word graph.

    The graph argument may be changed by this function.

    >>> graph = dict()
    >>> add_to_graph(graph, "foo")
    >>> graph["foo"]
    set()
    >>> add_to_graph(graph, "for")
    >>> graph["foo"]
    {'for'}
    >>> add_to_graph(graph, "far")
    >>> graph["for"] == {"far", "foo"}
    True
    """
    newAdjLst = []
    for i in graph:
        if are_neighbors(i, new_word):
            graph[i].add(new_word)
            newAdjLst.append(i)
    graph[new_word] = set(newAdjLst)


def create_graph(words: Iterable[Word]) -> WordGraph:
    """Turn a collection of words into a word graph.

    The collection can be any iterable, for instance a list,
    a set, or a generator expression, among others. Ensuring
    that all elements are proper words in the sense defined
    above is the caller's responsibility.

    >>> words = ["foo", "for", "far", "bar"]
    >>> g = create_graph(words)
    >>> g["foo"]
    {'for'}
    >>> sorted(g["far"])
    ['bar', 'for']
    """
    graph = dict()
    for i in words:
        lst = []
        for j in words:
            if are_neighbors(i,j):
                lst.append(j)
        graph[i] = set(lst)
    return graph


def breadth_first_search(start: T, graph: Graph[T]) -> dict[T, T | None]:
    """Determine the set of predecessors for each node via BFS.

    When the graph is disconnected, not all nodes will appear in the
    resulting predecessor map.

    >>> graph = {"a": set(), "b": set()}  # Fully disconnected
    >>> breadth_first_search("a", graph)
    {'a': None}

    >>> graph = {"foo": {"bar"}, "bar": {"foo"}}
    >>> breadth_first_search("foo", graph) == {'foo': None, 'bar': 'foo'}
    True

    >>> graph = {1: {2}, 2: {1, 3}, 3: {2, 4}, 4: {3}}
    >>> breadth_first_search(1, graph) == {1: None, 2: 1, 3: 2, 4: 3}
    True
    """
    predecessor = dict()
    predecessor[start] = None
    q = Queue()
    q.put(start)
    while not q.empty():
        front = q.get()
        for i in graph[front]:
            if not i in predecessor:
                predecessor[i] = front
                q.put(i)
    return predecessor
    pass


def trace_path(target: T, predecessor: dict[T, T | None]) -> list[T]:
    r"""Determine a path to the target given a predecessor map.

    It is assumed that a start node exists, whose predecessor is `None`.
    If the target is not in the map or no full path can be traced from
    the start node, a ValueError is raised.

    # Error conditions: 1) no path  2) target has no predecessor
    >>> predecessor = {0: None, 2: 1}
    >>> trace_path(2, predecessor)
    Traceback (most recent call last):
      ...
    ValueError: ...
    >>> trace_path(3, predecessor)
    Traceback (most recent call last):
      ...
    ValueError: ...

    The predecessor tree in the following example looks like this:
           0
          / \
         1   2
        /   / \
       3   4   5
    >>> predecessor = {0: None, 1: 0, 2: 0, 3: 1, 4: 2, 5: 2}
    >>> trace_path(5, predecessor)
    [0, 2, 5]
    >>> trace_path(3, predecessor)
    [0, 1, 3]
    >>> trace_path(2, predecessor)  # Direct edge
    [0, 2]
    """
    lst = [target]
    t = target
    while t in predecessor:
        if predecessor[t] == None:
            lst.reverse()
            return lst
        else:
            t = predecessor[t]
            lst.append(t)
    raise ValueError("SOMETHING IS WRONG HELP HELP HELP PLEASE IM STUCK IN HIS BASEMENT AND HE MAKES ME WRITE CODE EVERY DAY HELP")
    pass


def shortest_path(start: T, target: T, graph: Graph[T]) -> list[T]:
    """Determine a shortest path from start to target within graph.

    When no path exists, a ValueError is raised. This could be due to
    a disconnected graph or because either the start or the target node
    is not contained in the graph at all.
    """
    predList = breadth_first_search(start,graph)
    return trace_path(target,predList)


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
