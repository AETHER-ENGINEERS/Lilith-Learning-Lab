#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the short Welcome to Lilith University course. Usage: python3 make_lilith_university_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cmk  # noqa: E402
from cd.clib import PL, MATCH, FILL, ORDER, CH, T, C  # noqa: E402

CHS = []
CHS.append(CH(
 "What Lilith University is",
 ("Lilith University", [
  "Lilith University | is | A course catalog",
  "Catalog | lists | Courses",
  "Course | has | Chapters",
  "Chapter | has | Lessons and labs",
  "App | runs | Offline",
  "Website | previews | Courses",
  "Teacher | reads aloud | Lessons"]),
 ["Lilith University is a free library of self-study courses. Each course is one file that you download once and then use offline in the Lilith Learning Lab app.",
  "The website lets you search and read each course outline before you download it. The app holds your courses, shows lessons, reads them aloud with the Teacher, and runs the labs on your own device.",
  "There are no accounts, no tracking and no payments. Your progress stays on your device."],
 [("Catalog", "The list of all available courses with their category, level and tags."),
  ("Course file", "A single .course.json file that holds every lesson, quiz and lab of a course."),
  ("Teacher", "The built-in voice that reads lessons and explains them."),
  ("Lab", "A hands-on exercise that checks your answer, such as code, matching or ordering."),
  ("Offline", "Working without an internet connection once a course is downloaded.")],
 ["A course is one file; the app is the reader.",
  "Browse online in the app, or use the website, to find courses.",
  "Get downloads and imports a course in one tap.",
  "Everything runs on your device, offline.",
  "Categories group courses; levels tell you where to start."],
 [T("Lilith University is a catalog of courses you can study at your own pace. Think of the website as a course shelf and the Lilith Learning Lab app as your desk. On the shelf you read what each course covers. At your desk you actually learn it."),
  T("A course is a single file. It holds chapters, and each chapter holds a lesson, a short quiz, flashcards and labs. Once the file is on your phone, nothing more needs to be downloaded, so you can study on a train or a plane."),
  T("The catalog groups courses by category, such as Mathematics, Computer Science, Languages, and Hardware and Embedded. Each course also has a level, from beginner to advanced, and tags that help search. Start with a level that matches what you already know.")],
 [("What is a course in Lilith University?", ["A single file with chapters, quizzes and labs", "A live video call", "A paid subscription", "A website account"], 0, "One file you keep."),
  ("Does the app need the internet to run a downloaded course?", ["No", "Always", "Only for quizzes", "Only for labs"], 0, "It works offline."),
  ("What does the catalog tell you about a course?", ["Category, level and tags", "Your grade", "Your password", "Your location"], 0, "It helps you choose."),
  ("What is the Teacher?", ["A voice that reads the lessons", "A human tutor on call", "A quiz timer", "A chat room"], 0, "Built in.")],
 [("Catalog", "The list of courses with category, level and tags"), ("Course file", "One file holding the whole course"), ("Offline", "Works with no internet"), ("Teacher", "The built-in voice")],
 [MATCH("Match the term", "Pair each word with its meaning.", [("Catalog", "list of courses"), ("Course file", "one file with everything"), ("Teacher", "reads lessons aloud"), ("Lab", "hands-on exercise")]),
  FILL("The big idea", "A course is a single {{file}} that you download once. After that it works {{offline}} in the app.")]
))

CHS.append(CH(
 "Finding and getting a course",
 ("Getting courses", [
  "You | search | The catalog",
  "Filter | narrows | By category",
  "Level | shows | Where to start",
  "Outline | previews | Chapters",
  "Get | downloads | A course",
  "Library | stores | Your courses",
  "Import | adds | A file by hand"]),
 ["Open Library, then Browse online in the app. Search by name or tag, filter by category, and read the chapter outline. Tap Get to download a course into your library.",
  "You can also import a course file that someone sent you. Courses are plain JSON files, so they can be shared like any other file.",
  "Start with the level that fits you, and look at the outline first: a good course shows its chapters in a sensible order, from basics up."],
 [("Library", "Where your downloaded courses live in the app."), ("Browse online", "The in-app view of the catalog."), ("Outline", "The list of chapter titles for a course."),
  ("Import", "Adding a course file that you already have."), ("Tag", "A short keyword like python or hebrew used for searching.")],
 ["Search, filter, read the outline, tap Get.", "Level tells you where to start.", "Import adds a file you already have.", "Your library holds every course on your device."],
 [T("To find a course, open Browse online. Type a word like python or hebrew into the search box. The results shrink as you type. You can also pick a category to see only that group."),
  T("Tap a course to read its outline before you commit. The outline lists every chapter, so you can see whether it starts where you need it to. When you are happy, tap Get. The app downloads the file and puts it in your library."),
  T("If a friend sends you a course file, use Import and choose the file. The course appears in your library like any other. Courses are stored on your device, so deleting one frees space, and you can download it again whenever you like.")],
 [("What does Get do?", ["Downloads a course into your library", "Deletes a course", "Shares a course", "Starts a quiz"], 0, "One tap."),
  ("What should you read before downloading?", ["The chapter outline", "The source code", "A password", "Nothing"], 0, "It shows the order."),
  ("How do you add a course file a friend sent?", ["Import it", "Retype it", "Email it back", "You cannot"], 0, "It is just a file."),
  ("What does a level tell you?", ["Where to start", "How long the audio is", "Who wrote it", "The file size"], 0, "Beginner to advanced.")],
 [("Get", "Download a course"), ("Import", "Add a file you have"), ("Outline", "The chapter list"), ("Level", "Where to start")],
 [ORDER("Getting a course", "Put the steps in order.", ["Open Browse online", "Search or filter", "Read the outline", "Tap Get", "Open the course from your library"]),
  PL("Filter the catalog", "Write filter_courses(courses, category, tag). Each course is a list [title, category, tags]. Return the sorted titles of courses whose category matches, and which also have the tag if tag is not an empty string.", "filter_courses(courses, category, tag)", '''
def filter_courses(courses, category, tag):
    out = []
    for c in courses:
        if c[1] != category:
            continue
        if tag != "" and tag not in c[2]:
            continue
        out.append(c[0])
    return sorted(out)
''', [[[["Python", "Computer Science", ["python", "code"]], ["Hebrew", "Languages", ["hebrew"]], ["Algorithms", "Computer Science", ["code"]]], "Computer Science", ""],
      [[["Python", "Computer Science", ["python", "code"]], ["Hebrew", "Languages", ["hebrew"]], ["Algorithms", "Computer Science", ["code"]]], "Computer Science", "python"],
      [[["Hebrew", "Languages", ["hebrew"]]], "Mathematics", ""]], "Loop over the courses and skip the ones that do not match.")]
))

CHS.append(CH(
 "How to study a chapter",
 ("Studying a chapter", [
  "Lesson | teaches | Ideas",
  "Quiz | checks | Memory",
  "Flashcards | repeat | Facts",
  "Lab | builds | Skill",
  "Teacher | reads | The lesson",
  "Review | spaces | Repetition",
  "Exam | tests | The whole course"]),
 ["Each chapter has the same shape: a short lesson, a quiz, flashcards and labs. Read or listen to the lesson, answer the quiz, then do the labs, which turn ideas into skill.",
  "Flashcards work best in short daily sessions. Seeing a card again after a day, then three days, then a week, makes it stick.",
  "Do not skip the labs. Typing a line of code or putting steps in order shows you what you really understand."],
 [("Lesson", "The explanation at the start of a chapter."), ("Quiz", "A few questions that check what you just learned."), ("Flashcards", "Question and answer cards for quick review."),
  ("Spaced repetition", "Reviewing material at growing gaps so it is remembered longer."), ("Exam", "The final test covering the whole course.")],
 ["Lesson, quiz, cards, labs: the same loop every chapter.", "Short daily sessions beat one long one.", "Labs turn knowing into doing.", "Listen with the Teacher when your eyes are busy."],
 [T("Every chapter follows one loop. First the lesson explains an idea in plain words. Then the quiz asks a few questions, so you notice what did not stick. The flashcards fix the details, and the labs let you use the idea with your hands."),
  T("A simple plan is twenty minutes a day. Listen to the lesson, answer the quiz, and do one lab. The next day, start with the flashcards from yesterday. Review old cards at growing gaps: one day, three days, one week. This is called spaced repetition and it beats cramming."),
  T("Mistakes are useful. A wrong quiz answer tells you which part to reread, and a failed lab shows you exactly what you misunderstood. When the course ends, take the final exam to see the whole picture.")],
 [("What is the order of a chapter?", ["Lesson, quiz, cards, labs", "Labs, exam, lesson", "Exam only", "Cards only"], 0, "A fixed loop."),
  ("What is spaced repetition?", ["Reviewing at growing gaps", "Reading once", "Cramming at night", "Skipping cards"], 0, "One day, three days, one week."),
  ("Why do the labs matter?", ["They turn ideas into skill", "They are decoration", "They are optional noise", "They replace the lesson"], 0, "Doing beats reading."),
  ("What is a mistake in a quiz good for?", ["Showing what to reread", "Nothing", "Losing the course", "Resetting the app"], 0, "Feedback.")],
 [("Spaced repetition", "Review at growing gaps"), ("Quiz", "Checks what you learned"), ("Lab", "Hands-on practice"), ("Exam", "Whole-course test")],
 [MATCH("Match the part", "Pair each part of a chapter with its job.", [("Lesson", "explains the idea"), ("Quiz", "checks memory"), ("Flashcards", "repeat the facts"), ("Lab", "practice by doing")]),
  PL("Review days", "Write review_days(start, gaps). Given the first study day (an integer) and a list of gaps in days, return the list of review days, each gap counted from the previous review. For start 0 and gaps [1, 2, 4] the days are 1, 3 and 7.", "review_days(start, gaps)", '''
def review_days(start, gaps):
    days = []
    day = start
    for g in gaps:
        day = day + g
        days.append(day)
    return days
''', [[0, [1, 2, 4]], [10, [1, 3, 7, 14]], [5, []]], "Keep a running total.")]
))

CHS.append(CH(
 "Make your own course",
 ("Your own course", [
  "Course | is | A JSON file",
  "Editor | builds | Courses",
  "Chapter | holds | Lesson and quiz",
  "Lab | has | A type",
  "Export | saves | The file",
  "Import | loads | It in the app",
  "Share | spreads | Knowledge"]),
 ["Anyone can write a course. A course is a JSON file in the lilith-course format, and the web editor lets you build one without writing JSON by hand.",
  "Each chapter needs a title, a lesson, a few quiz questions and cards. Labs can be fill-in-the-blank, matching, ordering, Python code, a terminal, or a small web app.",
  "Export your file and import it in the app to try it. If it is good, share it so others can learn from it."],
 [("JSON", "A plain text format for structured data."), ("Editor", "The web page where you build and edit a course."), ("Lab type", "The kind of exercise: fill, match, order, python, terminal or web app."),
  ("Export", "Saving your course as a file."), ("Share", "Giving your course file to other people.")],
 ["A course is a plain JSON file.", "The editor means no hand-written JSON.", "Each chapter: lesson, quiz, cards, labs.", "Test by importing into the app, then share."],
 [T("A course is plain text in a format called JSON. It lists chapters, and each chapter has a title, a summary, a lesson, quiz questions, flashcards and labs. You do not have to write this by hand, because the editor on the Lilith University site gives you forms for everything."),
  T("The lab types give you variety. A fill lab blanks out words, a match lab pairs items, an order lab sorts steps, and a Python lab runs your code against tests. A terminal lab simulates a command line, and a web app lab can hold a small interactive tool."),
  T("Start small. Make one chapter, export the file, and import it into the app. Fix what feels awkward, add the next chapter, and repeat. When a course is ready, share the file, and it works the same on every device.")],
 [("What format is a course file?", ["JSON", "PDF", "MP3", "Word"], 0, "Plain structured text."),
  ("Which tool builds a course without hand-written JSON?", ["The editor", "The camera", "The clock", "The keyboard only"], 0, "It has forms."),
  ("Which is a lab type?", ["Match", "Poster", "Podcast", "Chat"], 0, "Fill, match, order, python."),
  ("How do you test your new course?", ["Export it and import into the app", "Print it", "Wait a year", "Delete it"], 0, "Try it for real.")],
 [("JSON", "Plain text data format"), ("Editor", "Where you build courses"), ("Export", "Save the course file"), ("Lab type", "Fill, match, order, python, terminal, web app")],
 [MATCH("Match the lab type", "Pair each lab type with what it does.", [("fill", "blank out words"), ("match", "pair items"), ("order", "sort the steps"), ("python", "run code against tests")]),
  PL("Count the quiz", "Write count_quiz(chapters). Each chapter is a dict with a key 'quiz' holding a list of questions. Return the total number of quiz questions.", "count_quiz(chapters)", '''
def count_quiz(chapters):
    total = 0
    for c in chapters:
        total += len(c["quiz"])
    return total
''', [[[{"quiz": [1, 2, 3]}, {"quiz": [1]}]], [[]], [[{"quiz": []}, {"quiz": [1, 2]}]]], "Add the length of each chapter's list.")]
))

SANDBOX = cmk.terminal("Lilith University guide", "uni>", "A scripted guide. Try: courses, study, start, make", [
    ("courses", ["Browse online > search > filter by category > read the outline > Get"]),
    ("study", ["Lesson, quiz, flashcards, labs. Twenty minutes a day. Review cards after 1, 3 and 7 days."]),
    ("start", ["Pick a beginner course in a subject you like. Do one chapter today."]),
    ("make", ["Open the editor, add a chapter, export the file, import it in the app, then share it."]),
])

EXAM = [
 ("What is a Lilith University course?", ["A single file with lessons, quizzes and labs", "A live class", "A paid plan", "A video"], 0, "One file."),
 ("Do you need the internet after you download a course?", ["No", "Yes, always", "Only for quizzes", "Only at night"], 0, "Offline."),
 ("What does the outline show?", ["The chapters of a course", "Your score", "Your password", "The price"], 0, "Read it first."),
 ("What does Get do?", ["Downloads a course", "Deletes it", "Grades it", "Prints it"], 0, "Into your library."),
 ("How do you add a course file someone sent?", ["Import it", "Retype it", "Email it back", "You cannot"], 0, "Just a file."),
 ("What is the order of a chapter?", ["Lesson, quiz, cards, labs", "Labs, lesson", "Cards only", "Exam first"], 0, "A loop."),
 ("What is spaced repetition?", ["Reviewing at growing gaps", "Reading once", "Cramming", "Skipping"], 0, "Better memory."),
 ("Why do labs matter?", ["They turn ideas into skill", "They are decoration", "They replace lessons", "They are timers"], 0, "Doing."),
 ("What format is a course file?", ["JSON", "PDF", "MP3", "DOC"], 0, "Plain text."),
 ("Which tool builds a course visually?", ["The editor", "The camera", "The clock", "The mouse only"], 0, "Forms."),
 ("Which is a lab type?", ["Order", "Poster", "Podcast", "Chat"], 0, "Sorts steps."),
 ("What is a good way to test a new course?", ["Export and import it", "Print it", "Wait", "Delete it"], 0, "Try it."),
]
CFG = dict(id="lilith-university", title="Welcome to Lilith University",
    subtitle="A very short guide to finding, getting, studying and making courses",
    description="A four-chapter orientation to Lilith University and the Lilith Learning Lab app: what a course is, how to find and download one, how to study a chapter with quizzes, flashcards and labs, and how to build and share your own course.",
    pronounce={"Lilith": "lil ith", "JSON": "jay son"}, sandbox=SANDBOX, exam=EXAM, appdir="lu", apps={})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "lilith-university.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
