# Lilith Learning Lab

A standalone, offline Android app with a talking, animated Teacher. It comes **empty**: you import courses as JSON files, and it teaches them as animated lectures with concept maps, glossary, key points, quizzes, practice labs, a final exam and progress tracking.

* Every chapter: concept map (with an animated tour), summary, glossary, key points, lesson, then quiz and practice.
* Practice labs: fill, order, match, write, code (JavaScript, runs on the device), scripted terminal, and **webxdc** apps that can travel inside the course JSON.
* Final exam: a course can define `finalExam`; otherwise it is built from the chapter quizzes.
* Courses are stored on the device, can be deleted, and can be shared as JSON. Progress is kept per course.
* No internet permission. Voice uses the phone's own text-to-speech.

## Courses (`courses/`)

* `jetson-agx-xavier.course.json`: the NVIDIA Jetson AGX Xavier course (23 chapters).
* `sample-percentages.course.json`: a tiny second-subject sample.

Course format: see the header of `build/src/course.js` or use "Template" and "AI prompt" in the app's library.

## Build

* `build/make_course.py <out.json>` and `build/make_sample.py <out.json>` regenerate the courses.
* `python3 build/build_web.py --web <dir>` writes the web app (`index.html` + `avatar/`).
* `node build/tests/test_course.js`, `python3 build/tests/ui_test.py <web dir> courses [shots]` (Playwright) run the tests.
* `android/build_apk.sh` builds and signs the APK with the plain Android SDK tools (no Gradle). It creates a local keystore on first run; do not commit it.

## Jade

`jade/tools/lilith_tool.js` (search, read, quiz, validate courses) and `jade/skills/lilith-learning-lab/SKILL.md`. `xavier_tool.js` adds a trtexec builder, DLA checker and simulated shell for the Xavier course.

Avatar art is the non-explicit frame set only. The APK is untested on a physical device from the build environment.
