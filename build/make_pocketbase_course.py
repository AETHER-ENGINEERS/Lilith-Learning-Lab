#!/usr/bin/env python3
"""Build the PocketBase course. Usage: python3 make_pocketbase_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "pbc"))
import cmk, pb1, pb2  # noqa: E402

PRONOUNCE = {
    "PocketBase": "pocket base", "pb_data": "P B data", "pb_hooks": "P B hooks", "pb_public": "P B public", "pb_migrations": "P B migrations", "SQLite": "S Q L ite", "SQL": "S Q L", "REST": "rest",
    "API": "A P I", "SSE": "S S E", "JWT": "J W T", "OAuth2": "O auth two", "OTP": "O T P", "MFA": "M F A", "JSON": "jason", "HTTPS": "H T T P S", "HTTP": "H T T P", "CORS": "cors", "SDK": "S D K",
    "S3": "S three", "SMTP": "S M T P", "TLS": "T L S", "CLI": "C L I", "ELI5": "E L I five", "goja": "go ya", "Go": "go", "cron": "cron", "cronMaxKeep": "cron max keep", "JavaScript": "java script",
    "Nginx": "engine x", "Caddy": "caddy", "Docker": "docker", "systemd": "system D", "rsync": "R sync", "sqlite3": "S Q L ite three", "GOMEMLIMIT": "go mem limit", "UTC": "U T C", "ES5": "E S five",
    "Dockerfile": "docker file", "CRUD": "crud", "ID": "I D", "id": "I D", "URL": "U R L", "ZIP": "zip", "MIME": "mime", "WxH": "W by H", "authWithPassword": "auth with password", "authStore": "auth store",
    "getList": "get list", "getFullList": "get full list", "getOne": "get one", "getFirstListItem": "get first list item", "routerAdd": "router add", "cronAdd": "cron add", "onRecordCreate": "on record create",
    "e.next": "E dot next", "pb.filter": "P B dot filter", "pb.collection": "P B dot collection", "listRule": "list rule", "viewRule": "view rule", "createRule": "create rule", "updateRule": "update rule", "deleteRule": "delete rule",
    "@request.auth": "at request dot auth", "@request.body": "at request dot body", "_superusers": "underscore superusers", "Let's Encrypt": "lets encrypt", "ES": "E S", "TLS ": "T L S ", "pb": "P B",
}

SANDBOX = cmk.terminal("PocketBase cheat sheet", "pb>", "A scripted lookup, not a real server. Try: serve, superuser, rules, filter, sdk, realtime, hooks, backup", [
    ("serve", ["./pocketbase serve  (default 127.0.0.1:8090)", "dashboard /_/   api /api/   data pb_data"]),
    ("superuser", ["./pocketbase superuser create EMAIL PASSWORD", "superusers bypass every API rule"]),
    ("rules", ["null = superusers only, \"\" = anyone, expression = condition", "list: 200 empty, create: 400, view/update/delete: 404, locked: 403"]),
    ("filter", ["title ~ 'abc' && created > '2022-01-01'", "pb.filter('x = {:v}', { v }) escapes values"]),
    ("sdk", ["const pb = new PocketBase(url)", "pb.collection('posts').getList(1, 20, { filter, sort, expand })"]),
    ("realtime", ["pb.collection('posts').subscribe('*', cb)", "events: create, update, delete (respect view rules)"]),
    ("hooks", ["pb_hooks/main.pb.js: routerAdd, onRecordCreate, cronAdd", "call e.next() to continue the chain"]),
    ("backup", ["ZIP snapshot of pb_data; cron + cronMaxKeep", "large data: sqlite3 .backup + rsync"]),
])

EXAM = [
 ("What is PocketBase?", ["An open source backend in one executable", "A frontend framework", "A cloud database service only", "A CSS library"], 0, "Written in Go."),
 ("Which database does it embed?", ["SQLite", "PostgreSQL", "Redis", "MongoDB"], 0, "A single file."),
 ("Where is the dashboard by default?", ["/_/", "/admin/", "/api/", "/dash"], 0, "Underscore slash."),
 ("Which folder holds the database and uploads?", ["pb_data", "pb_hooks", "pb_public", "pb_migrations"], 0, "Back it up."),
 ("What are the three collection types?", ["Base, auth, view", "Table, row, column", "Public, private, admin", "Text, number, bool"], 0, "Types of collection."),
 ("Which collection type is read-only?", ["View", "Base", "Auth", "System"], 0, "A SQL query."),
 ("How long is the default record id?", ["15 characters", "5", "36", "64"], 0, "Lowercase letters and digits."),
 ("Which verb partially updates a record?", ["PATCH", "GET", "POST", "TRACE"], 0, "Partial update."),
 ("What does sort=-created mean?", ["Newest first", "Oldest first", "Random", "By id"], 0, "Descending."),
 ("What does expand do?", ["Loads related records", "Makes pages bigger", "Sorts records", "Encrypts fields"], 0, "In record.expand."),
 ("Why use pb.filter with placeholders?", ["To escape values safely", "Speed", "Sorting", "Caching"], 0, "Prevents filter injection."),
 ("What does getFullList do?", ["Fetches every record in pages", "Fetches one page", "Deletes all", "Counts"], 0, "Slow for big sets."),
 ("What does a null rule mean?", ["Only superusers", "Anyone", "Only owners", "Disabled"], 0, "The default."),
 ("What does an empty string rule mean?", ["Anyone", "Locked", "Admins only", "Signed in"], 0, "Fully open."),
 ("What status does a failed list rule give?", ["200 with an empty list", "403", "404", "500"], 0, "No records match."),
 ("What status does a locked rule give a normal user?", ["403", "200", "404", "400"], 0, "Forbidden."),
 ("Which rule blocks changing the owner field?", ["@request.body.owner:changed = false", "owner = \"\"", "null", "@request.method = 'GET'"], 0, "The :changed modifier."),
 ("Who bypasses API rules?", ["Superusers", "Verified users", "Everyone", "Nobody"], 0, "Admins."),
 ("Where does the client send its token?", ["The Authorization header", "The URL path", "A cookie only", "The body only"], 0, "SDK does it."),
 ("What does requestOTP return?", ["An otpId", "A password", "A token", "A file"], 0, "Even for unknown emails."),
 ("Which collection does not support OAuth2?", ["_superusers", "users", "any auth collection", "view"], 0, "A documented caveat."),
 ("What does a relation field store?", ["Record ids", "Whole records", "SQL", "Hashes"], 0, "Ids only."),
 ("What does cascadeDelete true do?", ["Removes dependent records", "Blocks deletion", "Copies", "Nothing"], 0, "On parent delete."),
 ("What does realtime use?", ["Server-Sent Events", "Polling only", "Email", "FTP"], 0, "One way."),
 ("What does subscribe('*') follow?", ["All records in the collection", "One record", "Only creates", "Only deletes"], 0, "The star topic."),
 ("Which event carries the client id?", ["PB_CONNECT", "create", "update", "delete"], 0, "The first event."),
 ("Where are uploaded files stored by default?", ["Under pb_data", "In the record JSON", "In pb_hooks", "In memory"], 0, "Or S3."),
 ("What does ?thumb=100x100 do?", ["Returns a resized image", "Deletes the image", "Zips the file", "Lists files"], 0, "Allowed sizes only."),
 ("Where do JavaScript hooks live?", ["pb_hooks/*.pb.js", "pb_public", "pb_data", "Anywhere"], 0, "Next to the executable."),
 ("What stops a hook chain?", ["Throwing or not calling e.next()", "Calling e.next()", "Returning", "Logging"], 0, "Both stop it."),
 ("Which engine runs the hooks?", ["goja", "V8", "Node", "Bun"], 0, "A Go interpreter."),
 ("How do you build a static Go executable?", ["CGO_ENABLED=0 go build", "go vet", "go fmt", "go get"], 0, "No cgo."),
 ("How are migrations named?", ["TIMESTAMP_description.js", "Random ids", "The collection id", "alphabetical"], 0, "Run in order."),
 ("What does cronMaxKeep control?", ["How many scheduled backups remain", "Cron speed", "File size", "Logs"], 0, "Old ones are removed."),
 ("Why raise the open file limit?", ["Many realtime connections", "Faster SQL", "More fields", "Bigger ids"], 0, "Each client is a connection."),
 ("What limits SQLite scaling?", ["One writer at a time", "No readers", "Memory only", "Port numbers"], 0, "Scale vertically first."),
]

CFG = dict(id="pocketbase-backend-in-one-file", title="PocketBase: A Backend in One File", subtitle="Collections, rules, auth, realtime, files, hooks and production, with Python labs that rebuild the ideas",
    description="Learn PocketBase, the open source Go backend with an embedded SQLite database. You will design collections and fields, use the records API and the JavaScript SDK, write API rules and filters, sign users in with passwords, OAuth2 and one-time codes, expand relations, subscribe to realtime events, handle files, extend the server with JavaScript hooks and Go, manage migrations, and run it in production with backups and rate limits. Each chapter has an ELI5 block and Python labs.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="pbc", apps={})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "pocketbase-backend-in-one-file.course.json")
    cmk.main(CFG, pb1.A + pb2.B, [sys.argv[0], out])
