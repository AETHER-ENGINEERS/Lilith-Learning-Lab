"""Compiler Design course, chapters 13-17."""
from clib import *

CHS = []

# ------------------------------------------------------------ 13
CHS.append(CH(
 "Runtime environment",
 ("Runtime environment", [
  "Procedure activation | has | Activation record",
  "Activation record | lives on | Control stack",
  "Activations | form | Activation tree",
  "Code | uses | Static allocation",
  "Procedure calls | use | Stack allocation",
  "Dynamic variables | use | Heap allocation",
  "Parameter passing | has modes | Value, reference, copy-restore, name"]),
 ["A program needs memory and a mapping from names to locations at run time. The runtime environment is the state of the target machine, and the runtime support system handles memory allocation and de-allocation while the program runs.",
  "Each procedure execution is an activation with an activation record on the control stack, holding temporaries, local data, machine status, links, parameters and the return value. The sequence of activations forms an activation tree. Code is allocated statically, procedure activations on a stack and dynamic data on a heap.",
  "Parameters are passed by value, by reference, by copy-restore or by name. They differ in whether the callee can change the caller's variable and when."],
 [("Runtime environment", "The state of the target machine while the program runs: libraries, variables and memory."),
  ("Activation", "One execution of a procedure."),
  ("Activation record", "The data needed for one call: temporaries, locals, machine status, links, parameters, return value."),
  ("Control stack", "The stack on which activation records are kept."),
  ("Activation tree", "A tree showing how procedure calls nest."),
  ("r-value", "The value of an expression."),
  ("l-value", "The memory location where an expression's value is stored."),
  ("Formal parameter", "A variable in the definition of the called procedure."),
  ("Actual parameter", "A value or address passed in the call."),
  ("Pass by value", "The r-value is copied; changes inside do not affect the caller."),
  ("Pass by reference", "The l-value is passed; the callee works on the caller's variable."),
  ("Pass by copy-restore", "Values are copied in, and copied back to the caller's variables when the procedure ends."),
  ("Pass by name", "The argument expression is substituted textually into the body.")],
 ["Activation records live on the control stack.",
  "The call order gives a depth-first activation tree.",
  "Static: code, global data. Stack: procedure calls. Heap: dynamic data.",
  "Stack and heap sit at opposite ends of memory and grow toward each other.",
  "r-value is a value; l-value is a location. 7 = x + y is an l-value error.",
  "Value does not change the caller; reference does; copy-restore does at the end; name substitutes text."],
 [T("A program as source code is merely a collection of text. To make it alive, it requires actions performed on the target machine, and it needs memory resources to execute instructions. Names of procedures and identifiers must be mapped to actual memory locations at run time."),
  T("By runtime we mean a program in execution. The runtime environment is a state of the target machine, which may include software libraries, environment variables and so on, to provide services to the processes running in the system. The runtime support system is a package, mostly generated with the executable itself, that handles communication between the process and the runtime environment. It takes care of memory allocation and de-allocation while the program is executing."),
  T("A program is a sequence of instructions combined into procedures. Instructions in a procedure execute sequentially. The execution of a procedure is called its activation. An activation record contains all the information needed to call a procedure. Depending on the language it may contain these units."),
  C("""Temporaries         intermediate values of expressions
Local data          locals of the called procedure
Machine status      registers, program counter before the call
Control link        address of the caller's activation record
Access link         data outside the local scope
Actual parameters   inputs sent to the called procedure
Return value        value returned to the caller""", "text"),
  T("Whenever a procedure is executed, its activation record is stored on the stack, also known as the control stack. When a procedure calls another, the caller's execution is suspended until the called procedure finishes, and the called procedure's record is pushed on the stack."),
  T("When control flows sequentially, with a call transferring control to the callee and the return giving it back, the series of activations can be drawn as a tree, the activation tree. In the tutorial's example, the main program prints a prompt, reads a name, calls show_data and prints a last message; show_data is a child of main in the tree. The tutorial's code uses two different names for the same parameter, user and username; take it as one variable."),
  T("Procedures are executed depth first, so stack allocation is the best suited storage for procedure activations."),
  T("The runtime environment manages memory for these entities. Code is the text part of the program, which does not change at run time, and its memory requirement is known at compile time. Procedures have static text but are called in a random manner, so stack storage is used to manage their calls and activations. Variables are known only at run time unless they are global or constant, and a heap scheme manages their allocation and de-allocation."),
  T("In static allocation, compilation data is bound to a fixed location in memory and does not change while the program runs. As the memory requirement and locations are known in advance, no runtime support for allocation and de-allocation is needed."),
  T("Stack allocation manages procedure calls and activations. It works last in, first out, and it is very useful for recursive calls."),
  T("Heap allocation is used to dynamically allocate memory to variables whose lifetime is not tied to a call, and claim it back when they are no longer required. Except for statically allocated memory, both stack and heap can grow and shrink dynamically and unexpectedly, so they cannot be given a fixed amount of memory. The text part has a fixed area. Stack and heap are placed at the two extremes of the program's memory and grow toward each other."),
  T("Now parameter passing: the communication medium among procedures. First some terms. The value of an expression is its r-value. A single variable on the right of an assignment also gives an r-value. The location where an expression is stored is its l-value, which always appears on the left of an assignment. In day = 1 and week = day * 7, the constants and the variables have r-values; only variables have l-values. The statement 7 = x + y is an l-value error, because the constant 7 has no memory location."),
  T("Formal parameters are the variables in the definition of the called function that take the information passed by the caller. Actual parameters are the values or addresses given in the call. What the formal parameter holds depends on the technique, a value or an address."),
  T("Pass by value: the caller passes the r-value of the actual parameters and the compiler places it in the callee's activation record. If the formal parameter is changed, the actual parameter is not affected."),
  T("Pass by reference: the l-value of the actual parameter is copied into the callee's activation record. The callee has the address of the actual parameter, so a change to the formal parameter is seen on the actual parameter."),
  T("Pass by copy-restore works like reference, except that the changes to the actual parameters are made only when the called procedure ends. On entry the values are copied in. Changes to the formal parameter have no immediate effect on the actual parameter, but when the procedure ends the formal's value is copied to the actual's location."),
  T("The tutorial's example: y is a global set to 10, and the procedure takes x, sets x to 99 and then sets y to 0. Under copy-restore, at the end x is copied back into y, so the caller prints 99. The practice section runs this example under each mode."),
  T("Pass by name, from languages like Algol, works like the C preprocessor. The argument expression is substituted textually for the formal parameter in the body of the procedure, so it works on the actual parameters much like pass by reference."),
  T("The practice section builds an activation tree from call and return events and runs the parameter modes.")],
 [("Where are activation records stored?", ["In the heap", "On the control stack", "In the symbol table", "In the object file"], 1, "Calls are last in, first out."),
  ("Which part of a program uses static allocation?", ["Dynamic variables", "Code", "Recursion", "Heap data"], 1, "Its size is known at compile time."),
  ("In pass by value, a change to the formal parameter...", ["Changes the actual", "Does not change the actual", "Crashes", "Changes only globals"], 1, "Only the r-value was copied."),
  ("Why is 7 = x + y an error?", ["7 is too small", "7 has no l-value", "x and y are undeclared", "Plus is not allowed"], 1, "A constant is not a memory location.")],
 [("What links activation records?", "The control link."), ("Why a stack for procedures?", "Calls nest depth first, so last in first out."),
  ("Copy-restore timing?", "Values are copied back when the procedure ends."), ("Which end do stack and heap start at?", "Opposite ends of the program's memory.")],
 [MATCH("Storage allocation", "Match each item with where it is stored.", [("Program code", "Static area"), ("Procedure activations", "Stack"), ("Dynamically allocated data", "Heap")]),
  MATCH("Parameter passing", "Match each mode with how it works.", [("Pass by value", "Copies the r-value"), ("Pass by reference", "Passes the l-value"), ("Copy-restore", "Copies back at the end"), ("Pass by name", "Textual substitution")]),
  PL("Activation tree", "Events are strings \"call NAME\" and \"return\". The first event is the call of the root. Write activation_tree(events): return the tree as [name, [children]] with the children in call order.",
     "activation_tree(events)", """
def activation_tree(events):
    stack = []
    root = None
    for e in events:
        if e == 'return':
            stack.pop()
        else:
            node = [e.split(' ', 1)[1], []]
            if stack:
                stack[-1][1].append(node)
            else:
                root = node
            stack.append(node)
    return root
""", [[["call main", "call read", "return", "call show", "call fmt", "return", "return", "return"]], [["call f", "call f", "call f", "return", "return", "return"]], [["call main", "return"]]], "Keep a stack of open nodes. A call creates a node under the top of the stack; a return pops."),
  PL("Stack depth", "Same events. Write max_depth(events): the largest number of activation records on the stack at one time.",
     "max_depth(events)", """
def max_depth(events):
    d = 0
    best = 0
    for e in events:
        if e == 'return':
            d -= 1
        else:
            d += 1
            if d > best:
                best = d
    return best
""", [[["call a", "call b", "return", "call c", "call d", "return", "return", "return"]], [["call f", "call f", "call f", "return", "return", "return"]], [[]]], "Count calls up and returns down; remember the peak."),
  PL("Same call, four modes", "A global y starts at 10. The procedure p(x) does: x = 99, then y = 0. The call is p(y). Write final_y(mode) for mode \"value\", \"reference\", \"copy-restore\" or \"name\": return the value of y after the call. By value, x is a separate copy. By reference and by name, x is the same variable as y. By copy-restore, x is a copy that is stored into y when p ends.",
     "final_y(mode)", """
def final_y(mode):
    y = 10
    if mode == 'value':
        x = y
        x = 99
        y = 0
        return y
    if mode == 'reference' or mode == 'name':
        y = 99
        y = 0
        return y
    x = y
    x = 99
    y = 0
    y = x
    return y
""", [["value"], ["reference"], ["copy-restore"], ["name"]], "Decide which assignments touch the same variable in each mode. Copy-restore writes x into y at the very end."),
  PL("Swap under each mode", "A procedure swap(a, b) does t = a, a = b, b = t. It is called as swap(p, q) with the variables p and q. Write swap_result(mode, p, q): return [p, q] after the call. By value nothing changes. By reference, copy-restore and name the caller's variables end up swapped.",
     "swap_result(mode, p, q)", """
def swap_result(mode, p, q):
    if mode == 'value':
        return [p, q]
    a, b = p, q
    t = a
    a = b
    b = t
    return [a, b]
""", [["value", 1, 2], ["reference", 1, 2], ["copy-restore", 3, 4], ["name", 5, 6]], "Only value leaves the caller's variables as they were."),
  FILL("Runtime", "Activation records are stored on the {{stack}}. A constant has an r-value but no {{l-value|lvalue|l value}}. With pass by {{reference}} the callee works on the caller's variable.")]))

# ------------------------------------------------------------ 14
CHS.append(CH(
 "Symbol table",
 ("Symbol table", [
  "Symbol table | stores | Names and attributes",
  "Symbol table | is used by | Analysis and synthesis",
  "Symbol table | is implemented as | List, search tree or hash table",
  "insert | adds | Name and attributes",
  "lookup | returns | Attributes or 0",
  "Scope | is handled by | Hierarchy of tables",
  "Lookup | searches | Current scope then parents"]),
 ["The symbol table stores information about names: variables, functions, objects, classes and interfaces. It is used by both the analysis and the synthesis parts of the compiler.",
  "It serves to store names in one place, to check that a variable is declared, to type check, and to resolve scope. It is a linear table or, most often, a hash table. Each entry holds the symbol name, type and attributes.",
  "The two operations are insert, used mostly by the analysis phase, and lookup, which returns 0 when the symbol is absent. For scope, tables are arranged in a hierarchy, and lookup searches the current scope first and then the parent scopes."],
 [("Symbol table", "A table of the names in a program with their types and attributes."),
  ("insert", "Adds a new name with its attributes to the table."),
  ("lookup", "Searches for a name; returns its attributes, or 0 if not present."),
  ("Scope", "The region of a program in which a name is visible."),
  ("Global symbol table", "The table accessible by all procedures."),
  ("Scope symbol table", "A table created for one scope.")],
 ["Entry format: symbol name, type, attribute.",
  "static int interest is stored as interest, int, static.",
  "Implementation choices: linear list, binary search tree, hash table. Hash tables are most common.",
  "insert is used mostly by the analysis phase.",
  "lookup checks existence, prior declaration, scope, initialization and duplicates.",
  "Scope lookup: current table first, then parents, up to the global table."],
 [T("The symbol table is an important data structure created and maintained by compilers to store information about the occurrence of various entities such as variable names, function names, objects, classes and interfaces. It is used by both the analysis and synthesis parts of the compiler."),
  T("Depending on the language, a symbol table may serve these purposes: to store the names of all entities in a structured form in one place; to verify that a variable has been declared; to implement type checking by verifying that assignments and expressions are semantically correct; and to determine the scope of a name, which is scope resolution."),
  T("A symbol table is simply a table, either linear or a hash table. It keeps an entry for each name in the format symbol name, type, attribute. For example the declaration static int interest should be stored as the entry interest, int, static. The attribute field holds the other facts about the name."),
  T("Implementation. If a compiler handles only a small amount of data, the table can be an unordered list, which is easy to code but suitable only for small tables. The alternatives are a sorted or unsorted linear list, a binary search tree, and a hash table. Most symbol tables are hash tables, where the symbol itself is the key of the hash function and the return value is the information about the symbol."),
  T("The insert operation is more frequently used by the analysis phase, the first half of the compiler, where tokens are identified and names are stored. It adds information about unique names occurring in the source code. The attributes of a symbol are the information associated with it, such as its value, state, scope and type. For int a, the compiler calls insert with a and int."),
  T("The lookup operation searches for a name to determine whether the symbol exists in the table, whether it is declared before it is used, whether the name is used in the scope, whether the symbol is initialized, and whether it is declared multiple times. The basic form is lookup of a symbol. It returns 0 if the symbol does not exist, and otherwise the attributes stored in the table."),
  T("Scope management. A compiler maintains two kinds of symbol tables: a global symbol table accessible by all procedures, and scope symbol tables created for each scope in the program. To determine the scope of a name, the tables are arranged in a hierarchy."),
  T("In the tutorial's example, a global variable value and two procedures pro_one and pro_two sit in the global table. Each procedure has its own table with its locals, and each inner block has a child table. Names in pro_one's table and its children are not available to pro_two."),
  C("""int value = 10;
void pro_one() {
    int one_1; int one_2;
    { int one_3; int one_4; }     /* inner scope 1 */
    int one_5;
    { int one_6; int one_7; }     /* inner scope 2 */
}""", "c"),
  T("The hierarchy is kept by the semantic analyzer. To find a name it searches in this order. First the current scope, the current symbol table. If the name is found, the search is finished; otherwise it goes to the parent table, until the name is found or the global table has been searched."),
  T("This is what the practice section builds: a scoped table driven by a list of operations. You will see shadowing, where an inner declaration hides an outer one, and the hash function that a real implementation uses.")],
 [("What does lookup return for a missing name?", ["An error", "0", "The global table", "The type int"], 1, "Per the tutorial's convention."),
  ("Which implementation is most common?", ["Unordered list", "Hash table", "Stack", "Queue"], 1, "The symbol is the key of the hash function."),
  ("How does scope lookup proceed?", ["Global table first", "Current scope, then parents", "Random order", "Only the current scope"], 1, "Until the global table is searched."),
  ("What does an entry hold?", ["Symbol name, type, attribute", "Only the name", "Machine code", "Tokens"], 0, "For example interest, int, static.")],
 [("What does insert add?", "A name with its attributes."), ("Who uses insert most?", "The analysis phase."), ("Why a hierarchy of tables?", "To resolve scope."),
  ("What is shadowing?", "An inner declaration hides an outer one of the same name.")],
 [MATCH("Symbol table facts", "Match each item.", [("insert", "Add a name and attributes"), ("lookup", "Find attributes, or 0"), ("Global table", "Visible to all procedures"), ("Scope table", "One per scope")]),
  PL("A scoped symbol table", "Operations are lists: [\"enter\"] opens a new scope; [\"exit\"] closes the innermost scope; [\"insert\", name, type] adds the name to the current scope; [\"lookup\", name] searches the current scope then its parents. Write symtab(ops) returning one result per operation: \"ok\" for enter and exit; for insert \"ok\", or \"duplicate\" if the name already exists in the current scope; for lookup the type string, or 0 if not found. The global scope exists from the start; an exit on it returns \"error\".",
     "symtab(ops)", """
def symtab(ops):
    scopes = [{}]
    out = []
    for op in ops:
        if op[0] == 'enter':
            scopes.append({})
            out.append('ok')
        elif op[0] == 'exit':
            if len(scopes) == 1:
                out.append('error')
            else:
                scopes.pop()
                out.append('ok')
        elif op[0] == 'insert':
            if op[1] in scopes[-1]:
                out.append('duplicate')
            else:
                scopes[-1][op[1]] = op[2]
                out.append('ok')
        else:
            found = 0
            for sc in reversed(scopes):
                if op[1] in sc:
                    found = sc[op[1]]
                    break
            out.append(found)
    return out
""", [[[["insert", "value", "int"], ["enter"], ["insert", "one_1", "int"], ["lookup", "value"], ["lookup", "one_1"], ["insert", "value", "float"], ["lookup", "value"], ["exit"], ["lookup", "value"], ["lookup", "one_1"], ["insert", "value", "char"], ["exit"]]], [[["enter"], ["insert", "a", "int"], ["insert", "a", "int"]]]],
     "Keep a list of dictionaries, one per open scope. Lookup walks the list from the innermost scope outward."),
  PL("Hash table buckets", "Write hash_insert(names, size): hash each name as the sum of its character codes (ord) modulo size, and chain colliding names in insertion order. Return the buckets as a list of size lists. A name already present in its bucket is not added twice.",
     "hash_insert(names, size)", """
def hash_insert(names, size):
    buckets = [[] for _ in range(size)]
    for n in names:
        h = sum(ord(c) for c in n) % size
        if n not in buckets[h]:
            buckets[h].append(n)
    return buckets
""", [[["a", "b", "c", "a", "d"], 3], [["interest", "rate", "year"], 5], [[], 2]], "ord(c) gives the character code."),
  FILL("Symbol table", "Lookup of a missing name returns {{0|zero}}. A name in an inner scope that hides an outer one is {{shadowing|shadowed}}. Most symbol tables are {{hash}} tables.")]))

# ------------------------------------------------------------ 15
CHS.append(CH(
 "Intermediate code generation",
 ("Intermediate code", [
  "Intermediate code | separates | Front end from back end",
  "Intermediate code | can be | High level or low level",
  "Three-address code | has | At most three addresses",
  "Three-address code | is stored as | Quadruples, triples or indirect triples",
  "Triples | refer to results by | Position",
  "Indirect triples | use | Pointers",
  "Declarations | allocate | Offsets in memory"]),
 ["Intermediate code lets one analysis front end serve many machines: only the synthesis part changes with the target. It also makes it easier to apply optimizations that are independent of the machine.",
  "It can be high level, close to the source, or low level, close to the machine, and language specific (Java byte code) or language independent (three-address code). Three-address code has at most three addresses per instruction and is stored as quadruples, triples or indirect triples.",
  "Declarations allocate memory to names consecutively, using an offset that starts at zero and grows by each name's width, and enter the name, type and offset into the symbol table."],
 [("Intermediate representation", "A program for an abstract machine, between the source and the target."),
  ("High-level IR", "Close to the source language; easy to generate and to modify."),
  ("Low-level IR", "Close to the target machine; good for register and instruction selection."),
  ("Three-address code", "Instructions with at most three addresses, such as x = y op z."),
  ("Quadruple", "An instruction with four fields: operator, arg1, arg2 and result."),
  ("Triple", "An instruction with three fields; the result is referred to by its position."),
  ("Indirect triples", "A list of pointers to triples, so the optimizer can reorder them freely."),
  ("Offset", "The relative address of a name within its data area.")],
 ["IR saves writing a full compiler for each machine.",
  "Analysis stays the same; only synthesis changes per target.",
  "Three-address code assumes unlimited registers.",
  "Quadruples have a result field; triples use positions; indirect triples use pointers.",
  "Triples are hard to reorder; indirect triples fix that.",
  "Declarations: offset = offset + width."],
 [T("Source code can be translated directly into target machine code. So why have an intermediate code at all? There are reasons. Without it, each new machine would need a full native compiler. Intermediate code eliminates that, by keeping the analysis portion the same for all the compilers, so only the second part, synthesis, changes with the target machine."),
  T("It also becomes easier to apply code optimization techniques to the intermediate code, since the changes to improve performance do not depend on the machine."),
  T("Intermediate codes can be represented in a variety of ways. A high-level IR is very close to the source language itself. It can be generated easily from the source code and modified for performance, but it is less preferred for target machine optimization. A low-level IR is close to the target machine, which makes it suitable for register and memory allocation and instruction set selection. It is good for machine-dependent optimizations."),
  T("Intermediate code can be language specific, such as byte code for Java, or language independent, such as three-address code."),
  T("The intermediate code generator receives the annotated syntax tree from the semantic analyzer. The tree is converted to a linear representation, such as postfix notation. Intermediate code tends to be machine independent, so the generator assumes an unlimited number of memory storage units, called registers."),
  T("For a = b + c * d, the generator divides the expression into sub-expressions. First c times d goes into a temporary, then b plus that temporary goes into a second, then the result is copied to a. In code, r1 = c * d, then r2 = b + r1, then a = r2."),
  T("A correction to the tutorial. Its listing has a third temporary, r3 = r2 + r1, then a = r3. That extra addition does not belong to a = b + c * d. It would compute b + 2 * c * d. The correct code has just the three instructions above, and the practice section generates exactly these."),
  T("A three-address code has at most three address locations to calculate the expression. It can be represented in two main forms, quadruples and triples. Each instruction in the quadruple form has four fields: the operator, arg1, arg2 and the result. For the example: times with c and d giving r1; plus with b and r1 giving r2; and an assignment of r2 to a."),
  C("""op   arg1  arg2  result
*    c     d     r1
+    b     r1    r2
=    r2          a""", "text"),
  T("Triples have three fields: op, arg1 and arg2. The result of each sub-expression is denoted by the position of the instruction. They are equivalent to a DAG while representing expressions. Triples face the problem of code immovability during optimization: results are positional, so moving an instruction changes the meaning of every reference to it."),
  C("""(0)  *   c    d
(1)  +   b    (0)
(2)  =   a    (1)""", "text"),
  T("Indirect triples are an enhancement over triples. They use pointers instead of positions to store results. This lets the optimizer reposition sub-expressions freely: it reorders the list of pointers, not the triples."),
  T("Declarations. A variable or procedure has to be declared before it can be used. A declaration allocates space in memory and enters the type and name in the symbol table. Taking the program as a collection of procedures, all names can be local to a procedure. Memory is allocated consecutively, in the order the names are declared, and a variable offset starts at zero as the base address. Because the source language and the target machine may store names differently, relative addressing is used."),
  T("The tutorial's example uses C with a 2-byte integer and a 4-byte float, which was true of some old machines; modern compilers use 4 bytes for int. The widths are a parameter, so the rule is the same. Declare int a: the offset is 0, then add the width, so the offset is 2. Then float b: it is placed at offset 2, and the offset becomes 6."),
  T("To enter a name in the symbol table, a procedure called enter is used, with the name, its type and its offset, which is the relative address in the data area. The practice section writes the three-address code generator, the triples generator and the offset allocator.")],
 [("Why use intermediate code?", ["It is faster to run", "Only the back end must change for a new machine", "It removes the need for a parser", "It is shorter than source"], 1, "The analysis part is shared."),
  ("What is a quadruple?", ["Op, arg1, arg2 and result", "Four registers", "Four operators", "A kind of loop"], 0, "A triple omits the result field."),
  ("What problem do triples have?", ["They cannot hold constants", "Reordering breaks the positional references", "They need four fields", "They are machine dependent"], 1, "Indirect triples fix it with pointers."),
  ("How is an offset updated by a declaration?", ["offset = 0", "offset = offset + width", "offset = width", "It is not updated"], 1, "Names are allocated consecutively.")],
 [("Two forms of three-address code?", "Quadruples and triples (and indirect triples)."), ("Example of language-specific IR?", "Java byte code."), ("Registers in IR?", "Assumed unlimited."),
  ("What does enter(name, type, offset) do?", "Creates a symbol table entry.")],
 [MATCH("Representations", "Match each representation with its feature.", [("Quadruples", "Has a result field"), ("Triples", "Refers to results by position"), ("Indirect triples", "Uses pointers so instructions can move"), ("High-level IR", "Close to the source language")]),
  PL("Three-address code", "An expression tree is an atom (a string) or [op, left, right]. Write gen_tac(target, tree). Walk the tree in post-order (left, then right). For each operation emit the quadruple [op, arg1, arg2, temp] where temp is the next of \"t1\", \"t2\", ... and an argument is the atom or the temp that holds the sub-result. Finish with [\"=\", result, \"\", target]. Return the list of quadruples.",
     "gen_tac(target, tree)", """
def gen_tac(target, tree):
    code = []
    count = [0]
    def walk(t):
        if isinstance(t, str):
            return t
        a = walk(t[1])
        b = walk(t[2])
        count[0] += 1
        tmp = 't' + str(count[0])
        code.append([t[0], a, b, tmp])
        return tmp
    res = walk(tree)
    code.append(['=', res, '', target])
    return code
""", [["a", ["+", "b", ["*", "c", "d"]]], ["x", ["-", ["+", "a", "b"], ["*", "c", "d"]]], ["y", "z"]], "A recursive helper returns the name that holds a sub-tree's value: the atom itself or a new temporary."),
  PL("Triples", "Same expression trees. Write gen_triples(target, tree) returning triples [op, arg1, arg2] where a reference to an earlier triple is the string \"(i)\" with i its 0-based position. Finish with [\"=\", target, ref] for the final value (use the atom itself if the tree is a single atom).",
     "gen_triples(target, tree)", """
def gen_triples(target, tree):
    code = []
    def walk(t):
        if isinstance(t, str):
            return t
        a = walk(t[1])
        b = walk(t[2])
        code.append([t[0], a, b])
        return '(' + str(len(code) - 1) + ')'
    res = walk(tree)
    code.append(['=', target, res])
    return code
""", [["a", ["+", "b", ["*", "c", "d"]]], ["x", ["-", ["+", "a", "b"], ["*", "c", "d"]]], ["y", "z"]], "Same walk as before, but the name of a result is its position."),
  PL("Declarations and offsets", "decls is a list of [name, type]; widths is a dictionary from type to size in bytes. Allocate consecutively from offset 0. Write declare(decls, widths): return [entries, total] where entries is a list of [name, type, offset] and total is the final offset.",
     "declare(decls, widths)", """
def declare(decls, widths):
    offset = 0
    entries = []
    for name, t in decls:
        entries.append([name, t, offset])
        offset += widths[t]
    return [entries, offset]
""", [[[["a", "int"], ["b", "float"]], {"int": 2, "float": 4}], [[["i", "int"], ["x", "float"], ["j", "int"]], {"int": 4, "float": 8}], [[], {"int": 4}]], "Record the current offset, then add the width of the type."),
  FILL("Intermediate code", "Three-address code has at most {{three}} addresses. A {{quadruple}} has four fields. A {{triple}} refers to results by position.")]))

# ------------------------------------------------------------ 16
CHS.append(CH(
 "Code generation",
 ("Code generation", [
  "Code generator | maps | Intermediate code to target code",
  "DAG | shows | Flow of values in a basic block",
  "Peephole optimization | works on | Small windows of code",
  "Register descriptor | tracks | Register contents",
  "Address descriptor | tracks | Where each name's value is",
  "getReg | chooses | Register for the result",
  "Code generator | considers | Instruction selection, registers, ordering"]),
 ["Code generation is the final phase. It produces object code in a lower-level language such as assembly, which must carry the exact meaning of the source and be efficient in CPU and memory.",
  "A directed acyclic graph shows how values flow among the statements of a basic block and exposes shared sub-expressions. Peephole optimization improves a small window of code: redundant instructions, unreachable code, jumps to jumps, algebraic simplifications and strength reduction.",
  "A code generator has to select instructions, allocate registers and order instructions. It uses a register descriptor and an address descriptor, and a function getReg picks the register for each result."],
 [("DAG", "A directed acyclic graph of a basic block: leaves are names or constants, interior nodes are operators."),
  ("Peephole optimization", "A local optimization over a small portion of code."),
  ("Redundant instruction", "An instruction whose effect is already achieved by others."),
  ("Unreachable code", "Code that can never be executed because of the control structure."),
  ("Strength reduction", "Replacing an expensive operation by a cheaper one with the same result."),
  ("Register descriptor", "Records what value each register holds."),
  ("Address descriptor", "Records where the value of each name is currently found."),
  ("getReg", "The function that picks the location for a result.")],
 ["The object code must keep the meaning and be efficient.",
  "A DAG shows shared sub-expressions in a basic block.",
  "Peephole: redundant loads, unreachable code, jumps to jumps, algebraic simplification, strength reduction.",
  "x * 2 can become x << 1.",
  "The code generator selects instructions, allocates registers and orders instructions.",
  "Descriptors are updated as code is generated."],
 [T("Code generation can be considered the final phase of compilation. Optimization can still be applied after it, but that can be seen as a part of code generation itself. The code generated by the compiler is object code of some lower-level language, for example assembly language."),
  T("A source program in a higher-level language is transformed into lower-level object code, which should have two minimum properties: it should carry the exact meaning of the source code, and it should be efficient in terms of CPU usage and memory management."),
  T("A directed acyclic graph, DAG, depicts the structure of a basic block, helps to see the flow of values among the statements, and offers optimization too. It makes transformations on basic blocks easy. Leaf nodes represent identifiers, names or constants. Interior nodes represent operators. Interior nodes also represent the results of expressions or the names where the values are stored."),
  T("Example: t0 = a + b, t1 = t0 + c and d = t0 + t1. The plus node of a and b is reused by both later statements. If the same expression appeared twice with unchanged operands, the DAG would hold one node, which is how common sub-expressions are found."),
  T("Peephole optimization works locally on the code to transform it into optimized code. By local we mean a small portion of the code block. It can be applied to intermediate code and to target code. A group of statements is analyzed for these optimizations."),
  T("Redundant instruction elimination. At source level the user can simplify code such as y = 10, z = x + y, return z to return x plus 10. At the compiler level, the compiler looks for redundant instructions, such as multiple loading and storing that mean the same even if some are removed. Move x to R0 followed by move R0 to R1 can be rewritten as move x to R1. That is safe only when R0 is not used afterwards."),
  T("Unreachable code is part of the program that is never accessed because of the programming constructs, such as a statement after a return. It can be removed."),
  T("Flow of control optimization. The program control may jump back and forth without performing any significant task. A label that only passes control to another label can be bypassed. Given a goto L1 where L1 contains only a goto L2, the first jump can go to L2 directly."),
  T("Algebraic expression simplification: a = a + 0 can be replaced by a, and a = a + 1 can be replaced by an increment. Strength reduction replaces operations that consume more time and space with cheaper ones that give the same result. For example, x * 2 can be replaced by x << 1, a single left shift. And a * a is cheaper than a squared, using a power routine. The tutorial writes a2, meaning the square."),
  T("Accessing machine instructions: if the target machine has sophisticated instructions that do specific operations efficiently, using them directly improves the quality of the code."),
  T("A code generator needs to understand the target machine's runtime environment and instruction set. It must take these into account. The target language, which may be CISC or RISC. The IR type: an AST, reverse Polish notation or three-address code. Instruction selection: one IR form can be translated in many ways, and the generator must choose wisely. Register allocation: which values to keep in registers and which registers to use. And ordering of instructions: the order in which instructions execute, a schedule."),
  T("The generator tracks registers and addresses with two descriptors. The register descriptor says which registers are available and what each holds. The address descriptor says where the value of each name is: in a register, on the stack, in memory or several of these. They are updated in real time. For a load LD R1, x, the register descriptor of R1 records that it holds x, and the address descriptor of x records that one copy is in R1."),
  T("Where a value is found in several places, the register is preferred over the cache, which is preferred over main memory."),
  T("The function getReg decides the location L for the result of x = y op z. If y is already in a register, use that register. Otherwise if a register is available, use it. Otherwise choose a register that requires the fewest loads and stores."),
  T("Then the actions for x = y op z. Call getReg to choose L. Find where y is from its address descriptor, and if it is not in L, emit a move of y to L. Find z the same way and emit the operation on z and L. Now L holds y op z, so update the register descriptor of L to say it holds x, and the address descriptor of x to say it is in L. If y and z have no further use, their registers can be given back."),
  T("The practice section writes four peephole passes, a DAG counter that finds common sub-expressions, and a small code generator with descriptors.")],
 [("What does a DAG expose?", ["Syntax errors", "Common sub-expressions in a basic block", "Register names", "The linker"], 1, "Shared nodes are computed once."),
  ("What is strength reduction?", ["Using stronger registers", "Replacing an expensive operation by a cheaper one", "Removing loops", "Adding comments"], 1, "For example x * 2 to x << 1."),
  ("What does the address descriptor record?", ["Register availability", "Where the value of each name is", "Token types", "Line numbers"], 1, "The register descriptor records the registers."),
  ("What does getReg do first?", ["Uses a register already holding y", "Spills everything", "Picks R0 always", "Emits a jump"], 0, "That avoids a load.")],
 [("Peephole means?", "Optimizing a small window of code."), ("Rewrite a = a + 1?", "As an increment."), ("What does x * 8 become?", "x << 3."),
  ("Unreachable code example?", "A statement after a return.")],
 [MATCH("Peephole passes", "Match each optimization with its example.", [("Redundant instruction", "MOV x, R0 then MOV R0, R1"), ("Unreachable code", "A statement after return"), ("Flow of control", "A jump to a label that jumps again"), ("Algebraic simplification", "a = a + 0"), ("Strength reduction", "x * 2 to x << 1")]),
  PL("Algebraic simplification and strength reduction", "Instructions are strings like \"ADD R1, 0\". Write simplify(code). Remove ADD or SUB with 0, and MUL or DIV by 1. Replace \"ADD R, 1\" by \"INC R\". Replace MUL by a power of two 2, 4, 8 by \"SHL R, k\" (k = 1, 2, 3). Leave all other instructions as they are, in order.",
     "simplify(code)", """
def simplify(code):
    out = []
    shifts = {'2': '1', '4': '2', '8': '3'}
    for ins in code:
        op, rest = ins.split(' ', 1)
        reg, val = [x.strip() for x in rest.split(',')]
        if op in ['ADD', 'SUB'] and val == '0':
            continue
        if op in ['MUL', 'DIV'] and val == '1':
            continue
        if op == 'ADD' and val == '1':
            out.append('INC ' + reg)
        elif op == 'MUL' and val in shifts:
            out.append('SHL ' + reg + ', ' + shifts[val])
        else:
            out.append(ins)
    return out
""", [[["ADD R1, 0", "MUL R2, 1", "ADD R3, 1", "MUL R4, 8", "MUL R5, 3", "SUB R6, 2"]], [["MUL R1, 2", "MUL R1, 4"]], [[]]], "Split each instruction into its operation, register and value."),
  PL("Unreachable code", "Instructions are strings. A label is a string ending in a colon. Write remove_unreachable(code): delete every instruction that follows a RET or a GOTO up to (not including) the next label. Labels are always kept.",
     "remove_unreachable(code)", """
def remove_unreachable(code):
    out = []
    dead = False
    for ins in code:
        if ins.endswith(':'):
            dead = False
            out.append(ins)
        elif dead:
            continue
        else:
            out.append(ins)
            if ins == 'RET' or ins.startswith('GOTO'):
                dead = True
    return out
""", [[["MOV R1, 1", "RET", "MOV R2, 2", "L1:", "ADD R1, 1", "GOTO L1", "NOP", "NOP"]], [["ADD R1, 1"]]], "Keep a flag that turns on after RET or GOTO and off at a label."),
  PL("Jump threading", "Write thread_jumps(code). If a label L is immediately followed by GOTO M, then every GOTO L (and every \"IF\" jump ending in L, written like \"JNZ L\") can jump to M instead; repeat until the target no longer changes (follow chains, but stop if a loop is found). Keep every line in place, and only change jump targets. Jumps are GOTO, JNZ and JZ followed by a label.",
     "thread_jumps(code)", """
def thread_jumps(code):
    nxt = {}
    for i in range(len(code) - 1):
        if code[i].endswith(':') and code[i + 1].startswith('GOTO '):
            nxt[code[i][:-1]] = code[i + 1].split(' ')[1]
    def final(lab):
        seen = [lab]
        while lab in nxt:
            lab = nxt[lab]
            if lab in seen:
                break
            seen.append(lab)
        return lab
    out = []
    for ins in code:
        parts = ins.split(' ')
        if len(parts) == 2 and parts[0] in ['GOTO', 'JNZ', 'JZ']:
            out.append(parts[0] + ' ' + final(parts[1]))
        else:
            out.append(ins)
    return out
""", [[["MOV R1, R2", "GOTO L1", "L1:", "GOTO L2", "L2:", "INC R1"]], [["JNZ A", "A:", "GOTO B", "B:", "GOTO C", "C:", "RET"]], [["L1:", "GOTO L1", "GOTO L1"]]], "Build a map from each label to the target of the GOTO right after it. Follow it until it stops changing."),
  PL("DAG nodes", "Statements are [target, op, a, b] for target = a op b. Build the DAG using value numbering: each name has a current node (initially its own leaf). A new operation node is created only if no existing operation node has the same op and the same operand nodes (+ and * are commutative, so the order of operands does not matter). Write dag_ops(stmts): the number of distinct operation nodes. Assigning to a name gives it the node of the right side from then on.",
     "dag_ops(stmts)", """
def dag_ops(stmts):
    node_of = {}
    nodes = {}
    count = [0]
    def leaf(name):
        if name not in node_of:
            count[0] += 1
            node_of[name] = ('leaf', count[0])
        return node_of[name]
    ops = 0
    for target, op, a, b in stmts:
        na = leaf(a)
        nb = leaf(b)
        if op in ['+', '*'] and str(nb) < str(na):
            na, nb = nb, na
        key = (op, na, nb)
        if key not in nodes:
            nodes[key] = ('op', len(nodes))
            ops += 1
        node_of[target] = nodes[key]
    return ops
""", [[[["t0", "+", "a", "b"], ["t1", "+", "t0", "c"], ["d", "+", "t0", "t1"]]], [[["x", "+", "a", "b"], ["y", "+", "b", "a"], ["z", "*", "x", "y"]]], [[["x", "+", "a", "b"], ["a", "+", "a", "1"], ["y", "+", "a", "b"]]], [[]]], "Map every name to a node. Look up (op, node of a, node of b) in a dictionary before creating a new node."),
  PL("A small code generator", "Statements are [x, op, y, z]: op is +, - or * (operands y and z), or = (then z is empty and the statement is x = y). Registers R0, R1, ... are unlimited and taken in order. Rules: if y is a temp (a name starting with t) that is held in register r, reuse r (no load); otherwise take a new register r and emit \"MOV loc(y), r\" where loc(y) is the register holding y if any, else its name. Then emit \"ADD\", \"SUB\" or \"MUL\" followed by \"loc(z), r\" (using z's register if it has one). Now x lives in r. For \"=\": do the same load rule for y, and no operation. If x is not a temp, finish with \"MOV r, x\". Return the list of instruction strings.",
     "codegen(stmts)", """
def codegen(stmts):
    names = {'+': 'ADD', '-': 'SUB', '*': 'MUL'}
    reg_of = {}
    nxt = [0]
    out = []
    def loc(n):
        return reg_of.get(n, n)
    for x, op, y, z in stmts:
        if y.startswith('t') and y in reg_of:
            r = reg_of.pop(y)
        else:
            r = 'R' + str(nxt[0])
            nxt[0] += 1
            out.append('MOV ' + loc(y) + ', ' + r)
        if op != '=':
            out.append(names[op] + ' ' + loc(z) + ', ' + r)
        reg_of[x] = r
        if not x.startswith('t'):
            out.append('MOV ' + r + ', ' + x)
    return out
""", [[[["t1", "*", "c", "d"], ["t2", "+", "b", "t1"], ["a", "=", "t2", ""]]], [[["t1", "+", "a", "b"], ["t2", "-", "t1", "c"], ["x", "*", "t2", "t2"]]], [[["x", "=", "y", ""]]]],
     "Keep a dictionary from name to register. The result register is either a reused temp register or a fresh one."),
  FILL("Code generation", "A {{DAG|dag}} exposes common sub-expressions. Replacing x * 2 by a shift is strength {{reduction}}. The {{address}} descriptor records where each name's value is.")]))

# ------------------------------------------------------------ 17
CHS.append(CH(
 "Code optimization",
 ("Optimization", [
  "Optimization | must | Preserve meaning",
  "Optimization | is | Machine independent or machine dependent",
  "Basic block | has | Straight-line code",
  "Control flow graph | connects | Basic blocks",
  "Loop optimization | uses | Invariant code, induction variables, strength reduction",
  "Dead code | is | Unreachable or unused",
  "Partial redundancy | is removed by | Code motion"]),
 ["Optimization transforms a program so that it uses fewer resources and runs faster, while keeping the meaning, and without slowing the compiler too much. It can be done by the user, on the intermediate code, and on the target code.",
  "Machine-independent optimization works on intermediate code, with no registers or absolute addresses. Machine-dependent optimization uses registers and the memory hierarchy. Basic blocks and the control flow graph structure the program for analysis.",
  "Loops get special attention: moving invariant code out, working with induction variables, and strength reduction. Dead code, partially dead code and partially redundant expressions are removed or moved."],
 [("Machine-independent optimization", "Transforms intermediate code without using CPU registers or absolute memory locations."),
  ("Machine-dependent optimization", "Done after target code is generated; uses registers and the memory hierarchy."),
  ("Basic block", "A sequence of instructions always executed in order, with no jumps in or out except at its ends."),
  ("Control flow graph", "A graph of basic blocks showing how control passes between them."),
  ("Loop-invariant code", "Code in a loop that computes the same value on every iteration."),
  ("Induction variable", "A variable altered in a loop by a loop-invariant amount."),
  ("Dead code", "Code that is never executed or whose output is never used."),
  ("Partially dead code", "Code whose result is used only on some paths."),
  ("Partial redundancy", "An expression computed more than once on some path without a change in operands."),
  ("Code motion", "Moving code to a place where it is computed less often.")],
 ["Rules: keep the meaning; speed up; be fast itself.",
  "Levels: user code, intermediate code, target code.",
  "Leaders start basic blocks: the first statement, branch targets and statements after a branch.",
  "Loop optimizations: invariant code, induction analysis, strength reduction.",
  "Dead code: unreachable or unused result.",
  "Code motion removes partial redundancy."],
 [T("Optimization is a program transformation technique that tries to improve the code by making it consume fewer resources, such as CPU and memory, and deliver higher speed. High-level general constructs are replaced by very efficient low-level code. A code-optimizing process must follow three rules."),
  T("The output code must not in any way change the meaning of the program. Optimization should increase the speed of the program and, if possible, require fewer resources. And optimization should itself be fast, and not delay the overall compiling process."),
  T("Efforts can be made at various levels of the compiling process. At the beginning, users can change or rearrange the code or use better algorithms. After generating intermediate code, the compiler can modify it by address calculations and improving loops. While producing target machine code, the compiler can make use of the memory hierarchy and CPU registers. Optimization is broadly of two types, machine independent and machine dependent."),
  T("In machine-independent optimization, the compiler takes the intermediate code and transforms a part that does not involve CPU registers or absolute memory locations. For example a do-while loop that assigns item = 10 on every iteration before adding it to value can be rewritten with the assignment moved in front of the loop. The repeated assignment of the same value is removed."),
  T("Machine-dependent optimization is done after the target code has been generated, when the code is transformed according to the target architecture. It involves CPU registers and may have absolute memory references rather than relative ones. The optimizers try to take maximum advantage of the memory hierarchy."),
  T("Basic blocks. Source code has a number of instructions that are always executed in sequence, and these are considered the basic blocks. A basic block has no jump statements within it: when the first instruction executes, all the instructions in the block execute in order, with no loss of flow control. Constructs such as if-then-else, switch-case, do-while, for and repeat-until produce basic blocks."),
  T("To find the basic blocks, first find the header statements, the leaders. The first statement of the program is a leader. Statements that are the target of any branch, conditional or unconditional, are leaders. Statements that follow a branch statement are leaders. Each leader and the statements after it, up to the next leader, form a basic block, so a block never contains the header of another block."),
  T("Basic blocks play an important role in identifying variables that are used more than once in a single block. If a variable is used more than once, the register allocated to it need not be emptied until the block finishes."),
  T("A control flow graph represents the basic blocks of a program, and shows how control is passed among them. It helps optimization by locating unwanted loops in the program."),
  T("Loop optimization. Most programs run as a loop in the system, so loops need to be optimized to save CPU cycles and memory. Techniques: invariant code, a fragment inside the loop computing the same value every iteration, can be moved out and computed once. Induction analysis: a variable is an induction variable if its value is altered within the loop by a loop-invariant value. Strength reduction: an expression such as x * 2 is more expensive than x << 1 and gives the same result, so it is replaced."),
  T("Dead-code elimination. Dead code is one or more statements that are either never executed or unreachable, or whose output is never used. Dead code plays no role in any program operation, so it can simply be eliminated."),
  T("Partially dead code: some statements compute values that are used only under some circumstances. In the tutorial's flow graph, a variable a is assigned the value of x * y but not used inside the loop, and right after the loop it is reassigned the value of z. The first assignment is never used, so it can be eliminated. Likewise a conditional statement that is always false means the true branch is never executed and can be removed."),
  T("Partial redundancy. A redundant expression is computed more than once on the same path, without a change in operands. A partially redundant expression is computed more than once on some paths, and only once on others. The tutorial words the two definitions confusingly, but the example makes it clear. Loop-invariant code is partially redundant and can be eliminated by code motion."),
  C("""if (condition) { a = y OP z; }
else { ... }
c = y OP z;          // computed twice when condition is true""", "c"),
  T("If y and z do not change between a and c, then when the condition is true, y OP z is computed twice, otherwise once. Code motion fixes this: compute tmp = y OP z in both branches, assign a = tmp in the true branch, and c = tmp afterwards. Whichever way the condition goes, y OP z is computed exactly once."),
  T("The practice section finds basic blocks, removes dead assignments with a backward pass, and detects loop-invariant statements for code motion.")],
 [("Which is NOT a rule of optimization?", ["Keep the meaning", "Speed up the program", "Make the program longer", "Be fast itself"], 2, "The three rules are about meaning, speed and compile time."),
  ("Which statement starts a basic block?", ["Only the last one", "The first statement and branch targets", "Every assignment", "Comments"], 1, "Also statements following a branch."),
  ("What is loop-invariant code?", ["Code that never loops", "Code computing the same value every iteration", "Code with a jump", "A dead loop"], 1, "It can be moved out of the loop."),
  ("What fixes partial redundancy?", ["Dead-code elimination", "Code motion", "Linking", "Parsing"], 1, "Compute the value once on every path.")],
 [("Machine-independent optimization uses registers?", "No."), ("What is an induction variable?", "A variable changed in a loop by a loop-invariant amount."), ("Dead code?", "Never executed, or its output is never used."),
  ("What does a CFG show?", "How control passes between basic blocks.")],
 [MATCH("Optimizations", "Match each optimization to its idea.", [("Code motion", "Move invariant code out of a loop"), ("Strength reduction", "Cheaper operation, same result"), ("Dead-code elimination", "Remove code whose output is never used"), ("Partial redundancy elimination", "Compute a shared expression once on every path")]),
  PL("Basic blocks", "Code is a list of lines. A label is a line ending in a colon, a jump is \"goto L\" or \"if COND goto L\" (the label is the last word). Write basic_blocks(lines): split the code into basic blocks. Leaders: the first line, every label line that some jump targets, and every line after a jump. Return a list of blocks, each a list of lines.",
     "basic_blocks(lines)", """
def basic_blocks(lines):
    targets = set()
    for ln in lines:
        w = ln.split(' ')
        if 'goto' in w:
            targets.add(w[-1])
    leaders = set([0])
    for i in range(len(lines)):
        ln = lines[i]
        if ln.endswith(':') and ln[:-1] in targets:
            leaders.add(i)
        if 'goto' in ln.split(' ') and i + 1 < len(lines):
            leaders.add(i + 1)
    blocks = []
    for i in range(len(lines)):
        if i in leaders:
            blocks.append([])
        blocks[-1].append(lines[i])
    return blocks
""", [[["x = 0", "L1:", "x = x + 1", "if x < 10 goto L1", "y = x", "goto L2", "z = 1", "L2:", "w = 2"]], [["a = 1", "b = 2"]], [[]]], "Compute the set of leader indices first. Start a new block at each leader."),
  PL("Dead-code elimination", "Statements are [target, uses] where uses is the list of variables the statement reads. Write eliminate_dead(stmts, live_out), where live_out is the list of variables needed after the code. Work backwards: a statement is dead if its target is not live at that point; remove dead statements. Otherwise the target stops being live before it and its uses become live. Return the remaining statements in order.",
     "eliminate_dead(stmts, live_out)", """
def eliminate_dead(stmts, live_out):
    live = set(live_out)
    keep = []
    for target, uses in reversed(stmts):
        if target in live:
            keep.append([target, uses])
            live.discard(target)
            for u in uses:
                live.add(u)
    keep.reverse()
    return keep
""", [[[["a", ["x", "y"]], ["b", ["a"]], ["a", ["z"]], ["c", ["b"]]], ["a", "c"]], [[["t", ["p"]], ["u", ["t"]]], ["u"]], [[["t", ["p"]], ["u", ["q"]]], ["u"]]], "Loop over the statements backwards, keeping a set of live variables."),
  PL("Loop-invariant statements", "A loop body is a list of [target, uses]. A statement is loop-invariant if its target is assigned only once in the loop and every variable it uses is either not assigned in the loop, or assigned by an earlier statement that is itself loop-invariant. Write loop_invariants(body): the 0-based indices of the invariant statements, in order.",
     "loop_invariants(body)", """
def loop_invariants(body):
    counts = {}
    for target, uses in body:
        counts[target] = counts.get(target, 0) + 1
    inv = []
    inv_targets = set()
    for i in range(len(body)):
        target, uses = body[i]
        ok = counts[target] == 1
        for u in uses:
            if u in counts and u not in inv_targets:
                ok = False
        if ok:
            inv.append(i)
            inv_targets.add(target)
    return inv
""", [[[["t", ["a", "b"]], ["i", ["i", "one"]], ["s", ["s", "t"]], ["u", ["t"]]]], [[["x", ["y"]], ["y", ["x"]]]], [[["k", ["c"]], ["k", ["d"]]]]], "A used variable that is assigned in the loop must come from an invariant statement above. Remember that a statement that uses its own target is not invariant."),
  FILL("Optimization", "A basic {{block}} has no jumps inside it. Code that computes the same value every iteration is loop-{{invariant}}. Moving shared computation so it runs once is code {{motion}}.")]))
