from prtpy import partition
from random import random
from typing import Callable, List, Any
import prtpy
from prtpy import outputtypes as out, objectives as obj, Binner
from prtpy.packing import first_fit

def multifit(binner: Binner, numbins: int, items: List[any], iterations = 10):
    sum_values = sum(map(binner.valueof, items))
    max_values = max(map(binner.valueof, items))
    # With bin-capacity smaller than this, every packing must use more than `numbins` bins.
    lower_bound = max(sum_values/numbins, max_values)  
    # With this bin-capacity, FFD always uses at most `numbins` bins.
    upper_bound = max(2*sum_values/numbins, max_values) 
    sorted_items = sorted(items, key=binner.valueof, reverse=True)
    for _ in range(iterations):
        binsize = (lower_bound+upper_bound)/2
        ffd_num_of_bins = prtpy.pack(
            algorithm=prtpy.packing.first_fit, 
            binsize=binsize, 
            items=sorted_items, 
            valueof=binner.valueof, 
            outputtype=out.BinCount
        )
        if ffd_num_of_bins <= numbins:
            upper_bound = binsize
        else:
            lower_bound = binsize
            
    return first_fit.online(binner, binsize=upper_bound, items=sorted_items)

def distribute(items, bins):
    data = {i: items[i]["len"] for i in range(len(items))}
    # print(data)
    normalized = partition(
        algorithm=multifit, 
        numbins=bins, 
        items=data
    )
    # print(normalized) 
    return normalized # Normalized list of indeces

def join_column(column, width):
    # DEBUG
    # temp = [item['len'] for item in column]
    # print(temp, sum(temp))

    acc = []
    is_first_item = True
    last_line = ''
    for item in column:
        if is_first_item:
            acc.append("╔"+"═"*(width-2)+"╗")
            is_first_item = False
        else: # "╠"+"═"*(width-2)+"╣"
            acc.append(last_line.replace("╚","╠").replace("╝","╣"))
        for line in item["content"][1:-1]:
            acc.append(line)
        last_line = item["content"][-1]
    acc.append(last_line.replace("╠","╚").replace("╣","╝"))
    return {"content": acc, "len": len(acc)}

def join_table(columns):
    table = []
    for i in range(columns[0]["len"]):
        row = []
        for column in columns:
            try:
                row.append(column['content'][i])
            except IndexError:
                pass
        row = ''.join(row)
        row = row.replace('╗╔', '╦') \
                 .replace('║║', '║') \
                 .replace('╣║', '╣') \
                 .replace('║╠', '╠') \
                 .replace('╣╠', '╬') \
                 .replace('╝╚', '╩') \
                 .replace('╢║', '╢') \
                 .replace('║╟', '╟') \
                 .replace('╢╟', '╫') \
                 .replace('║╚', '╠') \
                 .replace('╢╠', '╬') \
                 .replace('╣╟', '╬') \
                 .replace('╢╚', '╬')
        table.append(row)
        print(row)
    return table

def fill_viewport(items, bins, width):
    # print([item['len'] for item in items])
    # join_column(items, width)

    sorted = [[items[i] for i in pile] for pile in distribute(items, bins)]
    columns = []
    for column in sorted:
        columns.append(join_column(column, width))
    columns.sort(key= lambda x: x['len'],reverse=True)
    join_table(columns)
    


if __name__ == "__main__":
    items = {}
    items["a"] = 45
    for each in "bcdefghij":
        items[each] = int(random() * 25 + 5)
    print(items)
    normalized = partition(
        algorithm=multifit, 
        numbins=5, 
        items=items, # {"a":1, "b":2, "c":3, "d":4, "e":10, "f":7}
    )
    print(normalized)
    values = [[items[i] for i in each] for each in normalized]
    print(values)
    print([sum(each) for each in values])