"""Small helpers for writing course content."""


def T(*items):
    return {"type": "text", "items": list(items)}


def C(code, lang="text"):
    return {"type": "code", "lang": lang, "code": code.strip("\n")}


def M(tex):
    """A displayed formula."""
    return {"type": "math", "tex": tex}
