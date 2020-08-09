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
        self.mar = 0

        # Memory Data Register - holds the value to write or the value just read
        self.mdr = None

        # Flags Register - holds the current flags status
        self.fl = None

    def load(self):
        """Load a program into memory."""

        # Print an error if user did not provide a program to load
        # and exit the program
        if len(sys.argv) < 2:
            print("Please provide a file to open\n")
            print("Usage: filename file_to_open\n")
            sys.exit()

        try:
            # Open the file provided as the 2nd arg
            with open(sys.argv[1]) as file:
                for line in file:

                    # Split each line into an array, with '#' as the delimiter
                    comment_split = line.split('#')

                    # The first value in each array is a possible instruction
                    possible_instruction = comment_split[0]

                    # If the value is an empty string, this line is a comment
                    if possible_instruction == '':
                        continue

                    # If the value starts with a 1 or 0, it's an instruction
                    if possible_instruction[0] == '1' or possible_instruction[0] == '0':
                        # Get the first 8 values (remove trailing whitespace and
                        # chars)
                        instruction = possible_instruction[:8]

                        # Convert the instruction into an integer and store it
                        # in memory
                        self.ram[self.mar] = int(instruction, 2)

                        # Increment the memory address register value
                        self.mar += 1

        except FileNotFoundError:
                print(f'{sys.argv[0]}: {sys.argv[1]} not found')
                sys.exit()


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

    def ram_write(self, address, value):
        """
        Should accept a value to write, and the address to write to
        """
        self.mar = address
        self.mdr = value

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

            # Halt the CPU
            if self.ir == HLT:
                running = False

            # Set the value of a register to an integer
            if self.ir == LDI:
                self.ram_write(operand_a, operand_b)

            # Print the decimal integer value stored in the given register
            if self.ir == PRN:
                number = self.ram_read(operand_a)
                print(number)

            # Point the PC to the next instruction in memory
            self.pc += num_operands + 1



