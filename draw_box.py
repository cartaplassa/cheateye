from functools import reduce
from collections import namedtuple

ERR_FAILED_INIT = "Broken data, can't initialize Box"
Entry = namedtuple("Entry", "type k v")

def debug(var):
    print(f'{type(var)}:{var}')
    return var

class Box:
    def __init__(self, TextIOStream):
        key = ""
        self.entries = []
        is_first_entry = True
        for line in TextIOStream:
            line = line.strip()
            if line == "":
                continue
            if is_first_entry:
                entry = Entry("name", None, line)
                self.entries.append(entry)
                is_first_entry = False
            elif line[0] == "#":
                if key:
                    raise Exception(ERR_FAILED_INIT)
                entry = Entry("heading", None, line[1:])
                self.entries.append(entry)
            elif line == "-":
                if key:
                    raise Exception(ERR_FAILED_INIT)
                entry = Entry("separator", None, None)
                self.entries.append(entry)
            elif not key:
                key = line
            elif key:
                entry = Entry("data", key, line)
                self.entries.append(entry)
                key = ""
            else:
                raise Exception('Unhandled case in Box.__init__')
            is_first_entry = False
        # debug(self.entries)

    def __place_at_center(self, str: str, limit: int):
        output = []
        for line in [ str[i:i+limit] for i in range(0, len(str), limit) ]:
            amount = limit - len(line)
            after = amount // 2 if amount % 2 == 0 else amount // 2 + 1
            output.append("║ " + " "*(amount // 2) + line + " "*after + " ║")
        return output
    
    def __fit_to_width(self, str: str, limit: int):
        if len(str) > limit:
            raise Exception('String larger than limit')
        return str + ' '*(limit - len(str))
    
    def draw(self, limit=0):
        """ If w_limit is set, k_limit is calculated and left column entries
        are broken into parts. Otherwise, w_limit is calculated based on
        longest entry from each column.

        *------------ limit ------------*
        ╔═══════════════════════════════╗
        ║ *--------- w_limit ---------* ║
        ╟───────────────┬───────────────╢
        ║ *- k_limit -* │ *- v_limit -* ║
        ╚═══════════════╧═══════════════╝
        """
        data = list(filter(lambda x: x.type == "data", self.entries))
        v_limit = max(len(each.v) for each in data if isinstance(each.v, str))
        if limit > 0:
            w_limit = limit - 4
            k_limit = w_limit - v_limit - 3
        else:
            k_limit = max(len(each.k) for each in data if isinstance(each.k, str))
            w_limit = k_limit + v_limit + 3

        output = []
        # print(w_limit, k_limit, v_limit) # DEBUG
        output.append("╔═" + "═"*(w_limit) + "═╗")
        # w_limit - 4 if w_limit > 0 else k_limit + v_limit + 3
        output += self.__place_at_center(self.entries[0].v, w_limit)
        try:
            if self.entries[1].type == "heading":
                output.append("╟─" + "─"*k_limit + "───" + "─"*v_limit + "─╢")
            else:
                output.append("╟─" + "─"*k_limit + "─┬─" + "─"*v_limit + "─╢")
        except IndexError:
            print("Empty cheatsheet")
        
        is_first_entry = True
        for entry in self.entries:
            if entry.type == "name" and is_first_entry:
                continue
            elif entry.type == "heading":
                if not is_first_entry:
                    output.append("╟─" + "─"*k_limit + "─┴─" + "─"*v_limit + "─╢")
                output += self.__place_at_center(entry.v, w_limit)
                output.append("╟─" + "─"*k_limit + "─┬─" + "─"*v_limit + "─╢")
            elif entry.type == 'separator':
                output.append("╟─" + "─"*k_limit + "─┼─" + "─"*v_limit + "─╢")
            elif entry.type == 'data':
                is_first_line = True
                for line in [ entry.k[i:i+k_limit] for i in range(0, len(entry.k), k_limit) ]:
                    k = self.__fit_to_width(line, k_limit)
                    v = (self.__fit_to_width(entry.v, v_limit) if is_first_line else " "*v_limit)
                    output.append("║ " + k + " │ " + v + " ║")
                    is_first_line = False
            else:
                raise Exception('Invalid entry type: ', entry)
            is_first_entry = False
        
        output.append("╚═" + "═"*k_limit + "═╧═" + "═"*v_limit + "═╝")
        return {"content": output, "len": len(output)}
    
    # def height(self, w_limit=0):
    #     if w_limit <= 0:
    #         return len(self.entries) + 4
    #     v_limit = len(max(self.entries.values(), key=len))
    #     k_limit = w_limit - v_limit - 7
    #     lines = reduce(lambda acc, x: acc + len(x) // k_limit + 1, self.entries.keys(), 0)
    #     return lines + 4
    def height(self, w_limit=0):
        return len(self.draw(w_limit))

    def print(self, w_limit=0):
        for line in self.draw(w_limit)["sheet"]:
            print(line)



        # self.entries = []
        # is_first_line = True
        # key = ""
        # for line in sequence:
        #     if is_first_line:
        #         self.name = line.rstrip()
        #         is_first_line = False
        #         continue
        #     if line == "---":
        #         if key:
        #             raise Exception("Key w/o value")
        #         self.entries.append('---')
        #     if line[0:1] == '# ':
        #         if key:
        #             raise Exception("Key w/o value")
        #         self.entries.append
        #     if not key:
        #         key = line.rstrip()
        #         continue
        #     self.entries[key] = line.rstrip()
        #     key = ""
        # if key:
        #     raise Exception("Key w/o value")