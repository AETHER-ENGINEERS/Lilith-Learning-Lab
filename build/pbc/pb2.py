"""PocketBase course, chapters 8-13."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

B = []

B.append(CH(
 "Realtime subscriptions",
 ("Realtime", [
  "Client | opens | An SSE connection", "Server | sends | PB_CONNECT", "Client | submits | Subscriptions", "Topic | is | Collection and star or id",
  "Event | has | Action and record", "Rules | filter | What clients receive", "SDK | reconnects | Automatically"]),
 ["Realtime uses Server-Sent Events, a one-way stream from server to browser. The client opens a connection, the server answers with a client id, and then the client says what it wants to follow.",
  "You subscribe to a whole collection with the star topic or to one record by id. Each event says whether a record was created, updated or deleted.",
  "The same rules apply: you only receive events for records you may view."],
 [("SSE", "Server-Sent Events: a long-lived HTTP response that streams messages to the client."), ("Subscription", "A request to receive events for a topic."), ("Topic", "What you follow: a collection (star) or one record id."),
  ("Event", "A message with an action and the changed record."), ("PB_CONNECT", "The first event, carrying the client id."), ("Custom topic", "A topic you publish yourself from server code.")],
 ["The realtime API is SSE with two steps: connect, then submit subscriptions.", "SSE events are sent for create, update and delete.", "pb.collection('posts').subscribe('*', cb) follows the collection; subscribe(id, cb) follows one record.",
  "Events respect the list and view rules, and a subscribe can take filter and fields options.", "View collections send no realtime events.", "The SDK reconnects by itself and resubscribes."],
 [T("Normal HTTP is request and answer. Realtime flips it: the screen keeps one connection open and the server pushes news when it has some. PocketBase uses Server-Sent Events for this, which is plain HTTP, one direction, and works through ordinary proxies."),
  T("The flow has two steps. First the client opens the stream and the server immediately sends an event called PB_CONNECT with a client id. Second, the client posts its list of topics along with that id. A topic is a collection followed by a star, or a collection followed by a record id."),
  C("// follow every change in the collection\nconst unsub = await pb.collection('messages').subscribe('*', (e) => {\n  console.log(e.action);   // 'create' | 'update' | 'delete'\n  console.log(e.record);\n}, { filter: 'room = \"lobby\"' });\n\n// later\nunsub();                              // stop this listener\npb.collection('messages').unsubscribe(); // stop all in the collection", "javascript"),
  T("Rules matter here as well. For each event the server checks whether this client would be allowed to view the record, using the collection's rules. A client that may not see a record never learns that it changed. The filter option narrows a subscription further, and fields trims what is sent."),
  T("On the client you typically keep a list in memory. On create you add the record, on update you replace it by id, and on delete you remove it. That gives you a live list with very little code."),
  T("You can also publish your own topics from JavaScript or Go on the server, and the browser subscribes with pb.realtime.subscribe. Remember that every open client is a connection: for large audiences raise the open file limit of the host, as the production chapter explains.")],
 [("What does realtime use?", ["Server-Sent Events", "WebSockets only", "Polling", "Email"], 0, "A one-way stream."),
  ("What does subscribe('*') follow?", ["Every record in the collection", "One record", "Only deletes", "Files"], 0, "The star topic."),
  ("What do the rules decide?", ["Which events a client receives", "The port", "Colors", "Backups"], 0, "Viewing rights.")],
 [("What is PB_CONNECT?", "The first event with a client id."), ("What actions do events have?", "Create, update, delete."), ("Which collection sends no events?", "View collections."), ("How do you stop listening?", "unsubscribe.")],
 [MATCH("Realtime", "Match each item with its role.", [("PB_CONNECT", "Carries the client id"), ("subscribe('*')", "Follows the whole collection"), ("subscribe(id)", "Follows one record"), ("unsubscribe()", "Stops listening")]),
  PL("Who gets the event", "Write dispatch(subs, event): subs is a list of [client, topic] where topic is 'collection/*' or 'collection/id'. event is [collection, record_id]. Return the sorted list of distinct clients subscribed to either the collection star topic or that record.",
     "dispatch(subs, event)", """
def dispatch(subs, event):
    coll, rid = event
    want1 = coll + '/*'
    want2 = coll + '/' + rid
    out = set()
    for client, topic in subs:
        if topic == want1 or topic == want2:
            out.add(client)
    return sorted(out)
""", [[[["c1", "posts/*"], ["c2", "posts/p1"], ["c3", "posts/p2"], ["c4", "users/*"]], ["posts", "p1"]], [[["c1", "posts/*"], ["c1", "posts/p1"]], ["posts", "p1"]], [[], ["posts", "p1"]]], "Compare each topic with both wanted topics.", approx=None),
  PL("Keep a live list", "Write apply_event(items, event): items is a list of [id, title]. event is [action, id, title]. Create appends, update replaces the title of the item with that id, delete removes it. Return the new list.",
     "apply_event(items, event)", """
def apply_event(items, event):
    action, rid, title = event
    out = []
    if action == 'create':
        for it in items:
            out.append([it[0], it[1]])
        out.append([rid, title])
        return out
    for it in items:
        if it[0] == rid:
            if action == 'update':
                out.append([rid, title])
        else:
            out.append([it[0], it[1]])
    return out
""", [[[["a", "A"]], ["create", "b", "B"]], [[["a", "A"], ["b", "B"]], ["update", "b", "B2"]], [[["a", "A"], ["b", "B"]], ["delete", "a", ""]], [[], ["create", "x", "X"]]], "Handle each action in turn.", approx=None)]))

B.append(CH(
 "Files and storage",
 ("Files", [
  "File field | stores | Uploaded files", "Upload | uses | Multipart form data", "Storage | is | pb_data/storage", "Filename | gets | A random suffix",
  "URL | is | /api/files/...", "Thumb | resizes | Images", "Protected | needs | A file token"]),
 ["A file field stores uploads in the record. You send them as multipart form data, and PocketBase saves them on disk under pb_data, or in an S3 compatible store if you configure one.",
  "Each file is served at /api/files/COLLECTION/RECORD/FILENAME. For images you can ask for a thumbnail with the thumb query parameter.",
  "A protected file needs a short-lived file token and obeys the view rule."],
 [("File field", "A field that holds one or more uploaded file names."), ("Multipart form", "An HTTP body format that can carry files."), ("Thumb", "A resized copy of an image, requested as WxH."),
  ("Protected file", "A file that can only be fetched with a token and a passing rule."), ("S3 storage", "Storing uploads in an object store instead of on local disk."), ("MIME type", "The kind of a file, such as image/png.")],
 ["File fields set maxSelect, maxSize and allowed MIME types.", "The record keeps the file name; the file lives under pb_data/storage/COLLECTION_ID/RECORD_ID/.", "PocketBase adds a random suffix to uploaded names so they do not collide.",
  "The URL is /api/files/COLLECTION/RECORD_ID/FILENAME, and ?thumb=100x100 returns a thumbnail.", "Thumb sizes must be listed in the field options.", "Protected files are fetched with ?token= from a file token request."],
 [T("A file field is an ordinary field in your collection. Set whether it holds one file or several, the maximum size, and which MIME types are allowed. In the browser you send a FormData object, or a plain object with File values in the SDK, which turns it into a multipart request."),
  C("const form = new FormData();\nform.append('title', 'My photo');\nform.append('image', fileInput.files[0]);\nconst rec = await pb.collection('photos').create(form);\n\n// build the file address, with a 100x100 thumbnail\nconst url = pb.files.getURL(rec, rec.image, { thumb: '100x100' });", "javascript"),
  T("On disk the file goes under the pb_data folder in a path made of the collection id and the record id. PocketBase adds a short random suffix to the name, so two people who upload photo.png do not overwrite each other. The record stores the new name."),
  T("The public address is made of /api/files, the collection, the record id and the filename. For images you can add thumb with a size like 100x100. A size with a zero keeps the proportions, like 0x300. An optional letter after the size chooses how to crop: t for the top, b for the bottom, f to fit inside. The sizes must be allowed in the field settings, so nobody can ask for a thousand different thumbnails."),
  T("Files are public by default if you know the address. If a field is set as protected, the file can only be fetched with a short-lived token that you request while signed in. The token is checked against the record's view rule, and a rule can see the case with @request.context = \"protectedFile\"."),
  T("If you run several servers or want cheap storage, switch to an S3 compatible store in the settings. Backups can go to S3 too. Remember that local files live in pb_data, so back them up with the database.")],
 [("Where does the file name live?", ["In the record's file field", "In a cookie", "In the rules", "In the hooks"], 0, "The record keeps the name."),
  ("What does ?thumb=100x100 return?", ["A resized image", "A zip", "The record", "Nothing"], 0, "A thumbnail."),
  ("How is a protected file fetched?", ["With a file token", "By anyone", "By email", "With the admin password"], 0, "A short-lived token.")],
 [("How do you upload?", "Multipart form data."), ("Why a random suffix?", "To avoid collisions."), ("What does 0x300 mean?", "Keep proportions, height 300."), ("Where is S3 set?", "In the settings.")],
 [FILL("Files", "A file is served at /api/{{files}}/COLLECTION/RECORD/FILENAME and a thumbnail is requested with ?{{thumb}}=100x100."),
  PL("File address", "Write file_url(base, collection, record_id, filename, thumb): return base (without a trailing slash) + '/api/files/' + collection + '/' + record_id + '/' + filename, and add '?thumb=' + thumb when thumb is not None.",
     "file_url(base, collection, record_id, filename, thumb)", """
def file_url(base, collection, record_id, filename, thumb):
    url = base.rstrip('/') + '/api/files/' + collection + '/' + record_id + '/' + filename
    if thumb is not None:
        url += '?thumb=' + thumb
    return url
""", [["http://127.0.0.1:8090", "photos", "r1", "a_x1.png", None], ["http://127.0.0.1:8090/", "photos", "r1", "a_x1.png", "100x100"], ["https://x.io", "docs", "d", "f.pdf", None]], "Strip the slash, then join.", approx=None),
  PL("Parse a thumb size", "Write parse_thumb(spec): a size is WxH with an optional last letter t, b or f. Return [width, height, mode] where mode is 'center' by default, or 't', 'b', 'f' for the letter, or 'resize' when either number is 0. Return an empty list when the spec is invalid (not two numbers, or both zero).",
     "parse_thumb(spec)", """
def parse_thumb(spec):
    mode = ''
    core = spec
    if spec[-1:] in ('t', 'b', 'f'):
        mode = spec[-1]
        core = spec[:-1]
    parts = core.split('x')
    if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
        return []
    w = int(parts[0])
    h = int(parts[1])
    if w == 0 and h == 0:
        return []
    if w == 0 or h == 0:
        return [w, h, 'resize']
    return [w, h, mode or 'center']
""", [["100x100"], ["100x300t"], ["0x300"], ["100x0"], ["0x0"], ["abc"], ["50x50f"], ["100"]], "Peel off the letter first.", approx=None),
  PL("Upload check", "Write upload_errors(mime, size, allowed, max_size): return a sorted list of problems: 'too large' when size is over max_size, and 'type not allowed' when allowed is not empty and mime is not in it.",
     "upload_errors(mime, size, allowed, max_size)", """
def upload_errors(mime, size, allowed, max_size):
    errors = []
    if size > max_size:
        errors.append('too large')
    if allowed and mime not in allowed:
        errors.append('type not allowed')
    return sorted(errors)
""", [["image/png", 100, ["image/png"], 500], ["text/plain", 100, ["image/png"], 500], ["image/png", 900, [], 500], ["text/plain", 900, ["image/png"], 500]], "Two independent checks.", approx=None)]))

B.append(CH(
 "Extending with JavaScript",
 ("Hooks", [
  "pb_hooks | holds | pb.js files", "routerAdd | adds | A route", "onRecordCreate | wraps | A record insert", "e.next | continues | The chain",
  "cronAdd | schedules | A job", "$app | is | The app", "types.d.ts | gives | Editor types"]),
 ["The prebuilt PocketBase runs JavaScript files that end in .pb.js from the pb_hooks folder. With them you add routes, react to events, and schedule jobs, without compiling anything.",
  "An event hook is a function that receives an event e. Code before e.next runs before the action, code after it runs after. Not calling e.next, or throwing, stops the chain.",
  "The engine is goja, a JavaScript interpreter written in Go, so it supports ES5 and a good part of newer syntax, but no ES modules."],
 [("Hook", "A function that runs when something happens."), ("Event", "The object a hook receives, with the app and the record or request."), ("e.next()", "Passes control to the next handler and then to the action itself."),
  ("routerAdd", "Registers a custom HTTP route."), ("cronAdd", "Registers a job on a cron schedule."), ("goja", "The JavaScript engine inside PocketBase.")],
 ["Put hooks in pb_hooks/*.pb.js next to the executable.", "routerAdd('GET', '/hello/{name}', (e) => e.json(200, {...})) adds a route.", "onRecordCreate runs before the insert; onRecordAfterCreateSuccess runs after it commits.",
  "A hook must call e.next() to continue; throwing an error stops the chain.", "You can add collection names after the handler to run it only for those collections.", "cronAdd('name', '*/30 * * * *', fn) runs a job on a five field cron schedule."],
 [C("// pb_hooks/main.pb.js\nrouterAdd(\"GET\", \"/hello/{name}\", (e) => {\n  const name = e.request.pathValue(\"name\")\n  return e.json(200, { message: \"Hello \" + name })\n})\n\n// run before every new post is saved\nonRecordCreate((e) => {\n  e.record.set(\"title\", e.record.get(\"title\").trim())\n  e.next()\n}, \"posts\")\n\nonRecordAfterCreateSuccess((e) => {\n  console.log(\"created\", e.record.id)\n  e.next()\n}, \"posts\")\n\ncronAdd(\"cleanup\", \"0 3 * * *\", () => {\n  console.log(\"nightly job\")\n})", "javascript"),
  T("Any file in the pb_hooks folder that ends in .pb.js is loaded when the server starts. Inside it you use global functions like routerAdd, onRecordCreate and cronAdd, and the global $app for the running application. The __hooks variable gives the absolute path to the folder."),
  T("Routes give you endpoints that the automatic API does not have, for example a call that charges a card. A route handler receives an event e and answers with e.json, e.string and similar helpers. You can add middleware such as a check that the caller is signed in."),
  T("Event hooks wrap things that PocketBase does. Think of onRecordCreate as a function around the insert. Code you put before e.next runs first. Calling e.next lets the next handler and then the real insert run. Code after e.next runs after the insert returns. If you throw, or never call e.next, the chain stops and the insert does not happen."),
  T("There are also hooks for after success and after error, for requests, for authentication, for mail, and for the server starting. Pass collection names after the handler to limit it. For editor help, add a reference line to pb_data/types.d.ts at the top of your file, and the editor will know every function."),
  T("The hook engine is for small amounts of logic. Each file is loaded in a sandbox, and handlers do not share mutable state, so keep shared data in the database. If your logic grows, you can move to the Go framework in the next chapter.")],
 [("Where do hook files go?", ["pb_hooks/*.pb.js", "pb_public", "pb_data", "Any folder"], 0, "Next to the executable."),
  ("What happens if a hook never calls e.next()?", ["The chain stops", "The action runs twice", "Nothing", "It restarts"], 0, "Not calling next ends it."),
  ("Which engine runs the hooks?", ["goja", "V8", "Node", "Deno"], 0, "A Go interpreter.")],
 [("What is $app?", "The running application."), ("What does routerAdd do?", "Adds an HTTP route."), ("What gives editor types?", "pb_data/types.d.ts."), ("What is cronAdd for?", "Scheduled jobs.")],
 [MATCH("Hooks", "Match each function with its job.", [("routerAdd", "Add an HTTP route"), ("onRecordCreate", "Wrap the record insert"), ("cronAdd", "Schedule a job"), ("e.next()", "Continue the chain")]),
  PL("Hook chain", "Write run_chain(handlers): handlers is a list of booleans, true when that handler calls e.next(). Handler i logs 'i:before' first. If it calls next, the next handler runs (or, after the last handler, the action logs 'INSERT'), and then it logs 'i:after'. A handler that does not call next logs nothing more. Return the log list.",
     "run_chain(handlers)", """
def run_chain(handlers):
    log = []
    def run(i):
        if i == len(handlers):
            log.append('INSERT')
            return
        log.append(str(i) + ':before')
        if handlers[i]:
            run(i + 1)
            log.append(str(i) + ':after')
    run(0)
    return log
""", [[[True, True]], [[True, False]], [[False]], [[]], [[True, True, True]]], "Use a recursive helper.", approx=None),
  PL("Cron match", "Write cron_match(expr, minute, hour, dom, month, dow): true when the five field cron expression matches. Each field may be *, */n, a number, a range a-b, or a comma list of those. Fields are minute, hour, day of month, month, day of week (0 is Sunday). */n counts from the first value of the field (0 for minute, hour and weekday, 1 for day and month).",
     "cron_match(expr, minute, hour, dom, month, dow)", """
def cron_match(expr, minute, hour, dom, month, dow):
    fields = expr.split()
    values = [minute, hour, dom, month, dow]
    starts = [0, 0, 1, 1, 0]
    for i in range(5):
        v = values[i]
        ok = False
        for part in fields[i].split(','):
            if part == '*':
                ok = True
            elif part.startswith('*/'):
                if (v - starts[i]) % int(part[2:]) == 0:
                    ok = True
            elif '-' in part:
                a, b = part.split('-')
                if int(a) <= v <= int(b):
                    ok = True
            elif int(part) == v:
                ok = True
        if not ok:
            return False
    return True
""", [["*/30 * * * *", 30, 5, 1, 1, 0], ["*/30 * * * *", 15, 5, 1, 1, 0], ["0 2 * * *", 0, 2, 9, 11, 1], ["0 2 * * *", 1, 2, 9, 11, 1], ["15,45 9-17 * * 1-5", 45, 10, 12, 6, 3], ["15,45 9-17 * * 1-5", 45, 10, 12, 6, 0], ["0 0 1 1 *", 0, 0, 1, 1, 4], ["0 0 */2 * *", 0, 0, 3, 5, 2]], "Check each field in turn.", approx=None)]))

B.append(CH(
 "Go framework, migrations and the CLI",
 ("Go", [
  "pocketbase.New | creates | An app", "OnServe | registers | Routes", "CGO_ENABLED=0 | builds | A static binary", "Migrations | record | Schema changes",
  "pb_migrations | holds | Timestamped files", "migrate | applies | Pending migrations", "Superuser | is created | From the CLI"]),
 ["Instead of the prebuilt program you can import PocketBase into your own Go program. You call pocketbase.New, register routes and hooks, and build one static executable.",
  "Schema changes are stored as migration files in pb_migrations, named with a timestamp. When you change collections in the dashboard in development, PocketBase writes a migration for you.",
  "Everyday commands are serve, superuser create, migrate and update."],
 [("Go framework", "Using PocketBase as a Go library to build your own backend."), ("Migration", "A file that changes the schema in a repeatable way."), ("Auto migrate", "Writing migration files automatically when collections change."),
  ("CLI", "The command line: serve, superuser, migrate, update."), ("Static binary", "An executable with no outside dependencies."), ("Superuser create", "A command to make an admin account.")],
 ["Create main.go with pocketbase.New() and register routes inside app.OnServe().", "Build a static executable with CGO_ENABLED=0 go build, then run ./myapp serve.",
  "Migration files live in pb_migrations and are named TIMESTAMP_description.js (or .go).", "Applied migrations are recorded in the database so each runs once.", "./pocketbase superuser create EMAIL PASSWORD makes an admin.",
  "./pocketbase update updates the prebuilt executable."],
 [T("The prebuilt program is enough for most apps. Choose the Go route when you want to write your server logic in Go, or ship one custom executable. Both routes give the same collections, rules and API."),
  C("// main.go\npackage main\n\nimport (\n    \"log\"\n    \"net/http\"\n\n    \"github.com/pocketbase/pocketbase\"\n    \"github.com/pocketbase/pocketbase/core\"\n)\n\nfunc main() {\n    app := pocketbase.New()\n\n    app.OnServe().BindFunc(func(se *core.ServeEvent) error {\n        se.Router.GET(\"/hello\", func(e *core.RequestEvent) error {\n            return e.String(http.StatusOK, \"Hello world!\")\n        })\n        return se.Next()\n    })\n\n    if err := app.Start(); err != nil {\n        log.Fatal(err)\n    }\n}", "go"),
  T("The Go module path is shown in the Go documentation for your version, so copy the import lines from there. After go mod tidy you can run go run main.go serve, or build a single static executable with CGO_ENABLED=0 go build and copy it to a server."),
  T("A migration is a file in pb_migrations that changes the schema, for example to create a collection or add a field. Its name starts with a Unix timestamp so that they run in order, followed by a short description. Each file has an up function and a down function. PocketBase records which ones have run, so each is applied once."),
  T("When you work in the dashboard on your own machine, PocketBase can create these files for you whenever you change a collection. Commit them to git. On the production server the new files run on start, or with the migrate command, so the schema follows the code."),
  C("./pocketbase serve                       # run the server\n./pocketbase superuser create a@b.com pw   # create an admin\n./pocketbase migrate                       # apply pending migrations\n./pocketbase update                        # update the prebuilt binary\n./pocketbase --dir=./mydata serve          # use a different data folder", "bash")],
 [("How do you build a static Go executable?", ["CGO_ENABLED=0 go build", "go install", "go vet", "go run"], 0, "No cgo."),
  ("How are migration files named?", ["TIMESTAMP_description.js", "A random id", "The collection name", "A version number only"], 0, "They run in order."),
  ("Which command creates an admin?", ["superuser create", "admin add", "user new", "serve"], 0, "In 0.23 and later.")],
 [("Where do migrations live?", "pb_migrations."), ("What does OnServe do?", "Lets you add routes."), ("What does migrate do?", "Applies pending migrations."), ("What does update do?", "Updates the binary.")],
 [FILL("CLI", "Run ./pocketbase {{serve}} to start the server and ./pocketbase {{migrate}} to apply pending migrations."),
  PL("Read a migration name", "Write parse_migration(name): a file name like '1700000000_created_posts.js' gives [1700000000, 'created_posts'] (the timestamp as an integer, and the description without the .js or .go ending).",
     "parse_migration(name)", """
def parse_migration(name):
    ts, rest = name.split('_', 1)
    for ext in ('.js', '.go'):
        if rest.endswith(ext):
            rest = rest[:-len(ext)]
    return [int(ts), rest]
""", [["1700000000_created_posts.js"], ["1700000500_add_title_to_posts.go"], ["5_x.js"]], "Split at the first underscore.", approx=None),
  PL("Pending migrations", "Write pending(files, applied): return the sorted list of file names in files that are not in applied, ordered by their numeric timestamp prefix.",
     "pending(files, applied)", """
def pending(files, applied):
    todo = []
    for f in files:
        if f not in applied:
            todo.append([int(f.split('_', 1)[0]), f])
    todo.sort()
    return [t[1] for t in todo]
""", [[["1_a.js", "3_c.js", "2_b.js"], ["1_a.js"]], [["1_a.js"], ["1_a.js"]], [["10_x.js", "9_y.js"], []], [[], []]], "Sort by the number, not the text.", approx=None),
  PL("Schema diff", "Write schema_diff(old, new): old and new are lists of field names. Return [added, removed], each a sorted list: added are in new but not old, removed are in old but not new.",
     "schema_diff(old, new)", """
def schema_diff(old, new):
    added = []
    removed = []
    for f in new:
        if f not in old:
            added.append(f)
    for f in old:
        if f not in new:
            removed.append(f)
    return [sorted(added), sorted(removed)]
""", [[["title", "body"], ["title", "body", "tags"]], [["a", "b"], ["b"]], [[], ["x"]], [["a"], ["a"]]], "Compare in both directions.", approx=None)]))

B.append(CH(
 "Going to production",
 ("Production", [
  "Binary | runs | On a small server", "Reverse proxy | adds | HTTPS", "pb_data | needs | Backups", "Rate limiter | slows | Abuse",
  "Encryption key | protects | Settings", "File limit | allows | Many clients", "S3 | stores | Files and backups"]),
 ["Running PocketBase for real takes a few steps. Put it on a small server with a persistent pb_data folder, serve it over HTTPS, back it up, and turn on rate limiting.",
  "Built-in backups make a ZIP snapshot of pb_data and can run on a cron schedule, keeping the newest few. For a very large pb_data, use a different strategy such as an SQLite backup copy.",
  "The labs rotate backups and simulate a rate limiter."],
 [("Reverse proxy", "A web server in front of PocketBase, such as Nginx or Caddy."), ("Backup", "A copy of pb_data that you can restore."), ("cronMaxKeep", "How many scheduled backups to keep before removing older ones."),
  ("Rate limiter", "A rule that limits requests per time window."), ("Encryption key", "A secret used to encrypt the settings stored in the database."), ("Open file limit", "The operating system limit on simultaneous connections and files.")],
 ["Persist the pb_data folder; in Docker mount it as a volume.", "serve with a domain name can handle HTTPS with an automatic Let's Encrypt certificate, or put Nginx or Caddy in front.",
  "Backups are ZIP snapshots of pb_data and can be scheduled by cron, with cronMaxKeep controlling how many remain.", "Large data folders, about 2 GB or more, need a different backup plan.",
  "The built-in rate limiter takes rules with a label, max requests and duration.", "--encryptionEnv=NAME encrypts the settings with a key from an environment variable; never lose that key."],
 [T("PocketBase is a single process, so production is simple. A small virtual machine is enough for many apps. Scale up with a bigger machine, because SQLite lives on one server, and plan for that from the start."),
  T("Start with persistence. The pb_data folder holds the database and the uploaded files. On a server, keep it on a real disk, and in Docker mount a volume on it. Next, serve over HTTPS. You can start the program with your domain name and let it fetch a certificate, or put Nginx or Caddy in front of it as a reverse proxy."),
  C("# serve a domain over HTTPS with an automatic certificate\n./pocketbase serve yourdomain.com\n\n# or listen locally behind a reverse proxy\n./pocketbase serve --http=127.0.0.1:8090\n\n# encrypt settings with a key from the environment\nexport PB_ENCRYPTION_KEY=\"a-random-32-character-secret-key!\"\n./pocketbase serve --encryptionEnv=PB_ENCRYPTION_KEY", "bash"),
  T("Back up before you need to. The dashboard can create a snapshot, which is a ZIP of pb_data, and can schedule one with a cron expression, such as 0 0 * * *. The setting cronMaxKeep removes old ones. While a snapshot is created the app is briefly read-only. For a big data folder, a hot copy with the sqlite3 backup command plus rsync is gentler. Test restoring."),
  T("Protect the front door. The built-in rate limiter takes rules, each with a label, a maximum number of requests and a duration, and it can apply to a whole path, such as the sign-in route. Use strong passwords for superusers and turn on multi-factor authentication for them. Configure an SMTP server so that verification and reset emails are sent."),
  T("Many open realtime clients are many open connections. If you see too many open files errors, raise the file limit for the process. Setting GOMEMLIMIT gives Go a soft memory limit on a small server. If storage grows, move uploads to S3.")],
 [("What should be persisted?", ["pb_data", "pb_hooks only", "The binary", "Nothing"], 0, "Database and files."),
  ("What does a backup snapshot contain?", ["A ZIP of pb_data", "Only rules", "The SDK", "Logs only"], 0, "A full snapshot."),
  ("Why raise the open file limit?", ["Many realtime connections", "Faster sorting", "Bigger passwords", "More collections"], 0, "Each client is a connection.")],
 [("What is cronMaxKeep?", "How many backups to keep."), ("What encrypts settings?", "The encryption key."), ("Where does SQLite live?", "On one server."), ("What limits requests?", "The rate limiter.")],
 [MATCH("Production", "Match each setting with its purpose.", [("Reverse proxy", "HTTPS and routing"), ("cronMaxKeep", "Old backups removed"), ("Rate limiter", "Fewer abusive requests"), ("--encryptionEnv", "Encrypted settings")]),
  PL("Rotate backups", "Write rotate_backups(names, max_keep): names are backup file names that sort oldest first. Return the sorted list of names to delete so that only the newest max_keep remain.",
     "rotate_backups(names, max_keep)", """
def rotate_backups(names, max_keep):
    ordered = sorted(names)
    cut = len(ordered) - max_keep
    if cut <= 0:
        return []
    return ordered[:cut]
""", [[["b_20260103.zip", "b_20260101.zip", "b_20260102.zip"], 2], [["b_1.zip"], 3], [[], 1], [["b_3.zip", "b_1.zip", "b_2.zip", "b_4.zip"], 1]], "Sort, then drop the oldest.", approx=None),
  PL("Rate limiter", "Write rate_limit(times, max_requests, duration): times is the list of request times in seconds, in order. Use fixed windows: window = time // duration. Return a list of booleans, true when the request is allowed (the count in its window, including this one, is at most max_requests).",
     "rate_limit(times, max_requests, duration)", """
def rate_limit(times, max_requests, duration):
    counts = {}
    out = []
    for t in times:
        w = t // duration
        counts[w] = counts.get(w, 0) + 1
        out.append(counts[w] <= max_requests)
    return out
""", [[[0, 1, 2, 3], 2, 10], [[0, 5, 10, 11, 12], 2, 10], [[], 5, 60], [[1, 1, 1], 1, 5]], "Count requests per window.", approx=None)]))

B.append(CH(
 "Designing an app and knowing the limits",
 ("Design", [
  "Notes app | uses | Auth and rules", "Owner field | links | Record and user", "Create rule | forces | Owner is me", "Update rule | blocks | Owner changes",
  "SQLite | limits | One writer", "Pre-1.0 | means | Read release notes", "Alternatives | scale | Beyond one server"]),
 ["A good PocketBase app is mostly collections and rules. Take a notes app: a notes collection with an owner relation to users, and rules that let each person see and change only their own notes.",
  "PocketBase fits small and medium apps, prototypes, internal tools and mobile backends well. It is less suited to apps that need many servers writing at once.",
  "The last labs audit rules and tie the course together."],
 [("Owner field", "A relation to users that marks who owns a record."), ("Least privilege", "Giving each action only the access it needs."), ("Vertical scaling", "Making one server bigger instead of adding more."),
  ("Single writer", "SQLite lets one write happen at a time."), ("Audit", "Reviewing rules for actions that are too open."), ("Pre-1.0", "Not yet stable: changes may break things.")],
 ["Start with all rules locked and open each action as narrowly as possible.", "Ownership pattern: author = @request.auth.id for list, view, update and delete.", "Create rule: @request.auth.id != \"\" && @request.body.author = @request.auth.id.",
  "Block ownership changes with @request.body.author:changed = false.", "SQLite handles many readers and one writer at a time; scale up one server first.", "Before upgrading, read the release notes and test a copy of pb_data."],
 [T("Let us design a notes app from start to finish. You need two collections. The users collection already exists as an auth collection. Add a notes collection with a title text field, a body editor field and an owner relation field that points to users."),
  T("Now the rules. Leave them all locked and open them one by one. Listing and viewing should show only your own notes, so the rule is owner = @request.auth.id. Creating should require sign-in and force the new note to be yours. Updating should let the owner edit but not hand the note to someone else. Deleting should be owner only."),
  C("// notes collection rules\nlistRule:   owner = @request.auth.id\nviewRule:   owner = @request.auth.id\ncreateRule: @request.auth.id != \"\" && @request.body.owner = @request.auth.id\nupdateRule: owner = @request.auth.id && @request.body.owner:changed = false\ndeleteRule: owner = @request.auth.id", "text"),
  T("Add realtime and the owner's open screens stay in sync with no extra code, because the list rule decides which events each client sees. Add a file field and attachments work, with the same rules."),
  T("Know the limits. SQLite allows many readers but a single writer at a time, so an app with very heavy parallel writes will hit a ceiling, and you cannot spread one database over many servers. For most apps a well-sized single server goes a very long way. If you outgrow it you can still move the data elsewhere."),
  T("Also remember the version. PocketBase is pre-1.0, with breaking changes allowed. Pin the version in your deployment, read the release notes, keep migrations in git, and test an upgrade on a copy of pb_data first. With those habits you have a backend that is small, fast to build on, and easy to run.")],
 [("What is the ownership list rule?", ["owner = @request.auth.id", "\"\"", "null", "@request.method = \"GET\""], 0, "Match the signed-in user."),
  ("What stops a user giving a note away?", ["@request.body.owner:changed = false", "A locked list rule", "A larger perPage", "A view collection"], 0, "Block changing the owner."),
  ("What limits SQLite writes?", ["One writer at a time", "Two writers", "No limit", "Only five users"], 0, "A single writer.")],
 [("How should rules start?", "Locked, then opened narrowly."), ("What does :changed check?", "Whether a field was changed."), ("How do you scale?", "Vertically first."), ("What should you test before upgrading?", "A copy of pb_data.")],
 [MATCH("Design", "Match each need with the tool.", [("Only the owner may edit", "updateRule with owner = @request.auth.id"), ("Block giving away a note", "@request.body.owner:changed = false"), ("Live updates", "Realtime subscriptions"), ("Schema in git", "Migrations")]),
  PL("Open write rules", "Write open_writes(rules): rules is a dict of action to rule value (None for locked, a string otherwise). Return the sorted list of the write actions create, update and delete whose rule is the empty string (open to anyone).",
     "open_writes(rules)", """
def open_writes(rules):
    out = []
    for action in ('create', 'update', 'delete'):
        if action in rules and rules[action] == '':
            out.append(action)
    return sorted(out)
""", [[{"list": "", "create": "", "update": None, "delete": ""}], [{"create": "@request.auth.id != \"\""}], [{}], [{"update": "", "delete": ""}]], "Look at the write actions only.", approx=None),
  PL("Ownership rule", "Write ownership_rule(field): return the update rule that lets only the owner edit and blocks changing the owner field, exactly: FIELD = @request.auth.id && @request.body.FIELD:changed = false (with FIELD replaced).",
     "ownership_rule(field)", """
def ownership_rule(field):
    return field + ' = @request.auth.id && @request.body.' + field + ':changed = false'
""", [["owner"], ["author"], ["user"]], "Join the pieces.", approx=None),
  PL("Lock check", "Write is_locked(rule, is_superuser): true when a normal user is denied. A null rule (None) denies a normal user; an empty string never denies; any other rule is conditional so return false. Superusers are never denied.",
     "is_locked(rule, is_superuser)", """
def is_locked(rule, is_superuser):
    if is_superuser:
        return False
    return rule is None
""", [[None, False], [None, True], ["", False], ["owner = @request.auth.id", False]], "Only null locks.", approx=None)]))
