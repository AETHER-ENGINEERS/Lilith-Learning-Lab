"""Compiler Design course, chapters 1-6."""
from clib import *

CHS = []

# ------------------------------------------------------------ 1
CHS.append(CH(
 "Overview of compilers",
 ("Language processing system", [
  "Compiler | translates | Source language to target language",
  "Preprocessor | prepares | Source code for the compiler",
  "Interpreter | executes | One statement at a time",
  "Assembler | produces | Object file",
  "Linker | merges | Object files into an executable",
  "Loader | places executable in | Memory",
  "Cross-compiler | runs on | Platform A for platform B",
  "Source-to-source compiler | outputs | Another high-level language"]),
 ["A compiler translates code written in one language into another language without changing the meaning. It is also expected to make the target code efficient in time and space.",
  "Compiler design covers translation, error detection and recovery. The front end is lexical, syntax and semantic analysis; the back end is code generation and optimization.",
  "A whole language processing system has more parts: a preprocessor, the compiler, an assembler, a linker and a loader. Related tools are the interpreter, the cross-compiler and the source-to-source compiler."],
 [("Compiler", "A program that translates a program in one language into an equivalent program in another."),
  ("Preprocessor", "Runs before the compiler: expands macros, includes files and removes comments."),
  ("Interpreter", "Reads a statement, converts it to intermediate code and executes it, then takes the next."),
  ("Assembler", "Translates assembly language into machine code in an object file."),
  ("Linker", "Merges object files and resolves references between them to make an executable."),
  ("Loader", "Part of the operating system that loads an executable into memory and starts it."),
  ("Cross-compiler", "Runs on one platform and generates code for another."),
  ("Source-to-source compiler", "Translates source in one high-level language into source in another.")],
 ["A compiler must preserve the meaning of the program.",
  "A compiler reads the whole program; an interpreter works statement by statement.",
  "The interpreter stops at the first error; a compiler keeps reading and reports many.",
  "Source goes through preprocessor, compiler, assembler, linker and loader.",
  "The linker resolves references between separately compiled modules.",
  "A cross-compiler runs on platform A and targets platform B."],
 [T("A compiler translates the code written in one language into some other language without changing the meaning of the program. It is also expected that a compiler should make the target code efficient and optimized in terms of time and space."),
  T("Compiler design principles give an in-depth view of the translation and optimization process. They cover basic translation mechanisms and error detection and recovery. The front end consists of lexical, syntax and semantic analysis. The back end consists of code generation and optimization."),
  T("To follow the course you need a basic understanding of at least one programming language. Exposure to assembly programming helps. The labs are in Python, and they build small working versions of the real components."),
  T("Source code does not become a running program in one step. A language processing system chains several tools. The first is the preprocessor. It runs before the compiler proper, and handles directives such as macro expansion and file inclusion.",
    "The compiler then translates the result into assembly language or another target. The assembler turns assembly into machine code in an object file. The linker merges object files, and the loader puts the executable in memory."),
  T("The interpreter, like a compiler, translates high-level language into lower-level form. The difference is in how it reads input. A compiler reads the whole source at once, creates tokens, checks semantics, generates intermediate code and may involve many passes. An interpreter reads a statement, converts it to intermediate code, executes it, then takes the next statement."),
  T("The error behaviour differs as well. If an error occurs, an interpreter stops execution and reports it, whereas a compiler reads the whole program even if it meets several errors."),
  T("The assembler translates assembly language into machine code. Its output is an object file, which contains machine instructions and the data needed to place them in memory."),
  T("The linker is a program that links and merges various object files to make an executable file. These files may have been produced by separate assemblers. Its major task is to search for and locate the referenced modules and routines, and to decide where the code will be loaded, so the instructions can have absolute references. A reference that no object file defines is an unresolved symbol and the link fails."),
  T("The loader is part of the operating system. It is responsible for loading executable files into memory and executing them. It calculates the size of the program, creates memory space for it, and initializes registers to start execution."),
  T("A cross-compiler runs on a platform A and generates executable code for a platform B. Phone apps are usually built this way, on a desktop. A source-to-source compiler takes source code in one language and produces source code in another."),
  T("In the practice section you write a tiny linker. It follows references from a main module, collects the modules it needs, and reports an unresolved symbol if one is missing.")],
 [("What does a compiler need to preserve?", ["Speed only", "The meaning of the program", "The comments", "The file names"], 1, "Translation must not change what the program means."),
  ("Which tool merges object files into an executable?", ["Assembler", "Linker", "Loader", "Preprocessor"], 1, "The linker resolves references between modules."),
  ("How does an interpreter treat an error?", ["Reads on and reports many", "Stops and reports it", "Ignores it", "Fixes it silently"], 1, "A compiler keeps reading the whole program."),
  ("What is a cross-compiler?", ["Runs on A and generates code for B", "A compiler with two inputs", "A debugger", "A faster interpreter"], 0, "Host and target platforms differ.")],
 [("What does the assembler produce?", "An object file."), ("Order of tools?", "Preprocessor, compiler, assembler, linker, loader."),
  ("Source-to-source compiler?", "Translates one high-level language to another."), ("Where is the loader?", "It is part of the operating system.")],
 [ORDER("Language processing system", "Put the tools in the order a program passes through them.", ["Preprocessor", "Compiler", "Assembler", "Linker", "Loader"]),
  MATCH("Tools", "Match each tool with what it does.", [("Preprocessor", "Expands macros and includes files"), ("Assembler", "Turns assembly into an object file"), ("Linker", "Merges object files and resolves references"), ("Loader", "Places the executable in memory"), ("Interpreter", "Executes statement by statement")]),
  PL("A tiny linker", "Each module is [name, defines, needs]: the symbols it provides and the symbols it needs. Write link(modules, main). Starting from the module called main, follow needs to the module that defines each symbol. Return the module names in the order they are first reached (main first, then depth-first). If some needed symbol is defined nowhere, return \"undefined: \" followed by that symbol.",
     "link(modules, main)", """
def link(modules, main):
    by_name = {}
    owner = {}
    for name, defines, needs in modules:
        by_name[name] = needs
        for s in defines:
            owner[s] = name
    order = []
    def visit(name):
        if name in order:
            return None
        order.append(name)
        for s in by_name[name]:
            if s not in owner:
                return "undefined: " + s
            r = visit(owner[s])
            if r:
                return r
        return None
    err = visit(main)
    if err:
        return err
    return order
""", [[[["main", ["main"], ["print", "sqrt"]], ["io", ["print"], []], ["math", ["sqrt"], ["abs"]], ["abs", ["abs"], []], ["unused", ["zzz"], []]], "main"],
        [[["main", ["main"], ["print", "log"]], ["io", ["print"], []]], "main"],
        [[["a", ["fa"], []]], "a"]],
     "Keep a map from symbol to the module that defines it. Visit main, then each needed symbol's owner, remembering modules already seen."),
  FILL("Overview", "A compiler reads the {{whole}} program, while an {{interpreter}} runs one statement at a time. A {{cross}}-compiler runs on one platform and targets another.")]))

# ------------------------------------------------------------ 2
CHS.append(CH(
 "Compiler architecture",
 ("Analysis and synthesis", [
  "Compiler | is divided into | Analysis phase and synthesis phase",
  "Analysis phase | is also called | Front end",
  "Synthesis phase | is also called | Back end",
  "Analysis phase | produces | Intermediate representation",
  "Analysis phase | produces | Symbol table",
  "Synthesis phase | consumes | Intermediate representation [ch3]",
  "Pass | is | One traversal of the whole program",
  "Phase | is | A distinguishable stage"]),
 ["A compiler splits into two parts. The analysis phase, the front end, reads the source, divides it into core parts and checks for lexical, grammar and syntax errors. It produces an intermediate representation and a symbol table.",
  "The synthesis phase, the back end, generates the target program from the intermediate representation and the symbol table.",
  "A pass is one traversal of the entire program. A phase is a distinguishable stage that takes input from the previous stage and yields output for the next. A pass can contain more than one phase."],
 [("Analysis phase", "The front end: reads the source and checks it, producing an intermediate representation and a symbol table."),
  ("Synthesis phase", "The back end: generates the target program from the intermediate representation and the symbol table."),
  ("Front end", "Machine independent analysis of the source language."),
  ("Back end", "Target dependent generation and optimization."),
  ("Pass", "A traversal of the compiler through the entire program."),
  ("Phase", "A distinguishable stage that takes input from the previous stage and produces output for the next.")],
 ["Front end = analysis; back end = synthesis.",
  "The front end depends on the source language, the back end on the target machine.",
  "The intermediate representation and symbol table link the two parts.",
  "A pass traverses the whole program; a phase is one stage.",
  "A pass may contain several phases."],
 [T("A compiler can broadly be divided into two parts, based on the way they compile: the analysis phase and the synthesis phase."),
  T("The analysis phase is known as the front end. It reads the source program, divides it into core parts, and then checks for lexical, grammar and syntax errors. It generates an intermediate representation of the source program and a symbol table, which are fed to the synthesis phase as input."),
  T("The synthesis phase is known as the back end. It generates the target program with the help of the intermediate representation and the symbol table."),
  T("This split is the reason one compiler family can support many languages and many machines. A new language needs a new front end. A new machine needs a new back end. The intermediate representation is the meeting point, and the symbol table travels with it."),
  T("A compiler can have many phases and passes. A pass refers to the traversal of a compiler through the entire program. A phase is a distinguishable stage which takes input from the previous stage, processes it and yields output that can be used as input for the next stage. A pass can have more than one phase."),
  T("For example, a one-pass compiler might do lexing, parsing and code generation together while reading the file once. A multi-pass compiler builds a tree in the first pass and optimizes it in later passes.")],
 [("Which part checks syntax errors?", ["Synthesis phase", "Analysis phase", "Loader", "Linker"], 1, "The analysis phase is the front end."),
  ("What does the synthesis phase receive?", ["Only source text", "Intermediate representation and symbol table", "Machine code", "Nothing"], 1, "It builds the target program from them."),
  ("What is a pass?", ["A traversal of the entire program", "One token", "A grammar rule", "A register"], 0, "A pass can contain several phases."),
  ("A new target machine needs changes to which part?", ["Front end", "Back end", "Preprocessor", "Source programs"], 1, "Code generation depends on the target.")],
 [("Another name for the analysis phase?", "The front end."), ("What does the front end output?", "An intermediate representation and a symbol table."),
  ("Phase vs pass?", "A pass is a traversal; a phase is a stage, and a pass can hold several.")],
 [MATCH("Front or back", "Match each activity with its part.", [("Check for syntax errors", "Analysis phase"), ("Generate target code", "Synthesis phase"), ("Build the symbol table", "Analysis phase"), ("Choose machine instructions", "Synthesis phase")]),
  PL("Front or back", "Write end_of(task). Return \"front\" for the tasks \"lexing\", \"parsing\" and \"type checking\", and \"back\" for \"register allocation\", \"instruction selection\" and \"code generation\". Anything else returns \"unknown\".",
     "end_of(task)", """
def end_of(task):
    if task in ['lexing', 'parsing', 'type checking']:
        return 'front'
    if task in ['register allocation', 'instruction selection', 'code generation']:
        return 'back'
    return 'unknown'
""", [["lexing"], ["parsing"], ["register allocation"], ["code generation"], ["drawing"]], "Two lists and membership tests."),
  PL("Counting passes", "A compiler runs a list of phases, and a pass ends where you see the word \"PASS_END\". Write count_passes(stages): the number of passes, counting a final group of phases without a PASS_END as a pass too. An empty list has 0 passes.",
     "count_passes(stages)", """
def count_passes(stages):
    n = 0
    open_pass = False
    for s in stages:
        if s == 'PASS_END':
            n += 1
            open_pass = False
        else:
            open_pass = True
    if open_pass:
        n += 1
    return n
""", [[["lex", "parse", "PASS_END", "optimize", "gen", "PASS_END"]], [["lex", "parse", "gen"]], [[]], [["lex", "PASS_END", "gen"]]], "Count each PASS_END; add one if phases are still waiting at the end."),
  FILL("Architecture", "The {{front}} end is the analysis phase and the {{back}} end is the synthesis phase. A {{pass}} traverses the entire program.")]))

# ------------------------------------------------------------ 3
CHS.append(CH(
 "Phases of a compiler",
 ("Six phases and a table", [
  "Lexical analysis | produces | Tokens",
  "Syntax analysis [ch7] | produces | Parse tree",
  "Semantic analysis [ch12] | produces | Annotated syntax tree",
  "Intermediate code generation [ch15] | produces | Intermediate code",
  "Code optimization [ch17] | improves | Intermediate code",
  "Code generation [ch16] | produces | Target machine code",
  "Symbol table [ch14] | is used by | Every phase"]),
 ["Compilation is a sequence of phases. Each takes input from the previous phase, has its own representation of the program and feeds the next. The phases are lexical analysis, syntax analysis, semantic analysis, intermediate code generation, code optimization and code generation.",
  "The lexical analyzer turns characters into tokens. The parser turns tokens into a parse tree. The semantic analyzer checks the rules of the language. The code generators then produce, improve and finally map code to the target machine.",
  "The symbol table is a data structure maintained through all phases. It stores identifier names with their types and supports scope management."],
 [("Lexeme", "A sequence of characters in the source that matches the pattern of a token."),
  ("Token", "A pair of token name and attribute value, produced by the lexical analyzer."),
  ("Parse tree", "A tree showing how the tokens match the grammar."),
  ("Annotated syntax tree", "The syntax tree with semantic information attached, output of semantic analysis."),
  ("Intermediate code", "A program for an abstract machine, between the source language and machine language."),
  ("Symbol table", "A data structure holding identifiers and their types, used by all phases.")],
 ["Phases: lexical, syntax, semantic, intermediate code, optimization, code generation.",
  "A token is <token-name, attribute-value>.",
  "The parser checks that the token arrangement fits the grammar.",
  "The semantic analyzer checks types and declarations.",
  "Intermediate code is machine independent, so optimization can be shared.",
  "The symbol table is used throughout."],
 [T("The compilation process is a sequence of phases. Each phase takes input from its previous stage, has its own representation of the source program, and feeds its output to the next phase of the compiler."),
  T("Lexical analysis is the first phase. The scanner works as a text scanner: it reads the source code as a stream of characters and converts it into meaningful lexemes. The analyzer represents these lexemes as tokens of the form token-name and attribute-value."),
  T("Syntax analysis, or parsing, comes next. It takes the tokens produced by lexical analysis and generates a parse tree, also called a syntax tree. The token arrangements are checked against the grammar of the language: the parser checks whether the expression made by the tokens is syntactically correct."),
  T("Semantic analysis checks whether the parse tree follows the rules of the language. For example, assignment between compatible data types, and adding a string to an integer. It also keeps track of identifiers, their types and expressions, and whether identifiers are declared before use. It produces an annotated syntax tree."),
  T("After semantic analysis the compiler generates intermediate code for an abstract machine. It sits between the high-level language and the machine language. It should be generated so that it is easy to translate into the target machine code."),
  T("Code optimization removes unnecessary code lines and arranges the sequence of statements to speed up execution without wasting resources such as CPU and memory."),
  T("In code generation, the generator takes the optimized intermediate code and maps it to the target machine language. It produces a sequence of, generally, relocatable machine code that performs the same task as the intermediate code."),
  T("The symbol table is a data structure maintained throughout all the phases. All the identifiers' names and their types are stored in it. It makes it easy for the compiler to search for an identifier record and retrieve it quickly, and it is also used for scope management."),
  T("Here is one statement through the first phases. The text x = a + 2 becomes the tokens id, equals, id, plus and number. The parser groups them into an assignment with a sum. The semantic analyzer checks that x and a are declared and compatible. The later chapters implement each phase in turn.")],
 [("What does the lexical analyzer output?", ["A parse tree", "Tokens", "Machine code", "A symbol table only"], 1, "Tokens are pairs of name and attribute."),
  ("Which phase checks that identifiers are declared before use?", ["Lexical", "Semantic", "Code generation", "Loading"], 1, "That needs the symbol table and types."),
  ("What is intermediate code?", ["Code for an abstract machine between source and target", "Assembly only", "A comment", "A token"], 0, "It makes retargeting easier."),
  ("Which structure is used by all phases?", ["Parse tree", "Symbol table", "Linker", "Token stream"], 1, "It stores identifiers and types.")],
 [("First phase?", "Lexical analysis."), ("What does the parser check?", "That the token arrangement matches the grammar."),
  ("What does optimization do?", "Removes unnecessary code and reorders statements to run faster with fewer resources."),
  ("Output of semantic analysis?", "An annotated syntax tree.")],
 [ORDER("Phases in order", "Put the compiler phases in order.", ["Lexical analysis", "Syntax analysis", "Semantic analysis", "Intermediate code generation", "Code optimization", "Code generation"]),
  MATCH("Phase and output", "Match each phase with its output.", [("Lexical analysis", "Tokens"), ("Syntax analysis", "Parse tree"), ("Semantic analysis", "Annotated syntax tree"), ("Code generation", "Target machine code")]),
  PL("Name the token kinds", "Write kinds(words). For each word return its kind: \"keyword\" for int, float, if, while, return; \"number\" if all characters are digits; \"identifier\" if it starts with a letter or underscore and has letters, digits or underscores; otherwise \"symbol\". This is a first, simple lexer; the next chapter does it properly.",
     "kinds(words)", """
def kinds(words):
    out = []
    for w in words:
        if w in ['int', 'float', 'if', 'while', 'return']:
            out.append('keyword')
        elif w.isdigit():
            out.append('number')
        elif (w[0].isalpha() or w[0] == '_') and all(c.isalpha() or c.isdigit() or c == '_' for c in w):
            out.append('identifier')
        else:
            out.append('symbol')
    return out
""", [[["int", "value", "=", "100", ";"]], [["while", "x1", "<", "_y", "2b"]], [[]]], "Check keywords first, then digits, then the identifier rule."),
  FILL("Phases", "The {{lexical}} analyzer produces tokens, the {{semantic}} analyzer checks types, and the {{symbol}} table is used by every phase.")]))

# ------------------------------------------------------------ 4
CHS.append(CH(
 "Lexical analysis",
 ("Lexical analysis", [
  "Lexical analyzer | reads | Character stream",
  "Lexical analyzer | removes | Whitespace and comments",
  "Lexeme | matches | Pattern",
  "Pattern | is written as | Regular expression [ch5]",
  "Token | is | Name and attribute",
  "Longest match rule | resolves | Ambiguous scanning",
  "Keyword | has priority over | Identifier"]),
 ["Lexical analysis is the first phase. It takes the preprocessed source, removes whitespace and comments, and breaks it into tokens. An invalid token is a lexical error. It works closely with the syntax analyzer, which asks for tokens when it needs them.",
  "A lexeme is the matched text. A pattern, written as a regular expression, says which lexemes make a valid token. Keywords, constants, identifiers, strings, numbers, operators and punctuation are all tokens.",
  "An alphabet is a finite set of symbols, a string a finite sequence of them, and a language a set of strings. When scanning is ambiguous the longest match wins, and reserved words beat identifiers."],
 [("Lexeme", "The actual characters matched in the source, such as value."),
  ("Pattern", "A rule describing what lexemes belong to a token, given by a regular expression."),
  ("Token", "A category of lexeme such as identifier or keyword, with an optional attribute."),
  ("Alphabet", "Any finite set of symbols."),
  ("String", "A finite sequence of symbols from an alphabet. The empty string is written epsilon."),
  ("Language", "A set of strings over an alphabet."),
  ("Longest match rule", "The scanner takes the longest lexeme that matches any token pattern."),
  ("Rule priority", "When two patterns match the same lexeme, the earlier or reserved one wins, so keywords beat identifiers.")],
 ["The lexer removes whitespace and comments and reports invalid tokens.",
  "int value = 100; has the tokens int, value, =, 100 and ;.",
  "Patterns are regular expressions; lexemes are the matched text.",
  "Longest match: intvalue is one identifier, not int followed by value.",
  "Keywords have priority over identifiers.",
  "The length of a string is its number of symbols; the empty string has length zero."],
 [T("Lexical analysis is the first phase of a compiler. It takes the modified source code from the language preprocessors, written as sentences. The lexical analyzer breaks these into a series of tokens, removing any whitespace or comments."),
  T("If the lexical analyzer finds a token invalid, it generates an error. It works closely with the syntax analyzer. It reads character streams from the source code, checks for legal tokens, and passes the data to the syntax analyzer when it demands."),
  T("A lexeme is a sequence of characters, alphanumeric, in a token. There are predefined rules for every lexeme to be identified as a valid token. These rules are defined by grammar rules, by means of a pattern. A pattern explains what can be a token, and patterns are defined by means of regular expressions."),
  T("In programming languages, keywords, constants, identifiers, strings, numbers, operators and punctuation symbols can be considered tokens. For example in C, the declaration int value = 100; contains the tokens int, a keyword; value, an identifier; the equals sign, an operator; 100, a constant; and the semicolon, a symbol."),
  T("Now the language-theory terms. An alphabet is any finite set of symbols. Binary has 0 and 1. Hexadecimal has the digits and the letters A to F. A string is any finite sequence of symbols. Its length is the number of symbols, so the length of tutorialspoint is 14. A string of zero length is the empty string, written with the Greek letter epsilon."),
  T("A typical high-level language has these symbol groups. Arithmetic symbols: plus, minus, modulo, multiplication, division. Punctuation: comma, semicolon, dot, arrow. Assignment is the equals sign, and special assignments are plus-equals and its relatives. Comparison operators are double equals, not equals, less than and so on. There are logical operators, shift operators, the preprocessor hash and the location specifier ampersand."),
  T("A language is a finite set of strings over some finite alphabet. Computer languages are treated as sets, so set operations such as union and concatenation can be applied. Finite languages can be described by regular expressions."),
  T("Now the longest match rule. The lexical analyzer scans the code letter by letter, and when it meets a whitespace, an operator symbol or a special symbol, it decides that a word is complete."),
  T("Take int intvalue; While reading the characters of the second word, up to int, the analyzer cannot know whether it has the keyword int or the start of the identifier intvalue. The longest match rule says: choose the longest lexeme that matches any token. Here that is intvalue, an identifier."),
  T("The analyzer also follows rule priority. A reserved word of the language has priority over user input. If the lexeme int is exactly a keyword, it becomes a keyword token, so a programmer cannot use it as a variable name. The tutorial words this as the analyzer generating an error. In practice, the scanner emits the keyword token, and the parser or semantic analysis rejects the misuse as an identifier."),
  T("In the practice section you write a real tokenizer. It applies the longest match rule, gives keywords priority, skips whitespace, and handles two-character operators like double equals.")],
 [("What does the lexical analyzer remove?", ["Tokens", "Whitespace and comments", "Identifiers", "Operators"], 1, "They have no meaning for the parser."),
  ("What is a pattern?", ["A rule, usually a regular expression, describing a token's lexemes", "A parse tree", "A register", "A memory page"], 0, "Lexemes are matched against patterns."),
  ("How is intvalue scanned?", ["As keyword int then value", "As one identifier by the longest match rule", "As an error", "As a number"], 1, "The longest lexeme wins."),
  ("What is the length of the empty string?", ["1", "0", "Undefined", "Epsilon"], 1, "It contains no symbols.")],
 [("Lexeme vs token?", "A lexeme is the matched text; a token is its category with an attribute."),
  ("What has priority, keyword or identifier?", "Keyword."), ("What is epsilon?", "The empty string."),
  ("How are patterns written?", "As regular expressions.")],
 [MATCH("Lexical terms", "Match each term to its meaning.", [("Lexeme", "The matched characters"), ("Pattern", "A rule for what a token can be"), ("Alphabet", "A finite set of symbols"), ("Epsilon", "The empty string")]),
  PL("A tokenizer", "Write tokenize(src). Split the source text into tokens, skipping whitespace. Return a list of [kind, lexeme]. Kinds: \"KEYWORD\" for int, float, if, else, while, return; \"ID\" for a letter or underscore followed by letters, digits or underscores (take the longest match, then check for a keyword); \"NUM\" for digits; \"OP\" for == != <= >= and the single characters + - * / = < > !; \"PUNCT\" for ; , ( ) { }. A character that fits nothing gives [\"ERROR\", char].",
     "tokenize(src)", """
def tokenize(src):
    keywords = ['int', 'float', 'if', 'else', 'while', 'return']
    two = ['==', '!=', '<=', '>=']
    one = '+-*/=<>!'
    punct = ';,(){}'
    out = []
    i = 0
    n = len(src)
    while i < n:
        c = src[i]
        if c.isspace():
            i += 1
        elif c.isalpha() or c == '_':
            j = i
            while j < n and (src[j].isalpha() or src[j].isdigit() or src[j] == '_'):
                j += 1
            word = src[i:j]
            out.append(['KEYWORD' if word in keywords else 'ID', word])
            i = j
        elif c.isdigit():
            j = i
            while j < n and src[j].isdigit():
                j += 1
            out.append(['NUM', src[i:j]])
            i = j
        elif src[i:i + 2] in two:
            out.append(['OP', src[i:i + 2]])
            i += 2
        elif c in one:
            out.append(['OP', c])
            i += 1
        elif c in punct:
            out.append(['PUNCT', c])
            i += 1
        else:
            out.append(['ERROR', c])
            i += 1
    return out
""", [["int value = 100;"], ["int intvalue;"], ["if (a>=b) x=1;"], ["x == 10 # y"], [""]],
     "Loop with an index i. Look at the character: letter, digit, two-character operator, one-character operator or punctuation. For words take the longest run of letters and digits, then test the keyword list."),
  PL("Language operations", "Write concat(L, M): the concatenation of two languages, given as lists of strings. Return a sorted list with no duplicates of every s+t with s in L and t in M.",
     "concat(L, M)", """
def concat(L, M):
    out = []
    for s in L:
        for t in M:
            w = s + t
            if w not in out:
                out.append(w)
    out.sort()
    return out
""", [[["a", "b"], ["0", "1"]], [["", "x"], ["", "y"]], [["ab"], []]], "Two nested loops, skipping duplicates, then sort."),
  FILL("Scanning", "The scanner takes the {{longest}} match, so intvalue is one {{identifier}}. A reserved word such as int is a {{keyword}}.")]))

# ------------------------------------------------------------ 5
CHS.append(CH(
 "Regular expressions",
 ("Regular expressions", [
  "Regular expression | specifies | Token pattern",
  "Regular expression | denotes | Regular language",
  "Union | is written | r | s",
  "Concatenation | is written | rs",
  "Kleene closure | is written | r*",
  "Star | has | Highest precedence",
  "Union | has | Lowest precedence",
  "Finite automata [ch6] | recognize | Regular expressions"]),
 ["The lexical analyzer must recognize a finite set of valid lexemes of the language. Regular expressions define patterns for strings of symbols. The grammar they define is a regular grammar and the language is a regular language.",
  "Operations on languages are union, concatenation and Kleene closure. A regular expression built with them denotes a language. The star has the highest precedence, then concatenation, and union has the lowest. All are left associative.",
  "Shorthands such as plus, question mark and character ranges are common. Tokens like identifiers and decimal numbers are written with them: letter followed by letters or digits, and an optional sign followed by one or more digits."],
 [("Regular expression", "A notation for patterns; each denotes a set of strings."),
  ("Union", "L union M is the set of strings in L or in M."),
  ("Concatenation", "LM is the set of strings st with s in L and t in M."),
  ("Kleene closure", "L star is zero or more occurrences of strings from L."),
  ("Regular language", "A language defined by a regular expression."),
  ("Plus", "x plus means one or more occurrences of x."),
  ("Question mark", "x question mark means zero or one occurrence of x.")],
 ["Operations: union, concatenation, Kleene closure.",
  "Precedence: star, then concatenation, then union.",
  "x* is zero or more; x+ is one or more; x? is zero or one.",
  "Identifier = letter (letter | digit)*.",
  "Decimal = (sign)? (digit)+.",
  "Finite automata verify the expressions."],
 [T("The lexical analyzer needs to scan and identify only a finite set of valid strings, tokens or lexemes that belong to the language in hand. It searches for the pattern defined by the language rules."),
  T("Regular expressions can express finite languages by defining a pattern for finite strings of symbols. The grammar defined by regular expressions is known as regular grammar. The language defined by a regular grammar is known as a regular language."),
  T("Regular expression is an important notation for specifying patterns. Each pattern matches a set of strings, so regular expressions serve as names for sets of strings. Programming language tokens can be described by regular languages. Their definition is recursive, they are easy to understand, and they have an efficient implementation."),
  T("There are algebraic laws that regular expressions obey, which can be used to turn them into equivalent forms."),
  T("The operations on languages are as follows. The union of two languages L and M is the set of strings in L or in M. The concatenation LM is the set of strings st where s is in L and t is in M. The Kleene closure of L is zero or more occurrences of strings from L."),
  M(r"L \cup M = \{\, s \mid s \in L \text{ or } s \in M \,\} \qquad LM = \{\, st \mid s \in L,\ t \in M \,\} \qquad L^{*} = \bigcup_{i \ge 0} L^{i}"),
  T("Notation: if r and s are regular expressions denoting the languages L of r and L of s, then r or s is a regular expression for the union, r followed by s denotes the concatenation, r star denotes the closure, and a parenthesized r denotes the same language as r."),
  T("Precedence and associativity. The star, concatenation and the pipe are left associative. The star has the highest precedence, concatenation the second highest, and the pipe the lowest. So ab|c* means a followed by b, or any number of c."),
  T("Common shorthands. x star generates epsilon, x, xx, xxx and so on. x plus means one or more, the same as x followed by x star. x question mark means at most one. The range a to z is all lower-case English letters, A to Z the upper-case ones, and 0 to 9 the digits."),
  T("Now some tokens. Let letter be a to z or A to Z, digit be 0 to 9, and sign be plus or minus. A decimal integer is an optional sign followed by one or more digits. An identifier is a letter followed by any number of letters or digits."),
  T("The one problem left is how to verify the validity of a regular expression used to specify patterns. The well-accepted solution is finite automata, the next chapter. In the practice section you test these two token patterns by hand and list a Kleene closure.")],
 [("What is the highest-precedence regular expression operator?", ["Union", "Concatenation", "Kleene star", "None"], 2, "Star binds tightest, union loosest."),
  ("What does x+ mean?", ["Zero or more x", "One or more x", "At most one x", "Exactly two x"], 1, "It equals x followed by x star."),
  ("Which pattern describes an identifier?", ["digit+", "letter (letter | digit)*", "sign? digit", "(letter | digit)"], 1, "It starts with a letter."),
  ("What do regular expressions define?", ["Context-free languages", "Regular languages", "All languages", "Binary files"], 1, "These are the token languages.")],
 [("x? means what?", "Zero or one occurrence of x."), ("Decimal pattern?", "(sign)? (digit)+"), ("Identifier pattern?", "letter (letter | digit)*"),
  ("What verifies a regular expression?", "A finite automaton.")],
 [MATCH("Notation", "Match each expression with its meaning.", [("x*", "Zero or more x"), ("x+", "One or more x"), ("x?", "Zero or one x"), ("[0-9]", "Any digit"), ("a|b", "a or b")]),
  PL("Is it an identifier?", "Write is_identifier(s) for the pattern letter (letter | digit)*. Letters are a-z and A-Z. Return true or false. Note the empty string is not an identifier.",
     "is_identifier(s)", """
def is_identifier(s):
    if s == '':
        return False
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if s[0] not in letters:
        return False
    for c in s[1:]:
        if c not in letters and c not in '0123456789':
            return False
    return True
""", [["value"], ["x1"], ["1x"], [""], ["a_b"], ["Z"]], "The first character must be a letter; the rest letters or digits."),
  PL("Is it a decimal?", "Write is_decimal(s) for the pattern (sign)? (digit)+, where sign is + or -. Return true or false.",
     "is_decimal(s)", """
def is_decimal(s):
    if s[:1] in ['+', '-']:
        s = s[1:]
    if s == '':
        return False
    for c in s:
        if c not in '0123456789':
            return False
    return True
""", [["100"], ["-42"], ["+"], ["4.5"], [""], ["+7"]], "Drop one optional sign, then require at least one digit and only digits."),
  PL("Kleene closure", "Write star(alphabet, max_len): every string over the alphabet (a list of one-character strings) of length 0 up to max_len, including the empty string. Return them sorted by length, then alphabetically.",
     "star(alphabet, max_len)", """
def star(alphabet, max_len):
    out = ['']
    layer = ['']
    for _ in range(max_len):
        nxt = []
        for w in layer:
            for a in sorted(alphabet):
                nxt.append(w + a)
        out = out + nxt
        layer = nxt
    return out
""", [[["a", "b"], 2], [["x"], 3], [["0", "1"], 0]], "Build length 1 from length 0 by appending each symbol, and so on."),
  FILL("Regular expressions", "The Kleene {{closure}} means zero or more. The operator with the lowest precedence is {{union}}. An optional sign is written {{sign}}?.")]))

# ------------------------------------------------------------ 6
CHS.append(CH(
 "Finite automata",
 ("Finite automata", [
  "Finite automaton | recognizes | Regular expressions",
  "Finite automaton | has | States, alphabet, start state, final states, transition function",
  "Transition function | maps | State and symbol to state",
  "Final state | means | Input accepted",
  "Lexical analyzer [ch4] | is built from | Finite automata",
  "Longest match rule [ch4] | is implemented by | Running past accepting states"]),
 ["A finite automaton is a state machine that takes a string of symbols and changes state for each symbol. It is a recognizer for regular expressions. If the whole input is processed and the automaton is in a final state, the string is accepted as a valid token.",
  "It consists of a finite set of states, a finite input alphabet, one start state, a set of final states and a transition function that maps a state and a symbol to a state.",
  "A lexer built on automata implements the longest match rule by running as far as it can and remembering the last point at which it was in a final state."],
 [("Finite automaton", "A state machine with states, an alphabet, a start state, final states and a transition function."),
  ("State", "A circle in the diagram; the machine is in exactly one state at a time."),
  ("Start state", "The state where the machine begins, marked with an arrow."),
  ("Final state", "A state where the input is accepted; drawn with a double circle."),
  ("Transition", "A move from one state to another on an input symbol; it may stay in the same state."),
  ("Transition function", "The mapping delta from a state and a symbol to the next state.")],
 ["The model: Q, the alphabet, q0, the final states and delta.",
  "delta maps Q times the alphabet to Q.",
  "Accept the input if it is consumed and the state is final.",
  "Transitions can loop back to the same state.",
  "The automaton for three binary digits ending in 1 has four steps.",
  "Longest match: keep going, remember the last accepting position."],
 [T("A finite automaton is a state machine that takes a string of symbols as input and changes its state accordingly. It is a recognizer for regular expressions. When a string is fed to it, it changes state for each symbol. If the input is successfully processed and the automaton reaches a final state, the string is accepted, meaning it is a valid token of the language in hand."),
  T("The mathematical model has five parts. A finite set of states, Q. A finite set of input symbols, Sigma. One start state, q0. A set of final states. And a transition function, delta, which maps states and symbols to states."),
  M(r"\delta : Q \times \Sigma \rightarrow Q"),
  T("Construction. States are circles with the name inside. The start state has an arrow pointing to it. A final state is drawn as a double circle. A transition is a directed arrow, taken when the desired symbol appears in the input. The automaton can move to the next state or stay in the same state, drawn as an arrow from a state to itself."),
  T("A note about one claim in the tutorial. It says a final state has an odd number of incoming arrows and an even number of outgoing arrows, with odd one greater than even. That is not a rule of automata. A final state can have any number of arrows in and out. Do not rely on it."),
  T("Example. Take an automaton that accepts any three-digit binary value ending in the digit 1. It needs a state for each number of digits read. After the third digit it accepts only if that digit was 1, and a fourth digit is not allowed. A dead state, which can never reach acceptance, is how a complete table rejects."),
  C("""state  on 0   on 1
q0     q1     q1
q1     q2     q2
q2     x      q3     # third digit: only a 1 reaches the accepting state
q3     x      x      # accepting, but a fourth digit is not allowed
x      x      x      # dead state: everything is rejected from here""", "text"),
  T("States q0, q1 and q2 count the digits read so far, q3 means three digits read ending in 1, and x is a dead state that absorbs everything else. The practice section gives you this machine as data, and you write the runner."),
  T("Now the longest match rule again. A lexer built from automata runs the automaton as long as it can make a transition. Each time it is in a final state it remembers the position. When the machine gets stuck, the lexer returns the lexeme up to the last remembered final position and restarts from there."),
  T("Rule priority fits the same picture. If two token automata both accept the same lexeme, the one listed first, for example the keyword, wins. In the practice section you write the runner, then the longest accepted prefix.")],
 [("What does a finite automaton recognize?", ["Programs", "Regular languages", "Any language", "Only keywords"], 1, "It is the recognizer for regular expressions."),
  ("When is a string accepted?", ["When input is consumed and the state is final", "When it is short", "When the start state is final only", "Never"], 0, "Both conditions are needed."),
  ("What does the transition function map?", ["Tokens to trees", "State and symbol to the next state", "Strings to numbers", "Lexemes to files"], 1, "It maps Q times Sigma to Q."),
  ("How does a lexer apply the longest match rule?", ["Stops at the first final state", "Remembers the last final state and continues", "Ignores final states", "Reads backwards"], 1, "It runs until stuck, then returns the last accepted prefix.")],
 [("Five parts of a finite automaton?", "States, alphabet, start state, final states and the transition function."), ("How are final states drawn?", "With a double circle."),
  ("What if the machine gets stuck?", "The string is rejected, or the lexer falls back to the last accepted prefix."), ("Rule priority?", "The earlier or reserved pattern wins on a tie.")],
 [MATCH("Automaton parts", "Match each part with its role.", [("Start state", "Where the machine begins"), ("Final state", "Accepting state"), ("Transition function", "Maps state and symbol to the next state"), ("Alphabet", "The finite set of input symbols")]),
  PL("Run a DFA", "A machine is given as {\"start\": state, \"final\": [states], \"delta\": {state: {symbol: state}}}. Write run_dfa(m, s): follow the transitions over the string s and return true if you end in a final state. If a transition is missing, return false.",
     "run_dfa(m, s)", """
def run_dfa(m, s):
    state = m['start']
    for c in s:
        row = m['delta'].get(state)
        if row is None or c not in row:
            return False
        state = row[c]
    return state in m['final']
""", [[{"start": "q0", "final": ["q3"], "delta": {"q0": {"0": "q1", "1": "q1"}, "q1": {"0": "q2", "1": "q2"}, "q2": {"0": "x", "1": "q3"}, "q3": {"0": "x", "1": "x"}, "x": {"0": "x", "1": "x"}}}, s] for s in ["101", "100", "11", "1111", "001", "011", ""]],
     "Keep a current state. For each symbol look up delta[state][symbol]. At the end test membership in the final list."),
  PL("Longest accepted prefix", "Same machine format. Write longest_prefix(m, s): the length of the longest prefix of s that the machine accepts, or -1 if no prefix (not even the empty one) is accepted. This is the longest match rule.",
     "longest_prefix(m, s)", """
def longest_prefix(m, s):
    state = m['start']
    best = 0 if state in m['final'] else -1
    for i in range(len(s)):
        row = m['delta'].get(state)
        if row is None or s[i] not in row:
            break
        state = row[s[i]]
        if state in m['final']:
            best = i + 1
    return best
""", [[{"start": "s", "final": ["id"], "delta": {"s": {"a": "id", "b": "id", "1": "e"}, "id": {"a": "id", "b": "id", "1": "id"}, "e": {}}}, s] for s in ["ab1+", "1ab", "a", "+"]],
     "Record the index after each step where the state is final; stop when no transition exists."),
  PL("Count transitions", "Write count_transitions(m): the number of transitions defined in the machine's delta table (the sum over states of the symbols defined).",
     "count_transitions(m)", """
def count_transitions(m):
    n = 0
    for state in m['delta']:
        n += len(m['delta'][state])
    return n
""", [[{"start": "q0", "final": ["q1"], "delta": {"q0": {"a": "q1", "b": "q0"}, "q1": {"a": "q1"}}}], [{"start": "q", "final": [], "delta": {}}]], "Add the length of each row."),
  FILL("Automata", "A finite automaton accepts when the input is consumed and the state is {{final}}. The function delta is the {{transition}} function. A final state is drawn as a {{double}} circle.")]))
