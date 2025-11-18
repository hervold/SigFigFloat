from sigfigfloat import SigFigFloat


def test_basic():
    full_prec = 1.4999999999
    sig_fig = SigFigFloat(full_prec)

    assert sig_fig == sig_fig
    assert sig_fig == full_prec
    assert sig_fig > 1.49
