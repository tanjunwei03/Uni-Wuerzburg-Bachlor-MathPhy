"""Module for Wordie, a word ladder game."""

import collections
import itertools
import random
import sys
from typing import Iterable

from wordgraph import (
    Word,
    WordGraph,
    breadth_first_search,
    create_graph,
    shortest_path,
)


def clean_words(src: Iterable[str]) -> set[Word]:
    """Return a set of words from a string source.

    The source could be an opened file, a generator expression, or a finite
    collection such as a list or a set. No assumption is made about
    the contents of the source; non-word elements are discarded.

    The words in the resulting list are normalised to lowercase.
    The length-check is done after stripping whitespace. The
    resulting list can be in any order.

    >>> sorted(clean_words(["abc", " DeF", "ghij"]))
    ['abc', 'def', 'ghij']

    >>> sorted(clean_words({"foo", "0", "B", "ar", "."}))
    ['ar', 'b', 'foo']

    >>> sorted(clean_words(s for s in ["foo", "0", "B", "ar", "."]))
    ['ar', 'b', 'foo']

    >>> clean_words({"A", "BC", "DEF", "12345678"}) == {"a", "bc", "def"}
    True
    """
    stripped = (raw.strip() for raw in src)
    words = (string for string in stripped if string.isalpha())
    return {word.lower() for word in words}


def read_words(filename: str) -> list[str]:
    """Read all words from a file."""
    with open(filename) as src:
        return clean_words(src)


def play_round(start: Word, goal: Word, graph: WordGraph):
    """Play a round of Wordie with the given start, goal, and word graph."""
    word = start
    while True:
        state = f"Current word is '{word}', goal is '{goal}'"
        commands = "Commands: n (show neighbors), h (show hint), q (quit), or enter the next word"
        print(f"\n{state}\n{commands}")
        neighbors = graph[word]
        entered = input("> ").lower()
        if entered == "q":
            print("Round aborted.")
            return
        elif entered == "n":
            print(f"Neighbors of '{word}': {", ".join(neighbors)}")
        elif entered == "h":
            path = shortest_path(word, goal, graph)
            if len(path) < 2:
                # If every function was implemented correctly, this cannot happen.
                print("Something went wrong. Check your implementation.")
            else:
                print(f"Ideal next word: {path[1]}")
        elif entered == "":
            pass
        else:
            if entered not in words:
                print(f"'{entered}' is not in the list of words")
            elif entered not in neighbors:
                print(f"'{entered}' is not a neighbor of '{word}'")
            elif entered == goal:
                print("You win!")
                return
            else:
                word = entered


def choose_start_end(
    words: list[Word], graph: WordGraph, max_tries: int = 8
) -> tuple[Word, Word] | None:
    """Choose a suitable start/end pair among the given words.

    If no suitable pair can be found, `None` is returned.
    """
    for _ in range(max_tries):
        start = random.choice(words)
        bfs_tree = breadth_first_search(start, graph)
        # Target should not be the start word or one of its direct neighbors
        possible_targets = list(bfs_tree.keys() - {start} - graph[start])
        if len(possible_targets) > 0:
            target = random.choice(possible_targets)
            return (start, target)
    # No start/target combination found, might not exist
    return None


def main(words: set[Word]):
    """Start a game of Wordie."""
    words_by_len = {}
    for word in words:
        n = len(word)
        if n in words_by_len:
            words_by_len[n].append(word)
        else:
            words_by_len[n] = [word]
    print(f"Welcome to Wordie! Playing with {len(words)} words.\n")
    print(
        """Instructions:
    For words of a given length, try to find a path from the starting
    word to the goal. Consecutive words in that path must have the
    same length and differ in exactly one place. All words must be
    in the word list provided.
    """
    )

    min_len = min(words_by_len.keys())
    max_len = max(words_by_len.keys())

    while True:
        n = int(input(f"Word length for this round? ({min_len} - {max_len}) "))
        if n < 2:
            print("This wouldn't be fun, choose a larger number.")
            continue
        elif n not in words_by_len:
            print("I have no words with that length.")
            continue

        words = words_by_len[n]
        graph = create_graph(words)
        start_end = choose_start_end(words, graph)
        if start_end is None:
            print(f"Error: no suitable start/end pair found with length {n}")
            continue
        else:
            start, target = start_end
            play_round(start, target, graph)
            response = ""
            while response not in ["y", "n"]:
                response = input("Play again? (y/n) ")[:1].lower()
            if response == "y":
                continue
            else:
                print("Thanks for playing!")
                return


if __name__ == "__main__":
    if len(sys.argv) == 2:
        words = read_words(sys.argv[1])
        main(words)
    else:
        print(f"usage: {sys.argv[0]} <word_list_file>", file=sys.stderr)
        sys.exit(1)
