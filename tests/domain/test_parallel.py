import pytest
from Pyfrontier.domain.parallel import MultiProcessor, NumberOfJobs


class TestNumberOfJobs:
    @pytest.mark.parametrize(
        "n_jobs",
        [1, 2],
    )
    def test_happy_path(self, n_jobs):
        assert NumberOfJobs(n_jobs).value == n_jobs

    @pytest.mark.parametrize(
        "n_jobs",
        [-1, 0],
    )
    def test_raise_error_with_invalid_n_jobs(self, n_jobs):
        with pytest.raises(ValueError):
            NumberOfJobs(n_jobs)


class TestMultiProcessor:
    @pytest.mark.parametrize(
        "n_jobs",
        [0, 1],
    )
    def test_happy_path(self, n_jobs):
        MultiProcessor(print, 5).solve(n_jobs)
