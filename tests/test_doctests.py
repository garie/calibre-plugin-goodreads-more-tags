"""
Run the doctests in the plugin's source.

calibre's bundled Python runs with -OO, which strips docstrings at import time, so pytest's --doctest-modules finds
nothing to run. This reads the docstrings from the source files instead, and runs them against the installed module.
"""
import ast
import doctest
import importlib
import os.path

import pytest


SRC_DIR = os.path.join(os.path.dirname(__file__), '..', 'src', 'goodreads_more_tags')
MODULES = ['worker']


def collect_doctests():
    parser = doctest.DocTestParser()
    for module_name in MODULES:
        filename = os.path.join(SRC_DIR, module_name + '.py')
        with open(filename) as f:
            # optimize = 0 keeps the docstrings, which ast.parse drops when the interpreter runs with -OO.
            tree = compile(f.read(), filename, 'exec', ast.PyCF_ONLY_AST, optimize = 0)

        scopes = [(node, []) for node in tree.body]
        while scopes:
            node, parents = scopes.pop(0)
            if not isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            path = parents + [node.name]
            scopes.extend((child, path) for child in node.body)

            docstring = ast.get_docstring(node, clean = False)
            if not docstring or not parser.get_examples(docstring):
                continue
            name = '{}.{}'.format(module_name, '.'.join(path))
            yield pytest.param(module_name, name, docstring, filename, node.body[0].lineno, id = name)


DOCTESTS = list(collect_doctests())


def test_doctests_found():
    # An empty parametrize is reported as a skip, which would hide doctests that silently stopped being collected.
    assert DOCTESTS


@pytest.mark.parametrize('module_name, name, docstring, filename, lineno', DOCTESTS)
def test_doctest(module_name, name, docstring, filename, lineno):
    module = importlib.import_module('calibre_plugins.goodreads_more_tags.' + module_name)
    test = doctest.DocTestParser().get_doctest(docstring, dict(vars(module)), name, filename, lineno)
    runner = doctest.DocTestRunner(optionflags = doctest.ELLIPSIS)
    output = []
    runner.run(test, out = output.append)
    assert runner.failures == 0, ''.join(output)
