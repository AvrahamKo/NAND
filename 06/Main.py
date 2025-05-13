"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")
    # Initialize a Parser object
    parser = Parser(input_file)
    # Initialize a symbol table to store label symbols and their corresponding addresses
    symbol_table = SymbolTable()

    # First pass: populate symbol table with label symbols and their addresses
    address = 0
    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()
        if command_type == "L_COMMAND":
            # For L_COMMAND, add the symbol and its address to the symbol table
            symbol = parser.symbol()
            symbol_table.add_entry(symbol, address)
        else:
            # For other command types, increment the address
            address += 1
    # Second pass: assemble instructions and write to output file
    input_file.seek(0)
    parser = Parser(input_file)
      # Reset parser to start from the beginning of the file
    cur = 16
    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()
        if command_type == "A_COMMAND":
            # For A_COMMAND, write the binary representation of the symbol/address to the output file
            symbol = parser.symbol()
            if symbol.isdigit():
                # If the symbol is a decimal number, write its binary representation
                address = int(symbol)
            else:
                if not symbol_table.contains(symbol):
                    address = cur
                    symbol_table.add_entry(symbol, cur)
                    cur = cur + 1
                else:
                    address = symbol_table.get_address(symbol)
            output_file.write(format(address, '016b') + "\n")
        elif command_type == "C_COMMAND":
            # For C_COMMAND, assemble and write the binary code to the output file
            code = Code
            dest = code.dest(parser.dest())
            comp = code.comp(parser.comp())
            jump = code.jump(parser.jump())
            if "<<" in parser.current_command or ">>" in parser.current_command:
                output_file.write("101" + comp + dest + jump + "\n")
            else:
                output_file.write("111" + comp + dest + jump + "\n")




if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
