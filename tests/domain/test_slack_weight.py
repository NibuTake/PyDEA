import numpy as np
import pytest

from Pyfrontier.domain import SlackWeight


class TestSlackWeight:
    def test_weights_have_to_be_positive(self):
        with pytest.raises(ValueError):
            SlackWeight(np.array([-1, 0.5]), 1)

    def test_raise_error_if_the_obj_has_different_dim(self):
        with pytest.raises(ValueError):
            SlackWeight(np.array([0.5, 0.5]), 1)

    def test_the_sum_of_weights_becomes_1(self):
        slack_weight = SlackWeight(np.array([3, 3]), 2)
        assert np.all(slack_weight.value == np.array([0.5, 0.5]))
