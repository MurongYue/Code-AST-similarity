import difflib
from ast import parse, NodeTransformer, copy_location, Name
import ast


class NormIdentifiers(NodeTransformer):
    def __init__(self):
        self.identifiers = {}
        super().__init__()

    def visit_Name(self, node):
        try:
            id = self.identifiers[node.id]
        except KeyError:
            id = f'id_{len(self.identifiers)}'
            self.identifiers[node.id] = id

        return copy_location(Name(id=id), node)


# class NormFunctions(NodeTransformer):
#     def __init__(self, func=None):
#         self.identifiers = {}
#         self.func = func
#         super().__init__()
#
#     def visit_FunctionDef(self, node):
#         if self.func and self.func != node.name:
#             return None
#
#         try:
#             name = self.identifiers[node.name]
#         except KeyError:
#             name = f'function{len(self.identifiers):x}'
#             self.identifiers[node.name] = name
#
#         for i, arg in enumerate(node.args.args):
#             arg.arg = f'arg{i}'
#
#         new_func = FunctionDef(name=name, args=node.args, body=node.body, decorator_list=node.decorator_list)
#
#         if isinstance(new_func.body[0], Expr) and isinstance(new_func.body[0].value, Str):
#             del new_func.body[0]
#
#         return copy_location(new_func, node)


def parse_code(code):
    tree = parse(code)  # parse code into the AST
    # tree = NormFunctions(func=None).visit(tree) # Normalize the function
    tree = NormIdentifiers().visit(tree)  # Normalize the identifiers
    d = ast.dump(tree)  # dump into string
    return d


def get_code_sim_score(code1, code2):
    tree1 = parse_code(code1)
    tree2 = parse_code(code2)
    pairs = difflib.SequenceMatcher(None, tree1, tree2).ratio()
    return pairs


if __name__ == '__main__':
    a = 'a=1\nb=2\nk=a+b\nd=3\nc=k+d\nans=c*0.5\nprint(ans)'
    b = 'a=1\nr=2\nk=a+r\nd=3\ncder=k+d\nans=c/4\nprint(ans)'
    c = "apple=1\nr=2\nk=apple+r\nd=3\nc=k+d\nans=c*2\nprint(ans)"
    print(get_code_sim_score(a, b))
    print(get_code_sim_score(a, c))
    print(get_code_sim_score(b, c))
