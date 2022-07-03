from dataclasses import dataclass


@dataclass
class Level:
    var: int

    def __post_init__(self):
        if int(self.var) < 0:
            raise ValueError()


@dataclass
class Degree:
    var: int

    def __post_init__(self):
        if int(self.var) < 0:
            raise ValueError()


@dataclass
class Attractiveness:
    var: float


@dataclass
class Progress:
    _var: float

    @property
    def var(self):
        return self._var
