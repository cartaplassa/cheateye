import shutil
import os
import sys

from draw_box import Box
from fill_viewport import fill_viewport
from random import random


WRONG_ARGS = 'Execute "main.py -f N", to divide space to N columns\n' \
'Execute "main.py -w N", to divide space to N-wide columns'

def main(width):
    items = []
    for filename in os.listdir(os.path.join(os.getcwd(), 'lists'))[::-1]:
        with open(os.path.join(os.getcwd(), 'lists', filename), 'r') as f:
            items.append(Box(f).draw(width))
    # distribute(items, 5, 40)
    # for item in items:
    #     item.print(40)
    return items

def random_boxes(amount, width):
    items = []
    for each in range(amount):
        f = []
        entries = int(random() * 12 + 4)
        longest_v = int(random() * 4 + 4)
        f.append(f'RANDOM BOX OF {entries} VALUES')
        for entry in range(entries):
            f.append('K'+'k'*int(random()*30+19))
            f.append('v'*int(random()*(longest_v-2)+2))
        box = Box(f)
        # box.print(40)
        items.append(Box(f).draw(width))
    return items


if __name__ == "__main__":
    args = sys.argv
    terminal_size = shutil.get_terminal_size().columns
    print(args, terminal_size)
    try: 
        if args[1] == '-f':
            columns = int(args[2])
            width = terminal_size // columns
        elif args[1] == '-w':
            width = int(args[2])
            columns = terminal_size // width
        else:
            print(WRONG_ARGS)
    except IndexError:
        print(WRONG_ARGS)
    boxes = main(width)
    fill_viewport(boxes, columns, width)