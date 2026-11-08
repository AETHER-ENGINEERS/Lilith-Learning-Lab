#!/usr/bin/env python3
"""Build the Operating Systems course. Usage: python3 make_os_course.py <out.json>"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "os"))
import o1, o2, o3  # noqa: E402
from make_trinity_course import split_long, stack  # noqa: E402


def app(name):
    with open(os.path.join(HERE, "os", "apps", name), encoding="utf-8") as f:
        return f.read()


PRONOUNCE = {
    "PCB": "P C B", "CPU": "C P U", "FCFS": "F C F S", "SJN": "S J N", "SJF": "S J F", "SRT": "S R T", "FIFO": "fie foe",
    "LRU": "L R U", "LFU": "L F U", "MFU": "M F U", "OPT": "opt", "MMU": "M M U", "DMA": "D M A", "I/O": "I O", "OS": "O S",
    "RAM": "ram", "DLL": "D L L", "DLLs": "D L Ls", "TCSEC": "T C S E C", "Belady's": "bell a dee's", "Solaris": "so lair iss",
    "Linux": "lin ucks", "Torvalds": "tor valds", "Unix": "you nix", "UNIX": "you nix", "VMS": "V M S", "AIX": "A I X",
    "ASCII": "ask ee", "USB": "U S B", "SMP": "S M P", "daemon": "dee mon", "ps": "P S", "pid": "P I D", "PID": "P I D",
    "quantum": "kwon tum", "spooling": "spool ing", "multiprogramming": "multi pro gramming", "preemptive": "pre empt iv",
    "Tutorialspoint": "tutorials point", "OS/400": "O S 400", "z/OS": "Z O S", "MIN": "min",
}

SANDBOX = {
    "type": "terminal", "title": "OS lookup", "prompt": "os>",
    "intro": "A scripted lookup, not a real operating system. Try: states, sched, mem, io, files, help",
    "chips": ["states", "sched", "mem", "io", "files", "help"],
    "commands": [
        {"re": "^help$", "out": ["states   process states", "sched    scheduling algorithms", "mem      memory management terms", "io       I/O techniques", "files    file allocation methods"]},
        {"re": "^states$", "out": ["new -> ready -> running -> terminated", "running -> waiting (I/O) -> ready", "running -> ready (preempted)"]},
        {"re": "^sched$", "out": ["FCFS  non-preemptive, FIFO", "SJN   non-preemptive, best average wait", "SRT   preemptive SJN", "RR    preemptive, quantum", "Our data: avg wait 5.75, 5.25, 5.0 and 8.5 (RR q=3)"]},
        {"re": "^mem$", "out": ["paging: fixed pages and frames, page table", "segmentation: variable segments", "fragmentation: internal and external", "page replacement: FIFO, LRU, OPT"]},
        {"re": "^io$", "out": ["polling: CPU checks status bit", "interrupt: device signals", "DMA: controller moves a block, one interrupt"]},
        {"re": "^files$", "out": ["contiguous: start and length", "linked: block points to next", "indexed: index block lists blocks"]},
        {"re": ".", "out": ["Unknown command. Type help."], "cls": "warn"}],
    "tasks": []
}

EXAM = [
    ("What is the main job of an operating system?", ["Compile programs", "Sit between user and hardware and manage resources", "Draw graphics", "Store passwords only"], 1, "It manages processes, memory, devices, files and security."),
    ("Which state does a process enter when it is preempted?", ["Waiting", "Ready", "Terminated", "New"], 1, "A preempted process is still able to run."),
    ("What does a PCB hold?", ["Only the program code", "State and information the OS needs to manage a process", "The user's files", "The screen"], 1, "Program counter, registers, scheduling and accounting data."),
    ("Where is a new process always placed?", ["Device queue", "Ready queue", "Swap area", "Disk"], 1, "New processes enter the ready queue."),
    ("Which scheduler is the fastest?", ["Long-term", "Short-term", "Medium-term", "Batch"], 1, "The CPU scheduler runs very often."),
    ("Which algorithm minimizes average waiting time?", ["FCFS", "Shortest job next", "Round robin", "Random"], 1, "But it needs known run times."),
    ("Which algorithm is the preemptive version of SJN?", ["FCFS", "SRT", "Priority", "Multilevel"], 1, "A shorter newcomer takes the CPU."),
    ("What do threads of one process share?", ["Stack", "Registers", "Code, data and open files", "Program counter"], 2, "Each has its own stack, registers and counter."),
    ("What is a race condition?", ["A fast scheduler", "A bug where the result depends on interleaving", "A disk error", "A priority rule"], 1, "Unsynchronized updates can be lost."),
    ("What does the MMU do?", ["Maps virtual to physical addresses", "Schedules threads", "Stores files", "Prints"], 0, "It is hardware."),
    ("External fragmentation is what?", ["A block larger than needed", "Enough free memory but not contiguous", "A page fault", "A swap"], 1, "Compaction can reduce it."),
    ("What does paging avoid?", ["Internal fragmentation completely", "External fragmentation", "Page tables", "Virtual memory"], 1, "Pages and frames are the same size."),
    ("What causes a page fault?", ["Reference to a page not in memory", "A full disk", "A closed file", "A syntax error"], 0, "The OS loads the page."),
    ("Which replacement algorithm has the lowest fault rate?", ["FIFO", "LRU", "OPT", "MFU"], 2, "It needs the future, so is only a benchmark."),
    ("With three frames, how many faults does FIFO have on 7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1?", ["9", "12", "15", "20"], 2, "FIFO 15, LRU 12, OPT 9."),
    ("What does DMA save?", ["Disk space", "One interrupt per word", "Memory", "Power"], 1, "It interrupts once per block."),
    ("What is polling?", ["Device signals the CPU", "CPU repeatedly checks a status bit", "A DMA transfer", "A page fault"], 1, "It wastes CPU time."),
    ("What does a spooler do?", ["Compiles", "Queues jobs for a non-shareable device", "Encrypts", "Swaps pages"], 1, "A daemon prints one job at a time."),
    ("Which allocation method gives fast direct access but suffers external fragmentation?", ["Linked", "Contiguous", "Chained", "None"], 1, "Files need adjacent blocks."),
    ("Why is direct access slow with linked allocation?", ["Blocks are small", "You must follow pointers from the start", "No disk", "Pointers are encrypted"], 1, "Reaching block i reads i earlier blocks."),
    ("What is a trap door?", ["A hidden entry bypassing security", "An antivirus", "A scheduler", "A page"], 0, "Left by the author."),
    ("Why are one-time passwords useful?", ["They are short", "A captured password cannot be reused", "They never change", "They are public"], 1, "Each login needs a fresh password."),
    ("Which component of Linux runs in kernel mode?", ["Utilities", "The kernel", "User programs", "The shell prompt"], 1, "Full access to hardware."),
    ("Which are the four Linux architecture layers?", ["Hardware, kernel, shell, utilities", "CPU, disk, RAM, bus", "Boot, login, run, halt", "User, group, root, other"], 0, "From hardware up to utilities."),
]


def build():
    chapters = o1.CH + o2.CH + o3.CH
    for ch in chapters:
        ch["summary"] = split_long(ch["summary"])
        for b in ch["lesson"]:
            if b["type"] == "math":
                b["tex"] = stack(b["tex"])
            if b["type"] == "text":
                b["items"] = split_long(b["items"])
    html = {"__SCHED__": app("sched.html")}
    for ch in chapters:
        for lab in ch["practice"]:
            if lab["type"] == "webxdc" and lab["html"] in html:
                lab["html"] = html[lab["html"]]
    return {
        "format": "lilith-course", "version": 1, "id": "operating-systems",
        "title": "Operating Systems",
        "subtitle": "Theory and practice, with Python labs",
        "author": "Lilith Learning Lab",
        "description": "A 15-chapter course based on the Tutorialspoint Operating System tutorial: processes, scheduling, threads, memory, virtual memory, I/O, file systems, security and Linux. Each chapter has theory, then Python labs that run on the built-in MicroPython engine. The scheduling data set is the course's own consistent example.",
        "pronounce": PRONOUNCE,
        "chapters": chapters,
        "finalExam": {"title": "Final exam: Operating Systems", "passMark": 70, "size": 20,
                      "questions": [{"q": q, "options": o, "answer": a, "explain": e} for q, o, a, e in EXAM]},
        "sandbox": SANDBOX,
    }


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "operating-systems.course.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=1)
    print("wrote", out)
