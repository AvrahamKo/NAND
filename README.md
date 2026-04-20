# NAND / nand2tetris

מאגר זה מרכז פתרונות ותרגילים לקורס **nand2tetris** (פרויקטים 0–12), כולל:

- מימושי חומרה ב־`HDL` (שערים, זיכרון, CPU ומחשב)
- תוכניות `Hack Assembly`
- מתרגם `VM` ב־Python (פרויקטים 7–8)
- כלי `JackAnalyzer` ו־`JackCompiler` ב־Python (פרויקטים 10–11)
- מחלקות מערכת ב־`Jack` (פרויקט 12)

## מבנה הפרויקט

- `00` – קבצי פתיחה
- `01` – לוגיקה קומבינטורית (`And`, `Mux`, `DMux`, וכו׳)
- `02` – אריתמטיקה ו־`ALU`
- `03` – רכיבי זיכרון (`Bit`, `Register`, `RAM`, `PC`)
- `04` – תוכניות `Hack Assembly` בסיסיות
- `05` – `CPU`, `Memory`, `Computer`
- `06` – Assembler ב־Python
- `07` – VM Translator (Stack Arithmetic + Memory Access)
- `08` – VM Translator (Program Flow + Function Calls)
- `09` – תוכניות Jack
- `10` – Jack Analyzer
- `11` – Jack Compiler
- `12` – ספריית מערכת ב־Jack (`Math`, `String`, `Memory`, וכו׳)

## דרישות

- `Python 3`
- כלי הקורס של nand2tetris (כמו Hardware Simulator / CPU Emulator / VM Emulator / TextComparer)

## הרצה מהירה

### פרויקט 6 – Assembler
```bash
cd 06
./Assembler path/to/file.asm
```

### פרויקטים 7–8 – VM Translator
```bash
cd 07
./VMtranslator path/to/input.vm

cd ../08
./VMtranslator path/to/folder_or_vm_file
```

### פרויקט 10 – JackAnalyzer
```bash
cd 10
./JackAnalyzer path/to/file_or_folder
```

### פרויקט 11 – JackCompiler
```bash
cd 11
./JackCompiler path/to/file_or_folder
```

## בדיקות

רוב התיקיות כוללות קבצי בדיקה של nand2tetris (`.tst`, `.cmp`, `.out`).
ניתן להריץ אותן דרך הסימולטורים של הקורס בהתאם לפרויקט.

## רישיון וזכויות

חלק מהקבצים במאגר מבוססים על תשתית הקורס nand2tetris והרחבות הקורס באוניברסיטה העברית, בהתאם להערות הרישוי שמופיעות בקבצים עצמם.
