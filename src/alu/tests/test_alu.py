import sys
import cocotb
from cocotb.triggers import Timer

sys.path.append("../../shared/tests")
from opcodes import *


async def test_op(dut, opcode, *operands):
    dut.a.value = operands[0] if len(operands) >= 1 else 0
    dut.b.value = operands[1] if len(operands) >= 2 else 0
    dut.opcode.value = opcode
    await Timer(10, "us")
    expected = OPFUNCS[opcode](*operands)
    assert dut.out.value == expected, f"{int(dut.out.value)} != {expected}"


@cocotb.test()
async def test_add(dut):
    await test_op(dut, ADD, 1, 2)

@cocotb.test()
async def test_adc(dut):
    await test_op(dut, ADC, 1, 2)

@cocotb.test()
async def test_sub(dut):
    await test_op(dut, SUB, 5, 1)

@cocotb.test()
async def test_and(dut):
    await test_op(dut, AND, 0xFFFF, 0x1234)

@cocotb.test()
async def test_or(dut):
    await test_op(dut, OR, 0xF0F0, 0x0F0F)

@cocotb.test()
async def test_xor(dut):
    await test_op(dut, XOR, 0b1010, 0b0110)

@cocotb.test()
async def test_cmp(dut):
    await test_op(dut, CMP, 666, 666)
    await test_op(dut, CMP, 1, 7)

@cocotb.test()
async def test_inc(dut):
    await test_op(dut, INC, 42)

@cocotb.test()
async def test_dec(dut):
    await test_op(dut, DEC, 42)

@cocotb.test()
async def test_shr(dut):
    await test_op(dut, SHR, 8, 2)

@cocotb.test()
async def test_shl(dut):
    await test_op(dut, SHL, 8, 2)
