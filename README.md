# NAND / nand2tetris

This repository contains solutions and exercises for the **nand2tetris** course (projects 0–12), including:

- Hardware implementations in `HDL` (gates, memory, CPU, and computer)
- `Hack Assembly` programs
- `VM` translator in Python (projects 7–8)
- `JackAnalyzer` and `JackCompiler` tools in Python (projects 10–11)
- Jack operating system classes (project 12)

## Project Structure

- `00` – Introductory files
- `01` – Boolean logic (`And`, `Mux`, `DMux`, etc.)
- `02` – Arithmetic and `ALU`
- `03` – Memory chips (`Bit`, `Register`, `RAM`, `PC`)
- `04` – Basic `Hack Assembly` programs
- `05` – `CPU`, `Memory`, `Computer`
- `06` – Assembler (Python)
- `07` – VM Translator (Stack Arithmetic + Memory Access)
- `08` – VM Translator (Program Flow + Function Calls)
- `09` – Jack programs
- `10` – Jack Analyzer
- `11` – Jack Compiler
- `12` – Jack OS standard library (`Math`, `String`, `Memory`, etc.)

## Requirements

- `Python 3`
- nand2tetris course tools (Hardware Simulator / CPU Emulator / VM Emulator / TextComparer)

## Quick Start

### Project 6 – Assembler
```bash
cd 06
./Assembler path/to/file.asm
```

### Projects 7–8 – VM Translator
```bash
cd 07
./VMtranslator path/to/input.vm

cd ../08
./VMtranslator path/to/folder_or_vm_file
```

### Project 10 – JackAnalyzer
```bash
cd 10
./JackAnalyzer path/to/file_or_folder
```

### Project 11 – JackCompiler
```bash
cd 11
./JackCompiler path/to/file_or_folder
```

## Testing

Most directories include nand2tetris test files (`.tst`, `.cmp`, `.out`).
Run them using the appropriate course simulator for each project.

## License

Some files in this repository are based on the nand2tetris course infrastructure and extensions developed at The Hebrew University, subject to the license notices found within each file.
