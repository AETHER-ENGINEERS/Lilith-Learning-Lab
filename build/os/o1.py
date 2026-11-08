"""Operating Systems course, chapters 1-5."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "trinity"))
from tlib import T, C, M

CH = []

# ---------------------------------------------------------------- 1
CH.append({
    "title": "Operating system overview",
    "maps": [{"title": "What an OS manages", "links": [
        "Operating system | sits between | User and hardware",
        "Operating system | performs | Memory management [ch9]",
        "Operating system | performs | Processor management [ch6]",
        "Operating system | performs | Device management [ch11]",
        "Operating system | performs | File management [ch13]",
        "Operating system | provides | Security [ch14]",
        "Processor management | is also called | Process scheduling",
        "Device management | uses | Device drivers",
        "Job accounting | records | Time and resources used"]}],
    "summary": [
        "An operating system is a program that sits between the user and the computer hardware. It controls how every other program runs and performs the basic tasks: memory, processor, device and file management, plus security and error handling.",
        "Popular examples are Linux, Windows, VMS, OS/400, AIX and z/OS.",
        "Each function follows the same pattern: keep track of a resource, decide who gets it and for how long, allocate it, and take it back when it is no longer needed. Once you see that pattern, the rest of the course is variations on it."],
    "glossary": [
        {"term": "Operating system", "def": "Software that acts as an interface between the user and the hardware and controls the execution of programs."},
        {"term": "Main memory", "def": "A large array of words or bytes, each with its own address, that the CPU can access directly."},
        {"term": "Process scheduling", "def": "Deciding which process gets the processor, when and for how long."},
        {"term": "Traffic controller", "def": "The OS component that tracks the processor and the status of each process."},
        {"term": "I/O controller", "def": "The OS component that tracks all devices."},
        {"term": "File system", "def": "The facilities that organize, locate and protect files, usually arranged into directories."},
        {"term": "Job accounting", "def": "Keeping track of the time and resources used by various jobs and users."},
        {"term": "Multiprogramming", "def": "Keeping several programs in memory so the CPU always has one to run."}],
    "keyPoints": [
        "The OS is the interface between users and hardware.",
        "Main functions: memory, processor, device and file management, security, performance control, job accounting and error detection.",
        "Memory management tracks what is in use, allocates on request and frees on exit.",
        "Processor management is process scheduling.",
        "Device management works through drivers and an I/O controller.",
        "Every resource follows the same cycle: track, decide, allocate, de-allocate."],
    "lesson": [
        T("An operating system, or OS, is an interface between a computer user and the computer hardware. It is software that performs the basic tasks: file management, memory management, process management, handling input and output, and controlling peripheral devices such as disk drives and printers.",
          "Popular operating systems include Linux, Windows, VMS, OS/400, AIX and z/OS."),
        T("The tutorial's definition is short and worth remembering. An operating system is a program that acts as an interface between the user and the computer hardware, and controls the execution of all kinds of programs."),
        T("Here are its important functions. Memory management, processor management, device management and file management. Then security, control over system performance, job accounting, error detecting aids, and coordination between other software and users.",
          "We will spend a chapter or more on each of the big four, so this chapter only sketches them."),
        T("Memory management is about primary memory, also called main memory. Main memory is a large array of words or bytes where each word or byte has its own address. It is fast storage that the CPU accesses directly, and for a program to run, it must be in main memory."),
        T("For memory, the OS keeps track of which parts are in use and by whom. In multiprogramming it decides which process gets memory, when, and how much. It allocates memory when a process asks, and de-allocates it when the process no longer needs it or has terminated."),
        T("Processor management matters in a multiprogramming environment, where the OS decides which process gets the processor and for how much time. This function is called process scheduling. The OS keeps track of the processor and the status of each process; the program responsible is known as the traffic controller.",
          "It allocates the CPU to a process and de-allocates it when the process is no longer required."),
        T("Device management works through drivers. The OS keeps track of all devices; the program responsible is the I/O controller. It decides which process gets a device, when and for how long, allocates the device in the most efficient way, and de-allocates it afterwards."),
        T("File management starts from the idea that a file system is normally organized into directories, which may contain files and other directories. The OS keeps track of information, location, use and status of files. These facilities are collectively known as the file system. It decides who gets resources, allocates them and de-allocates them."),
        T("Then there are other important activities. Security prevents unauthorized access to programs and data by means of passwords and similar techniques. Control over system performance records delays between a request for a service and the response.",
          "Job accounting tracks time and resources used by jobs and users. Error detecting aids produce dumps, traces and error messages. And the OS coordinates compilers, interpreters, assemblers and other software among users."),
        T("Notice the pattern. For memory, processor, devices and files the OS does the same four things: it keeps track of the resource, decides who gets it, allocates it, and takes it back. When you meet a new OS topic later, ask which of these four steps it is about."),
        T("A tiny Python model of the pattern follows. It is a memory ledger: allocate gives a process some memory, free takes it back. The practice section asks you to finish it, and you can run the Python on this device."),
        C("""used = {}

def alloc(name, size):
    used[name] = size

def free(name):
    used.pop(name, None)

alloc("P1", 100); alloc("P2", 50); free("P1")
print(used)          # {'P2': 50}""", "python")],
    "quiz": [
        {"q": "What is an operating system?", "options": ["A compiler", "A program that acts as an interface between the user and the hardware and controls program execution", "A kind of hardware", "A text editor"], "answer": 1, "explain": "That is the tutorial's definition."},
        {"q": "What is main memory?", "options": ["A backup tape", "A large array of words or bytes, each with its own address, that the CPU can access directly", "The hard disk", "The keyboard buffer"], "answer": 1, "explain": "A program must be in main memory to execute."},
        {"q": "What is process scheduling?", "options": ["Naming files", "Deciding which process gets the processor, when and for how long", "Compiling code", "Allocating disk blocks"], "answer": 1, "explain": "It is the processor management function."},
        {"q": "Which activity is job accounting?", "options": ["Checking passwords", "Keeping track of time and resources used by jobs and users", "Producing memory dumps", "Compiling programs"], "answer": 1, "explain": "Accounting records what each job and user consumed."}],
    "cards": [
        {"q": "What does the traffic controller do?", "a": "Keeps track of the processor and of process status."},
        {"q": "What tracks all devices?", "a": "The I/O controller."},
        {"q": "Four steps every resource goes through?", "a": "Track, decide who gets it, allocate, de-allocate."},
        {"q": "Name three popular operating systems.", "a": "Linux, Windows, VMS (also OS/400, AIX, z/OS)."}],
    "practice": [
        {"type": "match", "title": "Function and activity", "intro": "Match each OS function to what it does.", "pairs": [["Memory management", "Tracks what part of main memory is in use and by whom"], ["Processor management", "Decides which process gets the CPU and for how long"], ["Device management", "Decides which process gets a device, through its driver"], ["File management", "Keeps track of file information, location and status"], ["Job accounting", "Records time and resources used by jobs and users"]]},
        {"type": "python", "title": "Memory ledger", "intro": "Write track_memory(ops). Each op is a string: \"alloc NAME SIZE\" or \"free NAME\". Return the processes still holding memory as a list of [name, size] pairs sorted by name. Freeing a name that is not allocated is ignored.", "fn": "track_memory",
         "starter": "def track_memory(ops):\n    # your code\n    pass\n",
         "tests": [{"args": [["alloc P1 100", "alloc P2 50", "free P1"]], "expect": [["P2", 50]]}, {"args": [["alloc B 8", "alloc A 4"]], "expect": [["A", 4], ["B", 8]]}, {"args": [["free X", "alloc X 1", "free X"]], "expect": []}, {"args": [[]], "expect": []}],
         "hint": "Keep a dict. Split each op with .split(). At the end return sorted(d.items()) turned into lists.",
         "solution": "def track_memory(ops):\n    used = {}\n    for op in ops:\n        p = op.split()\n        if p[0] == 'alloc':\n            used[p[1]] = int(p[2])\n        elif p[0] == 'free':\n            used.pop(p[1], None)\n    return [[k, used[k]] for k in sorted(used)]\n"},
        {"type": "fill", "title": "Definitions", "text": "An operating system is an {{interface}} between the user and the computer hardware. Main memory is a large array of words or bytes where each has its own {{address}}. Deciding which process gets the processor is called process {{scheduling}}."}]
})

# ---------------------------------------------------------------- 2
CH.append({
    "title": "Types of operating systems",
    "maps": [{"title": "Kinds of operating system", "links": [
        "Batch system | groups | Similar jobs",
        "Batch system | suffers from | Idle CPU",
        "Time-sharing system | minimizes | Response time",
        "Multiprogrammed batch | maximizes | Processor use",
        "Distributed system | uses | Multiple processors",
        "Network OS | runs on | Server",
        "Real-time OS | needs | Fixed time constraints",
        "Real-time OS | has two kinds | Hard and soft",
        "Time-sharing | extends | Multiprogramming [ch4]"]}],
    "summary": [
        "Operating systems have evolved with each computer generation. The tutorial describes five types: batch, time-sharing, distributed, network and real-time systems.",
        "In a batch system the user does not interact with the computer. Similar jobs are grouped and run together, so the CPU is often idle waiting for slow mechanical I/O. Time-sharing lets many users share one machine, switching so fast that each gets quick responses.",
        "Distributed systems spread work over several loosely coupled processors. Network operating systems run on a server and share files and printers. Real-time systems must respond within fixed time limits, hard or soft."],
    "glossary": [
        {"term": "Batch operating system", "def": "A system where users submit jobs to an operator, who groups similar jobs and runs them without user interaction."},
        {"term": "Time-sharing", "def": "Letting many users at terminals use a computer at the same time, by giving each a short quantum of CPU time."},
        {"term": "Quantum", "def": "The short burst of computation given to one user program before the CPU moves on."},
        {"term": "Distributed system", "def": "Several processors, called sites or nodes, that communicate over lines and are loosely coupled."},
        {"term": "Network operating system", "def": "An OS on a server that manages data, users, groups, security and shared file and printer access."},
        {"term": "Real-time system", "def": "A system with rigid time requirements, where the response time is so small that it controls the environment."},
        {"term": "Hard real-time", "def": "Critical tasks are guaranteed to finish on time. Storage is limited and virtual memory is almost never found."},
        {"term": "Soft real-time", "def": "A critical task gets priority over other tasks and keeps it until it completes. Less restrictive."}],
    "keyPoints": [
        "Batch: no interaction, similar jobs grouped, CPU often idle, hard to set priorities.",
        "Time-sharing minimizes response time. Multiprogrammed batch maximizes processor use.",
        "Distributed systems: several processors, sites can fail independently, resources are shared.",
        "Network OS: runs on a server, centralizes security and shared files and printers.",
        "Real-time: fixed deadlines. Hard guarantees them, soft gives priority.",
        "Real-time examples: industrial control, medical imaging, air traffic control, robots."],
    "lesson": [
        T("Operating systems have been around since the very first computer generation, and they keep evolving. This chapter covers the most common types."),
        T("First, the batch operating system. Users do not interact with the computer directly. Each user prepares a job on an off-line device like punch cards and submits it to the computer operator. To speed up processing, jobs with similar needs are batched together and run as a group. The operator sorts programs with similar requirements into batches."),
        T("Batch systems have three problems. There is no interaction between the user and the job. The CPU is often idle, because mechanical I/O devices are slower than the CPU. And it is difficult to give jobs the priority they want."),
        T("Second, time-sharing systems. Time-sharing lets many people at different terminals use one computer at the same time. It is also called multitasking, a logical extension of multiprogramming. The processor's time is shared among the users.",
          "The difference from a multiprogrammed batch system is the goal. Multiprogrammed batch maximizes processor use. Time-sharing minimizes response time."),
        T("The CPU switches between jobs so frequently that the user gets an immediate response. In transaction processing, each user program runs in a short burst, or quantum, of computation. If n users are present, each gets a quantum, and the response time is a few seconds at most."),
        T("Time-sharing has advantages: quick response, no duplication of software, and less CPU idle time. It has disadvantages too: reliability problems, questions of security and integrity of user programs and data, and problems of data communication."),
        T("Third, the distributed operating system. Distributed systems use multiple central processors to serve multiple real-time applications and users. Jobs are distributed among the processors. The processors talk to each other over communication lines such as buses or telephone lines. These are called loosely coupled systems.",
          "Processors in a distributed system can vary in size and function. They are called sites, nodes or computers."),
        T("The advantages: a user at one site can use resources at another; data exchange speeds up, for example by email; if one site fails the others can carry on; service to customers is better; and the load on the host computer and delays in processing are reduced."),
        T("Fourth, the network operating system. It runs on a server and gives the server the ability to manage data, users, groups, security, applications and other networking functions. Its main purpose is to allow shared file and printer access among multiple computers, typically in a local area network.",
          "The tutorial's examples include Windows Server 2003 and 2008, UNIX, Linux, Mac OS X, Novell NetWare and BSD."),
        T("Network operating systems offer centralized and stable servers, server-managed security, easy upgrades, and remote access. The costs are a high price to buy and run a server, dependence on a central location, and regular maintenance and updates."),
        T("Fifth, the real-time operating system. A real-time system processes and responds to inputs so fast that it controls the environment. The time to respond is called the response time. Real-time systems are used when there are rigid time requirements on a processor or on the flow of data.",
          "A real-time OS must have well-defined, fixed time constraints, otherwise the system fails. Examples are scientific experiments, medical imaging, industrial control, robots and air traffic control."),
        T("There are two kinds. Hard real-time systems guarantee that critical tasks complete on time; secondary storage is limited or missing, data is kept in ROM, and virtual memory is almost never found. Soft real-time systems are less restrictive: a critical task gets priority and keeps it until it completes. Examples are multimedia, virtual reality and planetary rovers."),
        T("To feel the difference between batch and time-sharing, simulate them. The Python below runs jobs in submission order, as a batch would. In the practice section you will group similar jobs into batches, which is what the operator did.")],
    "quiz": [
        {"q": "What is the main problem of a batch system's CPU?", "options": ["It overheats", "It is often idle because mechanical I/O is slower than the CPU", "It has too many users", "It has no memory"], "answer": 1, "explain": "Slow I/O devices leave the CPU waiting."},
        {"q": "What does a time-sharing system try to minimize?", "options": ["Memory use", "Response time", "Cost", "Disk space"], "answer": 1, "explain": "Multiprogrammed batch maximizes processor use; time-sharing minimizes response time."},
        {"q": "What is a loosely coupled system called?", "options": ["Batch system", "Distributed system", "Hard real-time system", "Embedded system"], "answer": 1, "explain": "Processors communicate over lines and do not share memory or a clock."},
        {"q": "Which statement is true of hard real-time systems?", "options": ["They use virtual memory heavily", "They guarantee that critical tasks complete on time", "They have no deadlines", "They are slower than soft real-time"], "answer": 1, "explain": "Secondary storage is limited and virtual memory is almost never found."}],
    "cards": [
        {"q": "Batch vs time-sharing goal?", "a": "Batch (multiprogrammed): maximize processor use. Time-sharing: minimize response time."},
        {"q": "What is a quantum?", "a": "A short burst of computation given to a user program in time-sharing."},
        {"q": "Another word for a processor in a distributed system?", "a": "Site, node or computer."},
        {"q": "Soft vs hard real-time?", "a": "Soft gives critical tasks priority; hard guarantees completion on time."}],
    "practice": [
        {"type": "match", "title": "System and trait", "intro": "Match each type of system to its defining trait.", "pairs": [["Batch", "Similar jobs grouped, no user interaction"], ["Time-sharing", "Minimizes response time with quanta"], ["Distributed", "Loosely coupled sites that communicate over lines"], ["Network OS", "Runs on a server, shares files and printers"], ["Hard real-time", "Guarantees critical tasks finish on time"]]},
        {"type": "python", "title": "Make batches", "intro": "A batch operator groups jobs with the same requirement. Write group_jobs(jobs). Each job is [name, need]. Return a list of batches; each batch is the list of job names that share a need. Order batches by the first appearance of the need, and keep jobs in submission order inside a batch.", "fn": "group_jobs",
         "starter": "def group_jobs(jobs):\n    # your code\n    pass\n",
         "tests": [{"args": [[["J1", "tape"], ["J2", "cards"], ["J3", "tape"]]], "expect": [["J1", "J3"], ["J2"]]}, {"args": [[["a", "x"], ["b", "y"], ["c", "z"], ["d", "y"]]], "expect": [["a"], ["b", "d"], ["c"]]}, {"args": [[]], "expect": []}],
         "hint": "Keep a list of needs in order of first appearance and a dict from need to names.",
         "solution": "def group_jobs(jobs):\n    order = []\n    groups = {}\n    for name, need in jobs:\n        if need not in groups:\n            groups[need] = []\n            order.append(need)\n        groups[need].append(name)\n    return [groups[n] for n in order]\n"},
        {"type": "fill", "title": "Real time", "text": "A {{hard}} real-time system guarantees that critical tasks finish on time, while a {{soft}} real-time system only gives a critical task priority. A time-sharing system gives each user a short {{quantum|time slice}} of CPU time."}]
})

# ---------------------------------------------------------------- 3
CH.append({
    "title": "Operating system services",
    "maps": [{"title": "OS services", "links": [
        "Operating system | provides | Services to programs and users",
        "Program execution | encapsulates activity as | Process [ch5]",
        "I/O operation | uses | Device drivers",
        "File system manipulation | controls | Permissions",
        "Communication | uses | Shared memory",
        "Communication | uses | Message passing",
        "Error handling | keeps | Computing correct and consistent",
        "Resource management | uses | Schedulers",
        "Protection | controls | Access to resources"]}],
    "summary": [
        "An operating system provides services both to the programs that run on it and to the users who run them. The tutorial lists seven: program execution, I/O operations, file system manipulation, communication, error detection, resource allocation and protection.",
        "Program execution means loading a program, running it, and offering process synchronization, communication and deadlock handling. File services decide which program may read or write which file. Communication between processes uses shared memory or message passing.",
        "Errors are detected and handled so computing stays correct. Resources are allocated by schedulers. Protection controls access to resources, authenticating users by passwords."],
    "glossary": [
        {"term": "Process", "def": "The encapsulation of one activity, including its code, data, registers and OS resources in use."},
        {"term": "Driver", "def": "Software that hides the peculiarities of a specific hardware device from users."},
        {"term": "Permission", "def": "The right a program has on a file: read-only, read-write, denied and so on."},
        {"term": "Shared memory", "def": "Communication where processes read and write a common memory area."},
        {"term": "Message passing", "def": "Communication where processes send messages to each other, possibly over a network."},
        {"term": "Resource management", "def": "Allocating memory, CPU cycles and file storage among users and jobs using schedulers."},
        {"term": "Protection", "def": "Controlling access of programs, processes or users to system resources."}],
    "keyPoints": [
        "Seven services: program execution, I/O, file system, communication, error detection, resource allocation, protection.",
        "A process includes the code, data, registers and OS resources in use.",
        "File permissions vary from read-only to read-write to denied.",
        "Communication is by shared memory or message passing.",
        "The OS constantly checks for errors in CPU, I/O devices and memory.",
        "Protection means all access to resources is controlled."],
    "lesson": [
        T("An operating system provides services to both users and programs. It gives programs an environment to execute in, and it gives users convenient ways to run them. The common services are program execution, I/O operations, file system manipulation, communication, error detection, resource allocation and protection."),
        T("Program execution. Operating systems handle many kinds of activities, from user programs to system programs like the printer spooler, name servers and file servers. Each of these activities is encapsulated as a process. A process includes the complete execution context: the code to execute, the data to manipulate, the registers and the OS resources in use."),
        T("With respect to program management the OS loads a program into memory, executes it, handles its execution, and provides mechanisms for process synchronization, process communication and deadlock handling."),
        T("I/O operation. An I/O subsystem comprises I/O devices and their driver software. Drivers hide the peculiarities of specific hardware from users. The OS manages communication between the user and the drivers. An I/O operation means a read or write on a file or on a specific I/O device, and the OS gives access to the device when it is required."),
        T("File system manipulation. A file is a collection of related information. Files are stored on secondary storage for the long term: magnetic tape, magnetic disk, and optical disks like CD and DVD. Each medium has its own speed, capacity, transfer rate and access method. A file system is organized into directories."),
        T("Here is what the OS does for files. A program needs to read or write a file. The OS gives the program permission for the operation, and permission varies from read-only to read-write to denied. The OS provides interfaces to create and delete files and directories, and to back up the file system."),
        T("Communication. In distributed systems, which are collections of processors that share no memory, peripherals or clock, the OS manages communication between processes. Two processes often need to exchange data. They may be on one computer or on different computers connected by a network.",
          "Communication is implemented in two ways: shared memory or message passing."),
        T("Error handling. Errors can occur anywhere: in the CPU, in I/O devices or in memory hardware. The OS constantly checks for possible errors and takes appropriate action to ensure correct and consistent computing."),
        T("Resource management. In a multi-user or multitasking environment, resources such as main memory, CPU cycles and file storage must be allocated to each user or job. The OS manages all kinds of resources using schedulers, and CPU scheduling algorithms are used for better utilization of the CPU."),
        T("Protection. With multiple users and concurrent processes, processes must be protected from each other's activities. Protection is a way to control the access of programs, processes or users to resources. The OS ensures that all access is controlled, that external I/O devices are protected from invalid access attempts, and that users are authenticated, for example by passwords."),
        T("File permission is a clean example of protection plus a service. The practice section has you write the check that decides whether a user may read or write a file, using the permissions idea from this chapter.")],
    "quiz": [
        {"q": "What does a process include?", "options": ["Only code", "Code, data, registers and OS resources in use", "Only data", "Only the file name"], "answer": 1, "explain": "A process includes the complete execution context."},
        {"q": "Which are the two ways processes communicate?", "options": ["Shared memory and message passing", "Batching and spooling", "Paging and segmentation", "Read and write"], "answer": 0, "explain": "Communication is implemented by shared memory or message passing."},
        {"q": "What do drivers do?", "options": ["Compile programs", "Hide the peculiarities of specific hardware devices", "Print files", "Schedule the CPU"], "answer": 1, "explain": "They give the OS a uniform way to talk to devices."},
        {"q": "Which service ensures that all access to resources is controlled?", "options": ["Error handling", "Protection", "Spooling", "Compilation"], "answer": 1, "explain": "Protection controls access to system resources."}],
    "cards": [
        {"q": "Name the seven OS services.", "a": "Program execution, I/O operations, file system manipulation, communication, error detection, resource allocation, protection."},
        {"q": "File permissions range from?", "a": "Read-only, through read-write, to denied."},
        {"q": "What does error handling aim at?", "a": "Correct and consistent computing."},
        {"q": "How does the OS manage resources in a multitasking system?", "a": "With schedulers."}],
    "practice": [
        {"type": "match", "title": "Service and activity", "intro": "Match each service with an activity.", "pairs": [["Program execution", "Loads a program into memory and runs it"], ["I/O operation", "Gives access to the device through its driver"], ["File system manipulation", "Grants read-only, read-write or denied access"], ["Communication", "Shared memory or message passing"], ["Error detection", "Checks CPU, I/O and memory for faults"], ["Protection", "Authenticates users and controls resource access"]]},
        {"type": "python", "title": "Permission check", "intro": "Write check_permission(perms, user, action). perms maps a user name to a string made of the letters r (read) and w (write), for example {\"alice\": \"rw\", \"bob\": \"r\"}. action is \"read\" or \"write\". Return \"allowed\" if the user holds that permission, otherwise \"denied\". An unknown user is denied.", "fn": "check_permission",
         "starter": "def check_permission(perms, user, action):\n    # your code\n    pass\n",
         "tests": [{"args": [{"alice": "rw", "bob": "r"}, "alice", "write"], "expect": "allowed"}, {"args": [{"alice": "rw", "bob": "r"}, "bob", "write"], "expect": "denied"}, {"args": [{"alice": "rw", "bob": "r"}, "bob", "read"], "expect": "allowed"}, {"args": [{"alice": "rw"}, "eve", "read"], "expect": "denied"}],
         "hint": "Map read to 'r' and write to 'w', then test whether that letter is in perms.get(user, '').",
         "solution": "def check_permission(perms, user, action):\n    letter = 'r' if action == 'read' else 'w'\n    if letter in perms.get(user, ''):\n        return 'allowed'\n    return 'denied'\n"},
        {"type": "fill", "title": "Services", "text": "Processes communicate by {{shared memory}} or {{message passing}}. The OS manages resources using {{schedulers}}. Checking for errors in the CPU, I/O devices and memory is called error {{detection|handling}}."}]
})

# ---------------------------------------------------------------- 4
CH.append({
    "title": "Properties of operating systems",
    "maps": [{"title": "OS properties", "links": [
        "Batch processing | runs jobs | First come first served",
        "Multitasking | switches between | Jobs rapidly",
        "Multitasking | is also called | Time-sharing [ch2]",
        "Multiprogramming | keeps in memory | Several jobs",
        "Multiprogramming | needs | CPU scheduling [ch6]",
        "Multiprogramming | needs | Memory management [ch9]",
        "Spooling | uses | Disk as large buffer",
        "Spooling | overlaps | I/O with computation",
        "Real-time system | reads | Sensor data"]}],
    "summary": [
        "This chapter covers the properties an operating system can have: batch processing, multitasking, multiprogramming, interactivity, real-time operation, a distributed environment and spooling.",
        "Multiprogramming keeps several jobs in memory so the CPU always has one to run, which raises CPU utilization but requires CPU scheduling and memory management. Multitasking adds rapid switching so users interact with each program while it runs.",
        "Spooling, short for simultaneous peripheral operations on line, puts the data of I/O jobs in a buffer so slow devices can catch up while the CPU keeps computing."],
    "glossary": [
        {"term": "Batch processing", "def": "Collecting programs and data into a batch before processing starts; jobs run in submission order without manual intervention."},
        {"term": "Multitasking", "def": "Executing multiple jobs by switching between them so often that users can interact with each while it runs."},
        {"term": "Multiprogramming", "def": "Two or more programs residing in memory at the same time, sharing one processor."},
        {"term": "Job pool", "def": "The set of jobs waiting on disk; the jobs in memory are a subset of it."},
        {"term": "Interactivity", "def": "The ability of users to interact with the system through input and output devices."},
        {"term": "Spooling", "def": "Simultaneous peripheral operations on line: putting I/O job data into a buffer on memory or disk."},
        {"term": "Output spool", "def": "Where a finished batch job's output is copied for later printing or processing."}],
    "keyPoints": [
        "Batch: jobs run in submission order; when one finishes its memory is released and output goes to a spool.",
        "Multitasking is time-sharing: each user feels they have their own CPU.",
        "Multiprogramming increases CPU utilization; it needs scheduling and memory management.",
        "Interactivity demands a short response time.",
        "Real-time systems read sensors and must respond in fixed time.",
        "Spooling uses a disk as a very large buffer and overlaps I/O of one job with computation of another."],
    "lesson": [
        T("This chapter looks at properties of operating systems. Several of them extend ideas from chapter 2, but here we see what the OS actually does for each."),
        T("Batch processing is a technique where the OS collects programs and data together in a batch before processing starts. The OS defines a job with a predefined sequence of commands, programs and data as one unit. It keeps a number of jobs in memory and executes them without manual intervention, in the order of submission, first come first served."),
        T("When a job completes, its memory is released and its output is copied into an output spool for later printing or processing. The advantages: much of the operator's work moves to the computer, and a new job starts as soon as the previous one finishes. The disadvantages: programs are difficult to debug, a job could enter an infinite loop, and without protection one batch job can affect pending jobs."),
        T("Multitasking is when multiple jobs are executed by the CPU simultaneously by switching between them. Switches occur so frequently that users can interact with each program while it is running. Multitasking systems are also called time-sharing systems, developed to provide interactive use of a computer at reasonable cost."),
        T("A time-shared OS uses CPU scheduling and multiprogramming to give each user a small portion of the CPU. Each user has at least one separate program in memory. A program that is loaded and executing is a process. A process typically runs only a short time before it finishes or needs I/O."),
        T("Interactive I/O is slow, so it may take a long time to complete. During this time the CPU can be used by another process. Since each command in a time-shared system tends to be short, only a little CPU time is needed per user. As the CPU switches rapidly from one user to the next, each user is given the impression of having their own CPU."),
        T("Multiprogramming is sharing the processor when two or more programs reside in memory at the same time. It assumes a single shared processor. It increases CPU utilization by organizing jobs so the CPU always has one to execute. The OS keeps several jobs in memory, a subset of the job pool, picks one and begins to execute it."),
        T("When the running job waits, for example for I/O, the OS switches to another. Multiprogramming OSs monitor the state of all active programs and system resources using memory management programs, so that the CPU is never idle unless there are no jobs.",
          "Advantages: high CPU utilization, and the feeling that many programs get the CPU almost simultaneously. Disadvantages: CPU scheduling is required, and memory management is required to hold many jobs."),
        T("Interactivity is the ability of users to interact with the system. The OS provides an interface, manages input devices such as the keyboard and output devices such as the monitor. Since the user submits a request and waits for the result, the response time must be short."),
        T("Real-time systems are usually dedicated, embedded systems. The OS typically reads from and reacts to sensor data, and must guarantee a response to events within fixed periods of time to ensure correct performance."),
        T("A distributed environment means multiple independent CPUs or processors. The OS distributes computation among several physical processors. They share no memory or clock; each has its own local memory. They communicate through various communication lines, and the OS manages that communication."),
        T("Spooling is an acronym for simultaneous peripheral operations on line. It puts the data of various I/O jobs in a buffer, a special area in memory or on disk that I/O devices can access. The OS handles spooling because devices have different data access rates.",
          "The spool buffer is a waiting station where data can rest while the slower device catches up. Because of spooling the computer can perform I/O in parallel: read from tape, write to disk and write to a printer while it is computing."),
        T("The advantages of spooling: a disk becomes a very large buffer, and I/O for one job overlaps with processor work for another job. Here is a tiny spooling model in Python; the practice section asks you to complete it."),
        C("""# jobs: [name, arrival, print_time]  (one printer, first come first served)
t = 0
for name, arrival, dur in [["A", 0, 3], ["B", 1, 2]]:
    t = max(t, arrival) + dur
    print(name, "finishes at", t)     # A at 3, B at 5""", "python")],
    "quiz": [
        {"q": "In what order does batch processing run jobs?", "options": ["Random", "Shortest first", "In the order of submission", "Largest first"], "answer": 2, "explain": "First come first served."},
        {"q": "What does multiprogramming increase?", "options": ["Disk space", "CPU utilization", "Screen brightness", "Network speed"], "answer": 1, "explain": "The CPU always has a job to run."},
        {"q": "What does spooling stand for?", "options": ["Simultaneous peripheral operations on line", "Single process operation on line", "Sequential program output on load", "Shared process input on link"], "answer": 0, "explain": "It buffers I/O data so slow devices can catch up."},
        {"q": "Which two things does multiprogramming need?", "options": ["CPU scheduling and memory management", "Only a printer", "Only a keyboard", "Compilers and linkers"], "answer": 0, "explain": "Several jobs share the CPU and the memory."}],
    "cards": [
        {"q": "Where does a finished batch job's output go?", "a": "Into an output spool for later printing or processing."},
        {"q": "Why does each time-sharing user feel they have their own CPU?", "a": "Because the CPU switches between users very quickly."},
        {"q": "Where is the spool buffer?", "a": "A special area in memory or on disk accessible to I/O devices."},
        {"q": "Distributed processors share what?", "a": "Nothing: no shared memory or clock, only communication lines."}],
    "practice": [
        {"type": "order", "title": "Life of a batch job", "intro": "Put these steps in the right order.", "items": ["The OS defines the job as a unit of commands, programs and data", "The job waits and runs in order of submission", "The job executes without manual intervention", "Its memory is released", "Its output goes to the output spool"]},
        {"type": "python", "title": "Printer spooler", "intro": "One printer serves jobs first come first served. Write spool(jobs). Each job is [name, arrival, print_time]. Jobs are given in order of arrival. Return a list of [name, finish_time]. The printer may sit idle until a job arrives.", "fn": "spool",
         "starter": "def spool(jobs):\n    # your code\n    pass\n",
         "tests": [{"args": [[["A", 0, 3], ["B", 1, 2]]], "expect": [["A", 3], ["B", 5]]}, {"args": [[["A", 0, 1], ["B", 5, 2]]], "expect": [["A", 1], ["B", 7]]}, {"args": [[]], "expect": []}, {"args": [[["X", 2, 4], ["Y", 3, 1], ["Z", 4, 1]]], "expect": [["X", 6], ["Y", 7], ["Z", 8]]}],
         "hint": "Keep a clock t. For each job, start = max(t, arrival), then t = start + print_time.",
         "solution": "def spool(jobs):\n    t = 0\n    out = []\n    for name, arrival, dur in jobs:\n        t = max(t, arrival) + dur\n        out.append([name, t])\n    return out\n"},
        {"type": "fill", "title": "Properties", "text": "{{Multiprogramming}} keeps several jobs in memory so the CPU always has one to run. {{Spooling}} uses a disk as a very large buffer. Multitasking systems are also known as {{time-sharing}} systems."}]
})

# ---------------------------------------------------------------- 5
CH.append({
    "title": "Processes",
    "maps": [{"title": "Process concepts", "links": [
        "Program | becomes | Process",
        "Process | has section | Stack",
        "Process | has section | Heap",
        "Process | has section | Text",
        "Process | has section | Data",
        "Process | moves through | Five states",
        "Process | is described by | Process control block",
        "Process control block | is identified by | Process ID",
        "Scheduler [ch6] | moves | Process between states"]}],
    "summary": [
        "A process is a program in execution: the basic unit of work in the system. A program is passive code; a process is its dynamic instance.",
        "In memory a process has four sections: stack for function parameters, return addresses and local variables, heap for memory allocated at run time, text for the code and current activity, and data for global and static variables.",
        "A process passes through five states: start, ready, running, waiting and terminated. The OS tracks each process in a process control block, identified by an integer process ID."],
    "glossary": [
        {"term": "Process", "def": "A program in execution; the basic unit of work implemented in the system."},
        {"term": "Program", "def": "A collection of instructions that performs a specific task when executed."},
        {"term": "Stack", "def": "Process section holding temporary data: function parameters, return address and local variables."},
        {"term": "Heap", "def": "Memory dynamically allocated to a process during its run time."},
        {"term": "Text section", "def": "The code, along with the program counter value and processor registers."},
        {"term": "Data section", "def": "Global and static variables."},
        {"term": "Process control block (PCB)", "def": "The data structure the OS keeps for each process, identified by a process ID."},
        {"term": "Program counter", "def": "The pointer to the address of the next instruction to execute for this process."}],
    "keyPoints": [
        "A program is code; a process is a program in execution.",
        "A process has stack, heap, text and data sections.",
        "Five states: start, ready, running, waiting, terminated.",
        "Ready: waiting for the CPU. Running: executing. Waiting: needs a resource such as input or a file.",
        "A PCB holds state, privileges, ID, parent pointer, program counter, registers, scheduling, memory, accounting and I/O information.",
        "The PCB exists for the lifetime of the process and is deleted when it terminates."],
    "lesson": [
        T("A process is basically a program in execution. Its execution must progress in a sequential fashion. A process is the entity that represents the basic unit of work implemented in the system.",
          "In simple terms: we write programs in a text file, and when we execute the program it becomes a process which performs the tasks mentioned in the program."),
        T("When a program is loaded into memory and becomes a process, it can be divided into four sections: stack, heap, text and data."),
        T("The stack contains temporary data such as method or function parameters, the return address and local variables. The heap is memory dynamically allocated to the process during its run time. The text section includes the current activity, represented by the value of the program counter and the contents of the processor's registers. The data section contains global and static variables."),
        T("A program is a piece of code, from a single line to millions of lines, written by a programmer in some programming language. A program is a collection of instructions that performs a specific task when executed. Compared with a program, a process is a dynamic instance of that program."),
        C("""#include <stdio.h>
int main() {
    printf("Hello, World! \\n");
    return 0;
}""", "c"),
        T("The tutorial also gives definitions around it. A part of a program that performs a well-defined task is an algorithm. A collection of programs, libraries and related data is software."),
        T("Now the process life cycle. When a process executes, it passes through different states. These stages may differ between operating systems, and their names are not standardized. In general a process is in one of five states."),
        T("Start is the initial state, when the process is first created. Ready means the process is waiting to be assigned to a processor. A process comes to ready after start, or when the scheduler interrupts it so the CPU can go to another process."),
        T("Running: once the OS scheduler assigns the processor, the state is running and the processor executes its instructions. Waiting: the process moves to waiting if it needs a resource, such as user input or a file to become available. Terminated: when it finishes, or the OS terminates it, it waits to be removed from main memory."),
        T("For every process the OS keeps a data structure called the process control block, or PCB. It is identified by an integer process ID, the PID. It keeps all the information needed to track the process."),
        T("A PCB records: the process state, process privileges, the process ID, a pointer to the parent process, the program counter, the CPU registers, CPU scheduling information such as priority, memory management information such as page tables and limits, accounting information such as CPU time used, and I/O status information such as the devices allocated."),
        T("The architecture of a PCB depends completely on the operating system and may contain different information in different systems. The PCB is maintained for the process throughout its lifetime and deleted once the process terminates."),
        T("The state machine is easy to simulate. Here is the transition rule in Python. In the practice section you will write the function that walks a process through events and tells you which states it visited."),
        C("""NEXT = {
    ("new", "admit"): "ready",
    ("ready", "dispatch"): "running",
    ("running", "timeout"): "ready",
    ("running", "wait"): "waiting",
    ("waiting", "io_done"): "ready",
    ("running", "exit"): "terminated",
}
print(NEXT[("running", "wait")])      # waiting""", "python")],
    "quiz": [
        {"q": "What is a process?", "options": ["A file on disk", "A program in execution", "A kind of memory", "A device"], "answer": 1, "explain": "A program is passive; a process is its dynamic instance."},
        {"q": "Which section of a process holds local variables and return addresses?", "options": ["Heap", "Stack", "Data", "Text"], "answer": 1, "explain": "The stack holds temporary data."},
        {"q": "Which state does a process enter when it needs user input?", "options": ["Ready", "Running", "Waiting", "Start"], "answer": 2, "explain": "A process waits for a resource such as input or a file."},
        {"q": "What identifies a PCB?", "options": ["A file name", "An integer process ID", "A register", "A page number"], "answer": 1, "explain": "Each PCB is identified by the PID."}],
    "cards": [
        {"q": "Where do global and static variables live?", "a": "The data section."},
        {"q": "List the five process states.", "a": "Start, ready, running, waiting, terminated."},
        {"q": "What does the heap hold?", "a": "Memory allocated dynamically during run time."},
        {"q": "When is a PCB deleted?", "a": "When the process terminates."}],
    "practice": [
        {"type": "match", "title": "Section and contents", "intro": "Match each process section to what it holds.", "pairs": [["Stack", "Function parameters, return addresses, local variables"], ["Heap", "Memory allocated at run time"], ["Text", "Code, program counter and registers"], ["Data", "Global and static variables"]]},
        {"type": "python", "title": "Walk the states", "intro": "Write run_events(events). A process starts in \"new\". The events are: admit (new to ready), dispatch (ready to running), timeout (running to ready), wait (running to waiting), io_done (waiting to ready), exit (running to terminated). Return the list of states entered after each event, in order. If an event is not allowed in the current state, return the string \"error at N\" where N is the 0-based index of that event.", "fn": "run_events",
         "starter": "def run_events(events):\n    # your code\n    pass\n",
         "tests": [{"args": [["admit", "dispatch", "exit"]], "expect": ["ready", "running", "terminated"]}, {"args": [["admit", "dispatch", "wait", "io_done", "dispatch", "timeout"]], "expect": ["ready", "running", "waiting", "ready", "running", "ready"]}, {"args": [["admit", "wait"]], "expect": "error at 1"}, {"args": [["dispatch"]], "expect": "error at 0"}, {"args": [[]], "expect": []}],
         "hint": "Use a dict keyed by (state, event). Stop at the first missing key.",
         "solution": "NEXT = {\n    ('new', 'admit'): 'ready',\n    ('ready', 'dispatch'): 'running',\n    ('running', 'timeout'): 'ready',\n    ('running', 'wait'): 'waiting',\n    ('waiting', 'io_done'): 'ready',\n    ('running', 'exit'): 'terminated',\n}\n\ndef run_events(events):\n    state = 'new'\n    seen = []\n    for i, e in enumerate(events):\n        if (state, e) not in NEXT:\n            return 'error at ' + str(i)\n        state = NEXT[(state, e)]\n        seen.append(state)\n    return seen\n"},
        {"type": "order", "title": "A normal life", "intro": "Order the states of a process that runs, waits for input once, and then finishes.", "items": ["Start", "Ready", "Running", "Waiting", "Ready", "Running", "Terminated"]},
        {"type": "fill", "title": "PCB", "text": "The OS keeps a {{process control block|PCB}} for every process, identified by an integer {{process ID|PID}}. A process waiting for the processor is in the {{ready}} state."}]
})
