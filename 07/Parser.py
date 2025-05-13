"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    # Parser
    
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.

    ## VM Language Specification

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly 
    commands. VM commands may be separated by an arbitrary number of whitespace
    characters and comments, which are ignored. Comments begin with "//" and
    last until the line’s end.
    The different parts of each VM command may also be separated by an arbitrary
    number of non-newline whitespace characters.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that, 
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_file.read().splitlines()
        self.input_lines = []
        split_line = []
        for line in input_file:
            # Remove leading and trailing whitespace
            if line and not line.startswith("//"):
                split_line = line.split("//")
                line = split_line[0]
                line = line.strip()
                # Skip empty lines and lines starting with '//'
            if line and not line.startswith("//"):
                self.input_lines.append(line)
        self.current_command = ""

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        return bool(self.input_lines)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        # Your code goes here!
        if self.has_more_commands():
            # Remove the first command from the list and set it as the current command
            self.current_command = self.input_lines.pop(0)

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        # Your code goes here!
        # Check for arithmetic commands
        if self.current_command in {'add', 'sub', 'and', 'or', 'eq', 'gt', 'lt', 'neg', 'not','shiftleft', 'shiftright'}:
            return "C_ARITHMETIC"
        # Check for push commands
        elif self.current_command.startswith('push'):
            return "C_PUSH"
        # Check for pop commands
        elif self.current_command.startswith('pop'):
            return "C_POP"
        else:
            # If command type is not recognized, return an empty string or raise an error
            return ""


    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        # Your code goes here!
        command_type = self.command_type()
        if command_type == "C_ARITHMETIC":
            return self.current_command
        else:
            # For other command types, the first argument is typically the command after splitting by spaces
            return self.current_command.split()[1]

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        # Your code goes here!
        command_type = self.command_type()
        if command_type in {"C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"}:
            # For these command types, the second argument is typically the integer after splitting by spaces
            return int(self.current_command.split()[2])
        else:
            raise ValueError("arg2() should be called only for C_PUSH, C_POP, C_FUNCTION, or C_CALL commands.")
