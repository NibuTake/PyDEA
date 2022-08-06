import abc


class BaseSolver(object, metaclass=abc.ABCMeta):
    def __init__(self, orient: str, frontier: str, DMUs):
        """AI is creating summary for __init__

        Args:
            orient (str): [description]
            frontier (str): [description]
            DMUs ([type]): [description]
        """
        self.orient = orient
        self.DMUs = DMUs
        self.frontier = frontier
        self.u_c_index = 100

    @abc.abstractmethod
    def apply(self) -> list:
        pass

    @abc.abstractmethod
    def _solve_problem(self, o: int) -> dict:
        pass

    def _dict_to_list(self, _dict: dict) -> list:
        return [_dict[k] for k in _dict]

    def _rounder(self, v: float) -> float:
        self._sign_figs = 6
        return round(v, self._sign_figs)
