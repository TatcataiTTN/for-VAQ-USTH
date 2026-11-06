"""Helpers for the Concept finder data (build/concepts/mNN.py).  Every text is a pair (vi, en).
K(...)  one concept of a module.   O(...)  a topic outside the course: the analyser reports it as "out of scope" instead of forcing a match.
facts   = [(formula text, (vi, en) note)]     steps / traps / angles = [(vi, en)]    topics = English topic names that exist in the module's question bank
kw / kwv = English / Vietnamese phrases the analyser looks for.   src = book sections that were actually read.   chk = key in checks.CHECKS (numeric check of the formulas)."""
CONCEPTS = []; OUT = []

def _bi(x):
    assert isinstance(x, tuple) and len(x) == 2 and all(isinstance(s, str) and s.strip() for s in x), x
    return dict(vi=x[0], en=x[1])

def K(cid, mod, name, defn, facts=(), steps=(), traps=(), angles=(), topics=(), kw=(), kwv=(), units=(), src=(), related=(), chk=None):
    assert cid.startswith(mod + '-'), cid
    assert not any(c['id'] == cid for c in CONCEPTS), 'duplicate ' + cid
    CONCEPTS.append(dict(id=cid, mod=mod, name=_bi(name), defn=_bi(defn), facts=[dict(f=f, note=_bi(n)) for f, n in facts], steps=[_bi(s) for s in steps],
                         traps=[_bi(t) for t in traps], angles=[_bi(a) for a in angles], topics=list(topics), kw=[k.lower() for k in kw], kwv=[k.lower() for k in kwv],
                         units=list(units), src=list(src), related=list(related), chk=chk))

def O(oid, name, kw, kwv, note):
    OUT.append(dict(id=oid, name=_bi(name), kw=[k.lower() for k in kw], kwv=[k.lower() for k in kwv], note=_bi(note)))
