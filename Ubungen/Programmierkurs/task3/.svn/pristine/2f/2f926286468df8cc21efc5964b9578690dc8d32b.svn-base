from dataclasses import dataclass

import matplotlib.pyplot as plt

import lindenmayer as lm


@dataclass
class LSystem:
    axiom: str
    rules: dict[str, str]
    angle: float


lsystems = {
    'koch': LSystem(axiom='F', rules={'F': 'F+F-F-F+F'}, angle=90),
    'hilbert': LSystem(axiom='x', rules={'x': '+yF-xFx-Fy+', 'y': '-xF+yFy+Fx-'}, angle=90),
    'sierpinsky': LSystem(axiom='F-G-G', rules={'F': 'F-G+F+G-F', 'G': 'GG'}, angle=120),
    'sierpinsky_arrowhead': LSystem(axiom='F', rules={'F': 'G-F-G', 'G': 'F+G+F'}, angle=60),
    'sierpinsky_square': LSystem(axiom='F+xF+F+xF', rules={'x': 'xF-F+F-xF+F+xF-F+F-x'}, angle=90),
    'dragon_curve': LSystem(axiom='F', rules={'F': 'F+G', 'G': 'F-G'}, angle=90),
    'plant1': LSystem(axiom='F', rules={'F': 'F[+F]F[-F]F'}, angle=25.7),
    'plant2': LSystem(axiom='x', rules={'F': 'FF', 'x': 'F-[[x]+x]+F[+Fx]-x'}, angle=22.5),
    'plant3': LSystem(axiom='F', rules={'F': 'FF+[+F-F-F]-[-F+F+F]'}, angle=22.5),
}


def plot_lines(lines):
    """Plot the given lines with matplotlib."""
    fig, ax = plt.subplots()
    for line in lines:
        ax.plot(*zip(*line), 'k')
    ax.axis('equal')
    ax.axis('off')
    ax.set_frame_on(False)
    plt.show()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print(f"usage: {sys.argv[0]} <name> <iteration> [<filename>]", file=sys.stderr)
        sys.exit(1)

    name = sys.argv[1]
    if name not in lsystems:
        print(f'not a known L-system: "{name}"')
        sys.exit(2)

    ls = lsystems[name]
    it = int(sys.argv[2])
    word = lm.generate_word(ls.axiom, ls.rules, it)
    print(f'Iteration {it} of system "{name}" results in the word:\n{word}')
    coords = lm.word_to_lines(word, ls.angle)
    plot_lines(coords)
    if len(sys.argv) > 3:
        plt.savefig(sys.argv[3], bbox_inches="tight")
