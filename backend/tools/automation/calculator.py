"""Safe math evaluator using AST whitelist."""
from __future__ import annotations
import ast, math, operator

from backend.tools.base import BaseTool

_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Mod: operator.mod, ast.Pow: operator.pow,
    ast.USub: operator.neg, ast.UAdd: operator.pos, ast.FloorDiv: operator.floordiv,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and hasattr(math, node.func.id):
        return getattr(math, node.func.id)(*(_eval(a) for a in node.args))
    raise ValueError("unsupported expression")


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Evaluate a math expression. Args: expression."

    async def run(self, expression: str) -> float:
        tree = ast.parse(expression, mode="eval")
        return _eval(tree.body)
