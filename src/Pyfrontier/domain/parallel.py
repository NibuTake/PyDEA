from typing import List

from dataclasses import dataclass
import multiprocessing

from Pyfrontier.domain.result import BaseResult


@dataclass
class NumberOfJobs:
    _n_jobs: int = 1

    def __post_init__(self):
        self._minimum_job_validation()

    def _minimum_job_validation(self):
        if self._n_jobs < 1:
            raise ValueError("The number of parallel jobs must >= 1.")
        self._n_jobs = min(self._n_jobs, multiprocessing.cpu_count())

    @property
    def value(self) -> int:
        return self._n_jobs


@dataclass
class MultiProcessor:
    _solver_function: callable
    _n_dmus: int

    def solve(self, n_jobs: int) -> List[BaseResult]:
        if n_jobs <= 1:
            return [self._solver_function(j) for j in range(self._n_dmus)]
        else:
            pool = multiprocessing.Pool(n_jobs)

            problem_processes = []
            for j in range(self._n_dmus):
                problem_processes.append(
                    pool.apply_async(self._solver_function, args=(j,))
                )

            pool.close()
            pool.join()

            return [problem.get() for problem in problem_processes]
