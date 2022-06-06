import ast
import re
from typing import Any, Iterable, TextIO

curse_list = ["fuck", "bitch", "shit", "ass", "whore", "slut", "dick"]

def _is_profane(value: str) -> bool:
    words = []
    for curse in curse_list:
        if re.search(curse, value.lower()):
            words.append(curse)

    if words:
        return True, words
    else:
        return False, ""

class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_Name(self, node: ast.Name) -> Any:
        profane, words = _is_profane(node.id)
        if profane:
            for curse in words:
                self.errors.append(f"variable {node.id} should not include the word " + curse)
        return super().generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        profane, words = _is_profane(node.name)
        if profane:
            for curse in words:
                self.errors.append(f"class {node.name} should not include the word " + curse)
        return super().generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        profane, words = _is_profane(node.name)
        if profane:
            for curse in words:
                self.errors.append(f"function {node.name} should not include the word " + curse)
        return super().generic_visit(node)

def check_file(file: TextIO) -> Iterable[str]:
    code = file.read()
    tree = ast.parse(code)
    visitor = Visitor()
    visitor.visit(tree)

    return visitor.errors


if __name__ == "__main__":
    import sys

    path = sys.argv[1]
    with open(path, "r") as file:
        errors = check_file(file)

    exit_code = 0
    for error in errors:
        exit_code = 1
        print(f"{path}: {error}")

    sys.exit(exit_code)