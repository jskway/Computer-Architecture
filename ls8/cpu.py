"""CPU functionality."""

import sys

"""Instruction Opcodes"""
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        # Initialize ram to hold 256 bytes of memory
        byte = [0] * 8
        self.ram = [byte] * 256

        # Eight general purpose registers
        self.reg = [byte] * 8

        ## Internal Registers

        # Program Counter - address of the currently executing instruction
        self.pc = 0

        # Instruction Register - contains a copy of the currently executing
        # instruction
        self.ir = None

        # Memory Address Register - holds the memory address we're reading or
        # writing
        self.mar = None

        # Memory Data Register - holds the value to write or the value just read
        self.mdr = None

        # Flags Register - holds the current flags status
        self.fl = None

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        """
        Should accept the address to read and return the value stored there
        """
        self.mar = address
        self.mdr = self.ram[self.mar]

        return self.mdr

    def ram_write(self, value, address):
        """
        Should accept a value to write, and the address to write to
        """
        self.mdr = value
        self.mar = address

        self.ram[self.mar] = self.mdr

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            # Get the current instruction
            instruction = self.ram_read(self.pc)

            # Store a copy of the current instruction in IR register
            self.ir = instruction

            # Get the number of operands
            num_operands = instruction >> 6

            # Store the bytes at PC+1 and PC+2 
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if command == HLT:
                running = False

            # Point the PC to the next instruction in memory
            self.pc += num_operands + 1



