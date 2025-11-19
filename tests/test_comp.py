from sigfigfloat import SigFigFloat

FULL_PREC = 1.4999999999
SIG_FIG = SigFigFloat(FULL_PREC)

def test_basic():
    assert SIG_FIG.orig_val == FULL_PREC
    assert SIG_FIG.rounded == 1.5

    assert SIG_FIG == SIG_FIG
    assert SIG_FIG == FULL_PREC
    assert SIG_FIG > 1.49

def test_str():
    assert str(SIG_FIG) == "1.50"
    assert repr(SIG_FIG) == "1.4999999999"

def test_coercion():
    orig_val = float(SIG_FIG)
    assert isinstance(orig_val, float)
    assert orig_val == FULL_PREC
    assert str(orig_val) != str(SIG_FIG)
