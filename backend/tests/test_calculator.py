import asyncio
import pytest
from backend.tools.automation.calculator import CalculatorTool


@pytest.mark.asyncio
async def test_calculator_basic():
    tool = CalculatorTool()
    assert await tool.run(expression="2+2*3") == 8
    assert await tool.run(expression="sqrt(16)") == 4.0
