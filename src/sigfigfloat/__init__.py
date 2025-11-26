import math


class SigFigFloat:
    figs = 3
    orig_val = math.nan
    rounded = math.nan
    scale = math.nan
    epsilon = math.nan

    @staticmethod
    def get_scale(val):
        if val == 0.0:
            return 0.0
        if math.isnan(val):
            return math.nan
        return 10 ** (math.floor(math.log10(abs(float(val)))))

    @staticmethod
    def round_to_sig_figs(val, scale, figs):
        if val == 0.0:
            return 0.0
        if math.isnan(val):
            return math.nan
        # round the scaled number and then scale it back
        return round(float(val / scale), figs - 1) * scale

    def __init__(self, orig_val, figs=None):
        if figs is not None:
            if figs < 1:
                raise ValueError(f"{figs} is below the minimum of 1")
            self.figs = figs
        self.orig_val = orig_val
        self.scale = SigFigFloat.get_scale(orig_val)
        self.rounded = SigFigFloat.round_to_sig_figs(
            self.orig_val, self.scale, self.figs
        )
        base = self.scale if self.scale != 0.0 else 1.0
        self.epsilon = base / (10**self.figs)

    def __add__(self, o):
        o2 = o.orig_val if isinstance(o, SigFigFloat) else o
        return SigFigFloat(self.orig_val + o2, self.figs)

    def __radd__(self, o):
        return self + o

    def __sub__(self, o):
        o2 = o.orig_val if isinstance(o, SigFigFloat) else o
        return SigFigFloat(self.orig_val - o2, self.figs)

    def __rsub__(self, o):
        return SigFigFloat(o, self.figs) - self

    def __truediv__(self, o):
        o2 = o.orig_val if isinstance(o, SigFigFloat) else o
        return SigFigFloat(self.orig_val / o2, self.figs)

    def __rtruediv__(self, o):
        o2 = SigFigFloat(o, self.figs)
        return SigFigFloat(o2 / self.orig_val, self.figs)

    def __mul__(self, o):
        o2 = o.orig_val if isinstance(o, SigFigFloat) else o
        return SigFigFloat(self.orig_val * o2, self.figs)

    def __rmul__(self, o):
        return self * o

    def __pow__(self, e):
        e2 = e.orig_val if isinstance(e, SigFigFloat) else e
        return SigFigFloat(self.orig_val**e2, self.figs)

    def __str__(self):
        if math.isnan(self.scale):
            return "nan"
        if self.scale < 0.001 or (
            self.scale > 1e4 and math.log10(self.scale) > self.figs
        ):
            # below 1e-3 / above 1e4, use scientific notation
            fmt = f"{{:.{self.figs - 1}e}}"
            return fmt.format(self.rounded)

        pow_10 = int(math.log10(self.scale))
        if pow_10 > self.figs:
            # if we have fewer sig-figs than digits, return int
            return str(int(self.rounded))

        frac_digits = max(max([pow_10, self.figs]) - min([pow_10, self.figs]) - 1, 0)
        return f"{{:.{frac_digits}f}}".format(self.rounded)

    def __repr__(self):
        return repr(self.orig_val)

    def __lt__(self, o):
        rounded_o = (
            o.rounded
            if isinstance(o, SigFigFloat)
            else SigFigFloat.round_to_sig_figs(o, self.scale, self.figs)
        )
        return self.orig_val < rounded_o

    def __gt__(self, o):
        rounded_o = (
            o.rounded
            if isinstance(o, SigFigFloat)
            else SigFigFloat.round_to_sig_figs(o, self.scale, self.figs)
        )
        return self.orig_val > rounded_o

    def __eq__(self, o):
        rounded_o = (
            o.rounded
            if isinstance(o, SigFigFloat)
            else SigFigFloat.round_to_sig_figs(o, self.scale, self.figs)
        )
        return abs(self.rounded - rounded_o) < self.epsilon

    def __le__(self, o):
        return (self < o) or (self == o)

    def __ge__(self, o):
        return (self > o) or (self == o)

    def __float__(self):
        return float(self.orig_val)

    def __int__(self):
        return int(float(self))
