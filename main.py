import sys
import math

# Don't let the machines win. You are humanity's last hope...

if __name__ == '__main__':
    width = int(input())  # the number of cells on the X axis
    height = int(input())  # the number of cells on the Y axis
    lines = []
    for i in range(height):
        lines.append(input())  # width characters, each either 0 or .

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    for i in range(height):
        for j in range(width):
            if lines[i][j] == "0":
                print(f"{j} {i} ", end="")

                try:
                    if lines[i][j + 1] == "0":
                        print(f"{j + 1} {i} ", end="")
                    else:
                        print("-1 -1 ", end="")
                except IndexError:
                    print("-1 -1 ", end="")

                try:
                    if lines[i + 1][j] == "0":
                        print(f"{j} {i + 1}")
                    else:
                        print("-1 -1")
                except IndexError:
                    print("-1 -1")
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    # Three coordinates: a node, its right neighbor, its bottom neighbor
