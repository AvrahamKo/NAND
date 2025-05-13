"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output_stream = output_stream
        self.filename = None
        self.label_counter = 0

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.filename = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        if command in {'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'}:
            self._write_basic_arithmetic(command)
        else:
            raise ValueError(f"Invalid arithmetic command: {command}")

    def _write_basic_arithmetic(self, command: str) -> None:
        """Writes assembly code for basic arithmetic commands."""
        if command == 'add':
            self._write_addition()
        elif command == 'sub':
            self._write_subtraction()
        elif command == 'neg':
            self._write_negation()
        elif command == 'eq':
            self._write_comparison('JEQ')
        elif command == 'gt':
            self._write_comparison('JGT')
        elif command == 'lt':
            self._write_comparison('JLT')
        elif command == 'and':
            self._write_logical('AND')
        elif command == 'or':
            self._write_logical('OR')
        elif command == 'not':
            self._write_logical('NOT')

    def _write_addition(self) -> None:
        """Writes assembly code for addition."""
        self._write_binary_operation('+')

    def _write_subtraction(self) -> None:
        """Writes assembly code for subtraction."""
        self._write_binary_operation('-')

    def _write_binary_operation(self, operation: str) -> None:
        """Writes assembly code for binary operations (+, -)."""
        self.output_stream.write(f"@SP\n")
        self.output_stream.write(f"AM=M-1\n")
        self.output_stream.write(f"D=M\n")
        self.output_stream.write(f"A=A-1\n")
        self.output_stream.write(f"M=M{operation}D\n")

    def _write_negation(self) -> None:
        """Writes assembly code for negation."""
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M-1\n")
        self.output_stream.write("M=-M\n")

    def _write_comparison(self, jump_type: str) -> None:
        """Writes assembly code for comparison operations (eq, gt, lt)."""
        true_label = f"TRUE_{self.label_counter}"
        end_label = f"END_{self.label_counter}"
        self.label_counter += 1

        # Subtract top two stack values and set D to the result
        self.output_stream.write("@SP\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M-1\n")
        self.output_stream.write("D=M-D\n")

        # Jump to true label if condition met, else jump to end label
        self.output_stream.write(f"@{true_label}\n")
        self.output_stream.write(f"D;{jump_type}\n")  # Jump if condition is true
        self.output_stream.write("D=0\n")  # Set D to false (0)
        self.output_stream.write(f"@{end_label}\n")
        self.output_stream.write("0;JMP\n")  # Jump to end label

        # True label, set D to true (-1)
        self.output_stream.write(f"({true_label})\n")
        self.output_stream.write("D=-1\n")

        # End label, push D to stack
        self.output_stream.write(f"({end_label})\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M-1\n")
        self.output_stream.write("M=D\n")

    def _write_logical(self, operation: str) -> None:
        """Writes assembly code for logical operations (and, or, not)."""
        if operation == 'NOT':
            self.output_stream.write("@SP\n")
            self.output_stream.write("A=M-1\n")
            self.output_stream.write("M=!M\n")
        else:
            self.output_stream.write("@SP\n")
            self.output_stream.write("AM=M-1\n")
            self.output_stream.write("D=M\n")
            self.output_stream.write("A=A-1\n")
            if operation == 'AND':
                self.output_stream.write("M=D&M\n")
            elif operation == 'OR':
                self.output_stream.write("M=D|M\n")

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.

        if command == 'C_PUSH':
            self._write_push(segment, index)
        elif command == 'C_POP':
            self._write_pop(segment, index)
        else:
            raise ValueError(f"Invalid command type: {command}")

    def _write_push(self, segment: str, index: int) -> None:
        """Writes assembly code for push command."""
        segment_symbols = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT'
        }
        if segment == 'constant':
            self.output_stream.write(f"@{index}\n")
            self.output_stream.write(f"D=A\n")
            self._push_to_stack()
        elif segment in {'local', 'argument', 'this', 'that'}:
            # Pushing from local, argument, this, or that segment
            segment = segment_symbols[segment]
            self.output_stream.write(f"@{segment}\n")
            self.output_stream.write("D=M\n")  # D = base address of segment
            self.output_stream.write(f"@{index}\n")
            self.output_stream.write("A=D+A\n")  # A = base address + index
            self.output_stream.write("D=M\n")  # D = value at address
            self._push_to_stack()

        elif segment == 'temp':
            # Pushing from temp segment
            self.output_stream.write(f"@{5 + index}\n")
            self.output_stream.write("D=M\n")  # D = value at address
            self._push_to_stack()

        elif segment == 'pointer':
            # Pushing from pointer segment
            self.output_stream.write(f"@{3 + index}\n")
            self.output_stream.write("D=M\n")  # D = value at address
            self._push_to_stack()

        elif segment == 'static':
            # Pushing from static segment
            self.output_stream.write(f"@{self.filename}.{index+16}\n")
            self.output_stream.write("D=M\n")  # D = value at address
            self._push_to_stack()

    def _push_to_stack(self) -> None:
        """Pushes the value in register D to the top of the stack."""
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("M=D\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("M=M+1\n")  # Increment stack pointer

    def _write_pop(self, segment: str, index: int) -> None:
        """Writes assembly code for pop command."""
        segment_symbols = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT'
        }

        #insert the top of the stack to R14
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("M=M-1\n")
        self.output_stream.write("@R14\n")
        self.output_stream.write("M=D\n")


        if segment in {'local', 'argument', 'this', 'that'}:
            self.output_stream.write(f"@{segment_symbols[segment]}\n")
        elif segment == 'temp':
            # Pushing from temp segment
            self.output_stream.write(f"@{5 + index}\n")
        elif segment == 'pointer':
            # Pushing from pointer segment
            self.output_stream.write(f"@{3 + index}\n")

        elif segment == 'static':
            # Pushing from static segment
            self.output_stream.write(f"@{self.filename}.{index + 16}\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write(f"@{index}\n")
        self.output_stream.write("D=D+A\n")
        self.output_stream.write("@R15\n")
        self.output_stream.write("M=D\n")
        self.output_stream.write("@R14\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@R15\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("M=D\n")




    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass
    
    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass
    
    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass
    
    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        pass
    
    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        pass
    
    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        pass
