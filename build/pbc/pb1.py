"""PocketBase course, chapters 1-7."""
import sys, os, json, base64
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

A = []

A.append(CH(
 "What PocketBase is",
 ("PocketBase", [
  "PocketBase | is | One executable", "Executable | embeds | SQLite", "Executable | serves | REST and realtime API", "Executable | serves | Admin dashboard",
  "pb_data | holds | Database and files", "pb_hooks | holds | JavaScript extensions", "pb_public | holds | Static files"]),
 ["PocketBase is an open source backend in a single file. It is written in Go and uses an embedded SQLite database.",
  "One program gives you a database, a REST style API, realtime updates, user accounts, file storage and an admin dashboard. You start it with serve.",
  "It is still before version 1.0, so details can change between releases."],
 [("Backend", "The server side of an app: data, accounts, rules."), ("Embedded database", "A database that runs inside your program instead of a separate server."), ("SQLite", "A small database stored in one file."),
  ("Dashboard", "The admin web page, served at /_/."), ("Superuser", "An admin account that bypasses all access rules."), ("pb_data", "The folder where PocketBase keeps its database and uploaded files.")],
 ["PocketBase is open source, written in Go and MIT licensed.", "It bundles SQLite, a REST style API, realtime subscriptions, auth, files and a dashboard.", "Run it with ./pocketbase serve; the default address is 127.0.0.1:8090.",
  "The dashboard is at /_/ and the API is under /api/.", "Folders next to the program: pb_data, pb_public, pb_hooks and pb_migrations.", "It is pre-1.0, so read the release notes before upgrading."],
 [T("Most apps need the same few things from a backend: somewhere to store data, a way to sign users in, rules about who can see what, a way to upload files, and a way to push changes to open screens. Normally that is a database server, an auth service, a file store and glue code."),
  T("PocketBase puts all of it in one downloadable program. You download a file, unzip it, and run it. It creates a SQLite database on disk, opens a web server, and gives you a dashboard in the browser where you design your data."),
  C("./pocketbase serve\n# API:       http://127.0.0.1:8090/api/\n# Dashboard: http://127.0.0.1:8090/_/\n./pocketbase superuser create admin@example.com 'a-long-password'", "bash"),
  T("Next to the program PocketBase uses a few folders. The pb_data folder holds the SQLite database and uploaded files, so it is the one that matters for backups. The pb_hooks folder holds JavaScript files that extend the server. The pb_migrations folder holds schema changes as code. Files in pb_public are served as a static website."),
  T("You can also use PocketBase as a Go library and build your own program around it. The prebuilt program already includes a JavaScript engine for hooks. Both routes give the same core: collections, rules, auth, realtime and files."),
  T("Be aware of the version. PocketBase is still below 1.0 and its authors say backward compatibility is not guaranteed before then. Version 0.23 made large changes, for example admins became superusers. Always read the release notes, and the program can update itself with ./pocketbase update.")],
 [("Which database does PocketBase embed?", ["SQLite", "PostgreSQL", "MySQL", "MongoDB"], 0, "It is one file on disk."),
  ("Where is the admin dashboard by default?", ["/_/", "/admin", "/api/", "/dashboard"], 0, "Underscore slash."),
  ("Which folder should you back up?", ["pb_data", "pb_public", "pb_hooks only", "None"], 0, "Database and uploads.")],
 [("What does serve do?", "Starts the web server."), ("What is the default address?", "127.0.0.1:8090."), ("What are superusers?", "Admins that bypass rules."), ("Is PocketBase 1.0 yet?", "No, pre-1.0.")],
 [MATCH("Folders", "Match each folder with what it holds.", [("pb_data", "Database and uploaded files"), ("pb_hooks", "JavaScript extensions"), ("pb_migrations", "Schema changes as code"), ("pb_public", "Static website files")]),
  PL("Route kind", "Write route_kind(path): return 'dashboard' if the path is /_ or starts with /_/, 'api' if it starts with /api/, otherwise 'static'.",
     "route_kind(path)", """
def route_kind(path):
    if path == '/_' or path.startswith('/_/'):
        return 'dashboard'
    if path.startswith('/api/'):
        return 'api'
    return 'static'
""", [["/_/"], ["/_/#/collections"], ["/api/collections/posts/records"], ["/index.html"], ["/"], ["/apiary"]], "Check the prefixes in order.", approx=None),
  PL("Serve flags", "Write parse_serve(args): args is a list like ['serve', '--http=0.0.0.0:8080', '--dir=./mydata']. Return [http, dir], using the defaults '127.0.0.1:8090' and 'pb_data' when a flag is missing.",
     "parse_serve(args)", """
def parse_serve(args):
    http = '127.0.0.1:8090'
    d = 'pb_data'
    for a in args:
        if a.startswith('--http='):
            http = a[7:]
        elif a.startswith('--dir='):
            d = a[6:]
    return [http, d]
""", [[["serve"]], [["serve", "--http=0.0.0.0:8080"]], [["--dir=./mydata", "serve"]], [["serve", "--http=:80", "--dir=/data"]]], "Strip each prefix.", approx=None)]))

A.append(CH(
 "Collections and fields",
 ("Collections", [
  "Collection | is | A table", "Base | stores | Ordinary data", "Auth | stores | Accounts", "View | is | A read-only SQL query",
  "Record | is | A row", "Field | has | A type", "Index | speeds | Filters"]),
 ["A collection is a table of records, and each record has fields. There are three types of collection: base for ordinary data, auth for accounts that can sign in, and view for a read-only result of a SQL query.",
  "Every record has an id, created and updated. Fields have types such as text, number, bool, email, url, date, select, file, relation, json and password.",
  "The lab checks records against a field list."],
 [("Collection", "A named set of records, backed by a SQLite table."), ("Record", "One row in a collection."), ("Base collection", "The default type for general data."),
  ("Auth collection", "A base collection with sign-in features."), ("View collection", "A read-only collection defined by a SQL query."), ("Relation", "A field that points to a record in another collection.")],
 ["Collections are backed by plain SQLite tables.", "Base, auth and view are the three collection types.", "Every record has id, created and updated.",
  "The default id is a 15 character string of lowercase letters and digits.", "Auth collections add email, password, verified and token fields.", "View collections never get create, update or delete, and send no realtime events."],
 [T("Think of a collection as a spreadsheet tab. The columns are fields and the rows are records. Under the hood PocketBase creates a real SQLite table for each collection, so everything you know about SQL indexes and constraints still applies."),
  T("The base type is the default. Use it for posts, products, orders and anything else. Each record automatically has an id, which is a 15 character random string, plus created and updated times."),
  T("The auth type extends base with what a sign-in needs: an email, a password, a verified flag and a token key. Your own users usually live in an auth collection called users, which exists by default. Superusers live in a special system collection called _superusers."),
  T("The view type is different. You give it a SQL query, for example a join that counts comments per post, and it behaves like a read-only collection. You can list and view it, and apply rules, but you cannot create, update or delete, and it sends no realtime events."),
  C("// a collection created from JavaScript (inside a migration)\nconst posts = new Collection({\n  type: \"base\",\n  name: \"posts\",\n  listRule: \"\",\n  viewRule: \"\",\n  createRule: \"@request.auth.id != ''\",\n  fields: [\n    { name: \"title\", type: \"text\", required: true, max: 120 },\n    { name: \"published\", type: \"bool\" },\n  ],\n})\n$app.save(posts)", "javascript"),
  T("Fields have types: text, editor for rich text, number, bool, email, url, date, select, file, relation, json, password and geoPoint, among others. Each type has its own options, such as required, a maximum length, or the allowed values of a select. Add indexes on the fields you filter and sort by, in the same way you would in any SQL database.")],
 [("How many collection types are there?", ["Three: base, auth, view", "Two", "Four", "One"], 0, "Base, auth and view."),
  ("Which collection type is read-only?", ["View", "Base", "Auth", "System"], 0, "Defined by SQL."),
  ("What does a relation field store?", ["The id of a record in another collection", "A file", "A password", "A SQL query"], 0, "A reference.")],
 [("What is a record?", "One row in a collection."), ("What backs a collection?", "A SQLite table."), ("What does an auth collection add?", "Email, password, verified."), ("Which type has a SQL query?", "View.")],
 [FILL("Types", "The three collection types are {{base}}, {{auth}} and {{view}}."),
  PL("Valid names", "Write valid_name(name): a collection name is valid when it is not empty and uses only letters, digits and underscores.",
     "valid_name(name)", """
def valid_name(name):
    if not name:
        return False
    for ch in name:
        if not (ch.isalpha() or ch.isdigit() or ch == '_'):
            return False
    return True
""", [["posts"], ["blog_posts"], ["my-posts"], [""], ["a b"], ["users2"]], "Check each character.", approx=None),
  PL("Valid ids", "Write valid_id(s): true when s is exactly 15 characters, each a lowercase letter a to z or a digit.",
     "valid_id(s)", """
def valid_id(s):
    if len(s) != 15:
        return False
    for ch in s:
        if not (('a' <= ch <= 'z') or ('0' <= ch <= '9')):
            return False
    return True
""", [["abc123def456ghi"], ["ABC123def456ghi"], ["short"], ["abc123def456gh!"], [""]], "Length first, then characters.", approx=None),
  PL("Validate a record", "Write validate(fields, record): fields is a list of [name, type, required] with type 'text', 'number' or 'bool'. record is a dict. Return the sorted list of error strings: 'name: required' when a required field is missing or empty, or 'name: wrong type' when present but not the right kind (a bool is not a number).",
     "validate(fields, record)", """
def validate(fields, record):
    errors = []
    for name, kind, req in fields:
        if name not in record or record[name] is None or record[name] == '':
            if req:
                errors.append(name + ': required')
            continue
        v = record[name]
        if kind == 'text':
            ok = isinstance(v, str)
        elif kind == 'number':
            ok = isinstance(v, (int, float)) and not isinstance(v, bool)
        else:
            ok = isinstance(v, bool)
        if not ok:
            errors.append(name + ': wrong type')
    return sorted(errors)
""", [[[["title", "text", True], ["views", "number", False]], {"title": "Hi", "views": 3}], [[["title", "text", True]], {}], [[["views", "number", False]], {"views": True}], [[["ok", "bool", True], ["t", "text", True]], {"ok": False, "t": 5}]], "Loop over the fields.", approx=None)]))

A.append(CH(
 "The records API",
 ("Records API", [
  "List | returns | A page of records", "View | returns | One record", "Create | adds | A record", "Update | changes | A record",
  "Delete | removes | A record", "Filter | narrows | The list", "Expand | loads | Related records"]),
 ["Every collection gets a REST style API automatically. You list, view, create, update and delete records under /api/collections/NAME/records.",
  "A list call returns a page: page, perPage, totalItems, totalPages and items. You can pass sort, filter, expand and fields to shape the result.",
  "The labs compute page counts and parse sort strings."],
 [("Pagination", "Returning a long list in pages."), ("perPage", "How many records come back in one page."), ("Sort", "The order of results, such as -created for newest first."),
  ("Filter", "An expression that keeps only matching records."), ("Expand", "A query option that loads related records inside the response."), ("Fields", "A query option that returns only some fields.")],
 ["List is GET /api/collections/NAME/records; view adds /ID.", "Create is POST, update is PATCH, delete is DELETE.", "A page response has page, perPage, totalItems, totalPages and items.",
  "sort=-created,title sorts newest first, then by title.", "filter takes an expression like title ~ 'abc' && created > '2022-01-01'.", "Which records you may touch depends on the collection's API rules."],
 [T("When you add a collection, PocketBase already exposes its API. There is nothing to write. The dashboard even has an API preview tab that shows the exact calls for your collection."),
  C("GET    /api/collections/posts/records?page=1&perPage=20&sort=-created\nGET    /api/collections/posts/records/RECORD_ID\nPOST   /api/collections/posts/records\nPATCH  /api/collections/posts/records/RECORD_ID\nDELETE /api/collections/posts/records/RECORD_ID", "http"),
  T("A list call returns an object with the page number, the page size, the total count, the number of pages, and the items. Use page and perPage to walk through the list. Sort is a comma separated list of field names, and a minus sign means descending."),
  T("The filter option takes a filter expression. The syntax is the same one used in API rules, which you will meet in chapter 5. The expand option asks PocketBase to load related records so that you do not need a second request. The fields option trims the response to the fields you name."),
  T("Create and update accept JSON, or multipart form data when files are included. Update is a partial change: only the fields you send are modified. Delete returns an empty success response. Whether any of these calls is allowed depends on the rule for that action."),
  T("You will use these calls through the SDK in the next chapter, but they are plain HTTP, so any language can call them, including curl.")],
 [("Which verb updates a record?", ["PATCH", "GET", "PUT only", "OPTIONS"], 0, "Partial update."),
  ("What does sort=-created do?", ["Newest first", "Oldest first", "Random", "Alphabetical"], 0, "Minus means descending."),
  ("What does expand do?", ["Loads related records in the response", "Makes the page bigger", "Sorts", "Deletes"], 0, "Saves a second request.")],
 [("What does totalPages tell you?", "How many pages exist."), ("Which verb creates?", "POST."), ("What is fields for?", "Trimming the response."), ("Where do rules come in?", "Each action has one.")],
 [MATCH("Calls", "Match each call with what it does.", [("GET /records", "List a page"), ("GET /records/ID", "View one record"), ("POST /records", "Create"), ("DELETE /records/ID", "Delete")]),
  PL("Total pages", "Write total_pages(total, per): the number of pages needed for total items at per items per page. Zero items still give 0 pages.",
     "total_pages(total, per)", """
def total_pages(total, per):
    return (total + per - 1) // per
""", [[0, 20], [1, 20], [20, 20], [21, 20], [101, 30]], "Round up the division.", approx=None),
  PL("One page", "Write page_of(items, page, per): the items on the given 1-based page. Return an empty list past the end.",
     "page_of(items, page, per)", """
def page_of(items, page, per):
    start = (page - 1) * per
    return items[start:start + per]
""", [[[1, 2, 3, 4, 5], 1, 2], [[1, 2, 3, 4, 5], 3, 2], [[1, 2, 3, 4, 5], 4, 2], [[], 1, 10]], "Slice from (page minus 1) times per.", approx=None),
  PL("Parse sort", "Write parse_sort(s): turn 'a,-b' into [['a', 'asc'], ['b', 'desc']]. Ignore empty parts.",
     "parse_sort(s)", """
def parse_sort(s):
    out = []
    for part in s.split(','):
        part = part.strip()
        if not part:
            continue
        if part.startswith('-'):
            out.append([part[1:], 'desc'])
        else:
            out.append([part, 'asc'])
    return out
""", [["-created"], ["title"], ["-created,title"], ["a,,b"], [""]], "A leading minus means descending.", approx=None)]))

A.append(CH(
 "The JavaScript SDK",
 ("SDK", [
  "pb | is | The client", "collection | selects | A collection", "getList | fetches | A page", "getFullList | fetches | Everything",
  "pb.filter | binds | Safe values", "authStore | keeps | The token", "SDK | works in | Browser and Node"]),
 ["The official JavaScript SDK works in browsers, Node.js and React Native. You create a client with new PocketBase(url) and then work through pb.collection(name).",
  "The common calls are getList, getFullList, getOne, getFirstListItem, create, update and delete.",
  "Never paste user input into a filter string. Use pb.filter with placeholders so values are escaped."],
 [("SDK", "A library that wraps the HTTP API."), ("getList", "Fetches one page of records."), ("getFullList", "Fetches every record by requesting pages in a loop."),
  ("getFirstListItem", "Fetches the first record matching a filter."), ("authStore", "Where the SDK keeps the sign-in token and record."), ("Placeholder", "A named slot like {:name} that is filled with an escaped value.")],
 ["Install with npm install pocketbase, or import it as an ES module in a browser.", "pb.collection('posts').getList(1, 20, { filter, sort, expand }) returns one page.",
  "getFullList loops through pages for you, so use it only for small collections.", "getFirstListItem fetches one record and errors if none matches.", "pb.filter('title = {:t}', { t }) escapes and binds values.", "The authStore saves the token and updates after sign-in."],
 [C("import PocketBase from 'pocketbase';\nconst pb = new PocketBase('http://127.0.0.1:8090');\n\nconst page = await pb.collection('posts').getList(1, 20, {\n  filter: pb.filter('title ~ {:q} && published = true', { q: 'lorem' }),\n  sort: '-created',\n  expand: 'author',\n});\nconsole.log(page.totalItems, page.items);\n\nconst post = await pb.collection('posts').create({ title: 'Hello' });\nawait pb.collection('posts').update(post.id, { title: 'Hello again' });\nawait pb.collection('posts').delete(post.id);", "javascript"),
  T("The client keeps one connection setting, the address of the server. Every call goes through pb.collection with the collection name. Methods return promises, so you use await."),
  T("The getList call returns a page object with items and counts. The getFullList call fetches every record by requesting pages in a loop. That is convenient but slow for a large collection, so prefer getList with a real filter. The getFirstListItem call is handy when you expect exactly one match, for example a record found by a unique slug."),
  T("Filters need care. If you build a filter by joining a string with user input, a quote in the input can change the meaning of the filter, in the same way SQL injection does. The pb.filter helper takes a template with placeholders like {:q} and a values object, and it escapes each value."),
  T("The SDK also keeps the signed-in user in pb.authStore, which holds the token and the record and can be saved in local storage. You will use it in the next chapters. In a browser, the SDK cancels an older request when you send a new identical one, which you can turn off with autoCancellation.")],
 [("Why use pb.filter?", ["It escapes values", "It is faster", "It sorts", "It logs in"], 0, "Prevents filter injection."),
  ("Which call fetches every record?", ["getFullList", "getOne", "getList", "create"], 0, "It loops over pages."),
  ("Where is the sign-in token kept?", ["pb.authStore", "pb.files", "A cookie only", "The collection"], 0, "The auth store.")],
 [("What creates a client?", "new PocketBase(url)."), ("What does getFirstListItem do?", "Gets one matching record."), ("What is a placeholder?", "{:name} slot."), ("Is the SDK Node only?", "No, also browsers.")],
 [FILL("SDK", "You create the client with new {{PocketBase}}(url) and call pb.{{collection}}('posts').getList(1, 20)."),
  PL("Bind values", "Write pb_filter(tpl, params): replace each {:name} in tpl with the value from params. Strings become single-quoted with any single quote escaped as \\' ; booleans become true or false; null (None) becomes null; numbers are written as they are. Leave unknown placeholders unchanged.",
     "pb_filter(tpl, params)", """
def pb_filter(tpl, params):
    out = ''
    i = 0
    while i < len(tpl):
        if tpl[i:i + 2] == '{:':
            j = tpl.find('}', i)
            if j > 0:
                name = tpl[i + 2:j]
                if name in params:
                    v = params[name]
                    if v is None:
                        out += 'null'
                    elif v is True:
                        out += 'true'
                    elif v is False:
                        out += 'false'
                    elif isinstance(v, str):
                        out += "'" + v.replace("'", "\\\\'") + "'"
                    else:
                        out += str(v)
                else:
                    out += tpl[i:j + 1]
                i = j + 1
                continue
        out += tpl[i]
        i += 1
    return out
""", [["title = {:t}", {"t": "hello"}], ["title = {:t}", {"t": "it's"}], ["a = {:n} && b = {:f}", {"n": 5, "f": True}], ["x = {:v}", {"v": None}], ["x = {:y}", {}], ["{:a}{:b}", {"a": "1", "b": 2.5}]], "Scan for {: and read up to }.", approx=None),
  PL("Requests for a full list", "Write requests_needed(total, batch): how many requests getFullList makes for total records with the given batch size. It always makes at least one.",
     "requests_needed(total, batch)", """
def requests_needed(total, batch):
    n = (total + batch - 1) // batch
    return max(1, n)
""", [[0, 500], [1, 500], [500, 500], [501, 500], [1200, 200]], "Round up, but never below one.", approx=None)]))

A.append(CH(
 "API rules: who can do what",
 ("Rules", [
  "Each collection | has | Five rules", "null | means | Superusers only", "Empty string | means | Anyone", "Expression | filters | Requests and records",
  "Superusers | bypass | All rules", "@request | reads | The current request", "@collection | reaches | Other collections"]),
 ["API rules are access control and a record filter at once. Each collection has five: listRule, viewRule, createRule, updateRule and deleteRule. Auth collections also have a manage rule.",
  "A rule can be null, which locks the action to superusers, an empty string, which lets anyone in, or an expression that must be true. Superusers always bypass rules.",
  "The labs check rule outcomes and run a small rule evaluator."],
 [("API rule", "A filter expression that decides who may do an action."), ("Locked rule", "A null rule: only superusers may act."), ("Open rule", "An empty string: anyone may act."),
  ("@request.auth", "The signed-in record making the request."), ("@request.body", "The data submitted with the request."), ("Modifier", "A suffix such as :isset, :changed, :length or :each.")],
 ["null means locked, an empty string means open, and an expression means conditional.", "A failed list rule returns an empty list with status 200; a failed create rule returns 400.",
  "A failed view, update or delete rule returns 404; a locked rule for a non-superuser returns 403.", "@request.auth.id != \"\" means a signed-in user.", "@request.body.role:isset = false blocks sending a role field.", "Rules also act as filters: a list rule of status = 'active' returns only active records."],
 [T("Rules are the heart of PocketBase security. By default every rule is null, which means locked: only superusers can use the API. You open actions one at a time, as narrowly as you can."),
  T("A rule is a filter expression. It is evaluated for the request. For list it works as a filter on the records. For view, update and delete it decides whether the record is visible. For create it decides whether the data may be added. Superusers skip all of it."),
  T("The failure codes tell clients what happened. An unmet list rule returns an empty list with status 200, because to the list the records are simply not there. An unmet create rule returns 400. An unmet view, update or delete rule returns 404, as if the record did not exist. A locked rule returns 403 to anyone who is not a superuser."),
  C("// only signed-in users may list, and they see only their own posts\nlistRule:   @request.auth.id != \"\" && author = @request.auth.id\n// anyone may read published posts\nviewRule:   published = true\n// only signed-in users may create, and only as themselves\ncreateRule: @request.auth.id != \"\" && @request.body.author = @request.auth.id\n// only the author may edit, and may not change the author\nupdateRule: author = @request.auth.id && @request.body.author:changed = false\n// only the author may delete\ndeleteRule: author = @request.auth.id", "text"),
  T("Inside a rule you can use the fields of the record, including fields of related records such as author.name. You can read the request with @request.auth for the signed-in user, @request.body for submitted data, @request.query for query parameters, @request.headers and @request.method. The @collection prefix lets a rule look at another collection that shares a value."),
  T("Modifiers add checks. The :isset modifier asks whether the client sent a field. The :changed modifier asks whether a submitted value differs from the stored one. The :length modifier counts items in a multiple field, and :each applies a condition to every item. Operators include =, !=, comparisons, ~ for like, and a question mark variant such as ?= that means any item matches. Macros such as @now and @todayStart are in UTC.")],
 [("What does a null rule mean?", ["Only superusers can do it", "Anyone can do it", "Nobody can do it", "Signed-in users can do it"], 0, "Locked is the default."),
  ("What status does an unmet view rule give?", ["404", "403", "200", "500"], 0, "As if it were not there."),
  ("What does an empty string rule mean?", ["Anyone can do it", "Locked", "Only owners", "Disabled"], 0, "Fully open.")],
 [("Who bypasses rules?", "Superusers."), ("What is @request.body?", "Submitted data."), ("What does :isset check?", "Whether a field was sent."), ("What does ?= mean?", "Any item equals.")],
 [MATCH("Rule values", "Match each rule value with its meaning.", [("null", "Superusers only"), ("\"\" (empty string)", "Anyone"), ("@request.auth.id != \"\"", "Signed-in users"), ("author = @request.auth.id", "Only the author")]),
  PL("Rule value", "Write rule_kind(rule, is_superuser): rule is null (None), an empty string, or an expression. Return 'allow' for superusers and for an empty rule, 'locked' for null, and 'check' for an expression.",
     "rule_kind(rule, is_superuser)", """
def rule_kind(rule, is_superuser):
    if is_superuser:
        return 'allow'
    if rule is None:
        return 'locked'
    if rule == '':
        return 'allow'
    return 'check'
""", [[None, False], [None, True], ["", False], ["@request.auth.id != \"\"", False], ["x = 1", True]], "Superusers first.", approx=None),
  PL("Failure status", "Write fail_status(action, locked): the HTTP status when the rule fails. A locked rule gives 403 for any action. Otherwise list gives 200, create gives 400, and view, update and delete give 404.",
     "fail_status(action, locked)", """
def fail_status(action, locked):
    if locked:
        return 403
    if action == 'list':
        return 200
    if action == 'create':
        return 400
    return 404
""", [["list", False], ["create", False], ["view", False], ["update", False], ["delete", False], ["list", True]], "Handle locked first.", approx=None),
  PL("A tiny rule evaluator", "Write check(rule, record, auth): evaluate a rule made of clauses joined by && and || (|| binds weaker, no parentheses). Each clause is 'left op right' with spaces around op, where op is one of = != > >= < <= ~ !~. Operands: a quoted string, true, false, a number, @request.auth.FIELD (from auth, empty string if missing) or a field of record (empty string if missing). The ~ operator is a case-insensitive contains, or starts-with / ends-with when the right side ends / starts with %.",
     "check(rule, record, auth)", """
def check(rule, record, auth):
    def val(tok):
        tok = tok.strip()
        if tok[:1] == '"' or tok[:1] == "'":
            return tok[1:-1]
        if tok == 'true':
            return True
        if tok == 'false':
            return False
        if tok.startswith('@request.auth.'):
            return auth.get(tok[14:], '')
        try:
            return float(tok) if '.' in tok else int(tok)
        except ValueError:
            pass
        return record.get(tok, '')

    def like(a, b):
        s = str(a).lower()
        p = str(b).lower()
        core = p.strip('%')
        if p.startswith('%') and p.endswith('%') and len(p) > 1:
            return core in s
        if p.endswith('%'):
            return s.startswith(core)
        if p.startswith('%'):
            return s.endswith(core)
        return core in s

    def clause(c):
        c = c.strip()
        for op in ['!=', '>=', '<=', '!~', '=', '>', '<', '~']:
            parts = c.split(' ' + op + ' ', 1)
            if len(parts) == 2:
                a = val(parts[0])
                b = val(parts[1])
                if op == '=':
                    return a == b
                if op == '!=':
                    return a != b
                if op == '~':
                    return like(a, b)
                if op == '!~':
                    return not like(a, b)
                try:
                    if op == '>':
                        return a > b
                    if op == '>=':
                        return a >= b
                    if op == '<':
                        return a < b
                    return a <= b
                except TypeError:
                    return False
        return False

    for alt in rule.split('||'):
        ok = True
        for c in alt.split('&&'):
            if not clause(c):
                ok = False
                break
        if ok:
            return True
    return False
""", [["@request.auth.id != \"\"", {}, {"id": "u1"}], ["@request.auth.id != \"\"", {}, {}], ["owner = @request.auth.id", {"owner": "u1"}, {"id": "u1"}], ["status = \"active\" || owner = @request.auth.id", {"status": "draft", "owner": "u2"}, {"id": "u1"}], ["@request.auth.id != \"\" && title ~ \"Lorem%\"", {"title": "Lorem ipsum"}, {"id": "x"}], ["price > 10", {"price": 12}, {}], ["price <= 10", {"price": 12}, {}], ["published = true", {"published": True}, {}], ["title ~ \"%ipsum\"", {"title": "Lorem ipsum"}, {}], ["title !~ \"zzz\"", {"title": "Lorem"}, {}]], "Split on || then &&.", approx=None)]))

def _b64(s):
    return base64.urlsafe_b64encode(s.encode()).decode().rstrip("=")

def tok(payload, parts=3):
    h = _b64(json.dumps({"alg": "HS256", "typ": "JWT"}))
    p = _b64(json.dumps(payload))
    return h + "." + p + ".sig" if parts == 3 else h + "." + p

A.append(CH(
 "Authentication",
 ("Auth", [
  "Auth collection | signs in | Users", "Password | gives | A token", "Token | is | A JWT", "Header | carries | The token",
  "OAuth2 | signs in | With Google or GitHub", "OTP | emails | A one-time code", "MFA | needs | Two methods"]),
 ["Any auth collection can sign users in. The classic way is a password: the server checks it and returns a signed token, a JWT, plus the record.",
  "The client sends the token in the Authorization header on later requests. The SDK keeps it in the authStore.",
  "PocketBase also supports OAuth2 providers, one-time passwords by email, and multi-factor authentication. Superusers sign in the same way, but cannot use OAuth2."],
 [("JWT", "A signed token with three parts: header, payload and signature."), ("authStore", "The SDK's storage for the token and the signed-in record."), ("OAuth2", "Signing in through another service like Google or GitHub."),
  ("OTP", "A one-time password sent by email."), ("MFA", "Multi-factor authentication: two methods in a row."), ("Verification", "Confirming that a user owns their email address.")],
 ["pb.collection('users').authWithPassword(email, password) returns the token and record.", "A JWT has header, payload and signature, joined by dots; the payload carries the id and the expiry.",
  "The token goes in the Authorization header.", "OAuth2 uses the redirect address /api/oauth2-redirect; _superusers do not support OAuth2.", "requestOTP returns an otpId, even if the email is unknown, so attackers cannot probe for accounts.",
  "Record creation does not sign the user in; you sign in after creating."],
 [T("Sign-in works on auth collections. A user record has an email and a password, and the server never stores the password itself, only a hash. You create the account with a normal create call. Creating does not sign anyone in."),
  C("// sign up, then sign in\nawait pb.collection('users').create({\n  email: 'ana@example.com',\n  password: 'a-long-password',\n  passwordConfirm: 'a-long-password',\n});\nconst auth = await pb.collection('users').authWithPassword('ana@example.com', 'a-long-password');\nconsole.log(pb.authStore.isValid, pb.authStore.record.id);\n\n// call later: refresh the token\nawait pb.collection('users').authRefresh();\n// sign out\npb.authStore.clear();", "javascript"),
  T("The token is a JSON Web Token. It is three parts joined by dots: a header, a payload and a signature. The payload holds claims such as the record id, the collection and the expiry time. The signature proves that the server issued it. The client sends it in the Authorization header, and the SDK does that for you."),
  T("OAuth2 lets users sign in with Google, GitHub and many other providers. You enable a provider in the collection settings with its client id and secret, and use the redirect address on your own server, ending in /api/oauth2-redirect. In the browser, authWithOAuth2 opens a popup and finishes the flow. Superusers are the exception: OAuth2 is not supported for the _superusers collection."),
  T("A one-time password sends a short code to the user's email. You call requestOTP, which returns an otpId, and then authWithOTP with that id and the code. The otpId is returned even when no such user exists, so nobody can use it to find out which emails are registered. For sensitive apps, combine OTP with another method using multi-factor authentication."),
  T("Verification is separate: it confirms that a user controls an email address, by sending a link. A rule can then require @request.auth.verified = true. Next to sign-in there are helpers for password reset and for changing an email address.")],
 [("What does a JWT payload usually carry?", ["The record id and the expiry", "The password", "The database file", "The collection rules"], 0, "Claims."),
  ("Does creating a user sign them in?", ["No", "Yes", "Only for admins", "Only by OAuth2"], 0, "Sign in separately."),
  ("Which collection does not support OAuth2?", ["_superusers", "users", "Any auth collection", "views"], 0, "A documented caveat.")],
 [("Where is the token sent?", "In the Authorization header."), ("What does requestOTP return?", "An otpId."), ("What does MFA need?", "Two methods."), ("What clears the sign-in?", "pb.authStore.clear().")],
 [FILL("Sign in", "Use pb.collection('users').{{authWithPassword}}(email, password), and the token is kept in pb.{{authStore}}."),
  PL("Token status", "Write token_status(token, now): the token has three parts joined by dots, and the middle part is base64url JSON with an integer exp (expiry seconds). Return 'malformed' if it does not have three parts, cannot be decoded, or has no integer exp; 'expired' if now is at or after exp; otherwise 'valid'. (The signature is not checked here, only a server can do that.)",
     "token_status(token, now)", """
def token_status(token, now):
    import json
    parts = token.split('.')
    if len(parts) != 3:
        return 'malformed'
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    s = parts[1].replace('-', '+').replace('_', '/')
    bits = 0
    nbits = 0
    out = ''
    try:
        for ch in s:
            if ch == '=':
                break
            v = alphabet.find(ch)
            if v < 0:
                return 'malformed'
            bits = (bits << 6) | v
            nbits += 6
            if nbits >= 8:
                nbits -= 8
                out += chr((bits >> nbits) & 255)
                bits &= (1 << nbits) - 1
        data = json.loads(out)
        exp = data.get('exp')
    except Exception:
        return 'malformed'
    if not isinstance(exp, int) or isinstance(exp, bool):
        return 'malformed'
    if now >= exp:
        return 'expired'
    return 'valid'
""", [[tok({"id": "abc", "exp": 2000}), 1000], [tok({"id": "abc", "exp": 2000}), 2000], [tok({"id": "abc", "exp": 2000}), 3000], [tok({"id": "abc"}), 1000], [tok({"exp": 5}, parts=2), 1], ["not.a.token", 1], [tok({"exp": "x"}), 1]], "Decode the middle part by hand.", approx=None),
  PL("OTP check", "Write otp_check(stored, entered, issued, now, ttl): return 'expired' when now - issued is at least ttl seconds, otherwise 'ok' if the codes are equal, otherwise 'wrong'.",
     "otp_check(stored, entered, issued, now, ttl)", """
def otp_check(stored, entered, issued, now, ttl):
    if now - issued >= ttl:
        return 'expired'
    if stored == entered:
        return 'ok'
    return 'wrong'
""", [["12345678", "12345678", 0, 60, 180], ["12345678", "87654321", 0, 60, 180], ["12345678", "12345678", 0, 180, 180], ["12345678", "12345678", 100, 150, 180]], "Check the time first.", approx=None)]))

A.append(CH(
 "Relations, expand and view collections",
 ("Relations", [
  "Relation field | stores | Record ids", "Expand | loads | The related record", "expand | fills | record.expand", "Back-relation | expands | The other direction",
  "cascadeDelete | removes | Dependent records", "View collection | joins | Collections", "Index | speeds | Joins"]),
 ["A relation field stores the id of a record in another collection, or several ids for a multiple relation. Rules can follow relations too, for example author.verified = true.",
  "The expand option loads the related records in the same response, under record.expand. Nested paths like author.team work too, and a back-relation can be expanded in the other direction.",
  "The labs join records and find back-relations."],
 [("Relation field", "A field holding the id or ids of other records."), ("Expand", "Loading related records into record.expand."), ("Back-relation", "The records in another collection that point at this one."),
  ("Cascade delete", "Deleting dependent records when the parent is deleted."), ("Multiple relation", "A relation field that holds a list of ids."), ("Join", "Combining rows of two tables by a shared value.")],
 ["A relation stores ids, so a plain read shows only an id like author: 'abc123'.", "expand: 'author' adds record.expand.author with the full record.", "Nested paths use dots: expand: 'author.team'.",
  "Related records you may not view are left out of expand, because their view rule applies.", "A back-relation expand uses the form COLLECTION_via_FIELD.", "cascadeDelete true removes dependent records; false blocks deleting the parent."],
 [T("A relation is a pointer. In a posts collection you add an author field of type relation that points to users. The stored value is the user's id. The API returns that id by default, because returning a whole user inside every post would be wasteful."),
  T("When you do want the user, ask for it with expand. The SDK puts the loaded record in record.expand.author, never directly on the record. You can expand several fields at once, separated by commas, and go deeper with dots, such as author.team."),
  C("const post = await pb.collection('posts').getOne(id, { expand: 'author,comments_via_post.user' });\nconsole.log(post.expand.author.name);\n// comments that point at this post, loaded from the other side\nconsole.log(post.expand.comments_via_post);", "javascript"),
  T("Access rules still apply to expanded records. If you may not view the author record, it simply does not appear in expand. This keeps a relation from leaking data that the target's own rules protect."),
  T("What happens when you delete a record that others point at? A relation field has a cascadeDelete option. When it is true, deleting the parent removes the dependent records. When it is false, the parent cannot be deleted until the dependents are gone or changed. Choose false for important data like orders."),
  T("When you need aggregates, such as a post and its comment count, create a view collection. It is a SQL query, so joins and GROUP BY are available. It is read-only and sends no realtime events, but it can have list and view rules like any other collection.")],
 [("What does a relation field store?", ["Record ids", "Whole records", "SQL", "Passwords"], 0, "Ids only."),
  ("Where do expanded records appear?", ["record.expand", "record.data", "At the record's root", "In headers"], 0, "Under expand."),
  ("What does cascadeDelete false do?", ["Blocks deleting the parent", "Deletes children", "Ignores rules", "Archives"], 0, "Protects dependents.")],
 [("How do you expand a nested path?", "With dots: author.team."), ("What is a back-relation?", "Records pointing at this one."), ("Which collection type joins SQL?", "View."), ("Do rules apply to expands?", "Yes.")],
 [MATCH("Relations", "Match each term with its meaning.", [("expand", "Load related records"), ("cascadeDelete", "Remove dependents on delete"), ("View collection", "Read-only SQL result"), ("Multiple relation", "A list of record ids")]),
  PL("Parse expand", "Write expand_paths(s): split an expand string like 'author,comments.user' into a list of paths, each a list of names: [['author'], ['comments', 'user']]. Ignore empty parts.",
     "expand_paths(s)", """
def expand_paths(s):
    out = []
    for part in s.split(','):
        part = part.strip()
        if part:
            out.append(part.split('.'))
    return out
""", [["author"], ["author,comments.user"], ["a.b.c"], [""], ["a,,b"]], "Split twice.", approx=None),
  PL("Expand a relation", "Write expand(posts, users): posts is a list of [post_id, author_id], users is a list of [user_id, name]. Return a list of [post_id, name] with None for a missing author.",
     "expand(posts, users)", """
def expand(posts, users):
    names = {}
    for uid, name in users:
        names[uid] = name
    out = []
    for pid, aid in posts:
        out.append([pid, names.get(aid)])
    return out
""", [[[["p1", "u1"], ["p2", "u2"], ["p3", "u9"]], [["u1", "Ana"], ["u2", "Ben"]]], [[], []], [[["p1", "u1"]], []]], "Build a lookup first.", approx=None),
  PL("Back-relations", "Write back_relations(users, posts): users is a list of user ids and posts is a list of [post_id, author_id]. Return a list of [user_id, sorted list of post ids] for every user, sorted by user id.",
     "back_relations(users, posts)", """
def back_relations(users, posts):
    by = {}
    for u in users:
        by[u] = []
    for pid, aid in posts:
        if aid in by:
            by[aid].append(pid)
    out = []
    for u in sorted(by):
        out.append([u, sorted(by[u])])
    return out
""", [[["u2", "u1"], [["p1", "u1"], ["p2", "u2"], ["p3", "u1"]]], [["u1"], []], [[], [["p1", "u1"]]]], "Group posts by author.", approx=None)]))
