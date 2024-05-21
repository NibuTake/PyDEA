import numpy as np

from Pyfrontier.domain import DMU, AdditiveResult, EnvelopResult, MultipleResult

dmu = DMU(np.array([1, 2]), np.array([1]), id=0)


class TestEnvelopResult:
    def test_score1_with_no_slack(self):
        x_slack = [0, 0]
        y_slack = [0]
        result = EnvelopResult(1.0, 1, dmu, [1, 1], x_slack, y_slack)
        assert result.is_efficient
        assert not result.has_slack

    def test_score1_with_slack(self):
        x_slack = [0, 0]
        y_slack = [0.5]
        result = EnvelopResult(1.0, 1, dmu, [1, 1], x_slack, y_slack)
        assert not result.is_efficient
        assert result.has_slack

    def test_score09_result(self):
        x_slack = [0, 0]
        y_slack = [0.5]
        result = EnvelopResult(0.9, 1, dmu, [1, 1], x_slack, y_slack)
        assert not result.is_efficient


class TestMultipleResult:
    def test_score1_is_efficient(self):
        x_weight = [1, 1]
        y_weight = [0]
        result = MultipleResult(1.0, 1, dmu, x_weight, y_weight, 0.0)
        assert result.is_efficient

    def test_score09_is_inefficient(self):
        x_weight = [1, 1]
        y_weight = [0]
        result = MultipleResult(0.9, 1, dmu, x_weight, y_weight, 0.0)
        assert not result.is_efficient


class TestAdditiveResult:
    def test_no_slack_is_efficient(self):
        x_slack = [0, 0]
        y_slack = [0]
        result = AdditiveResult(0.0, 1, dmu, x_slack, y_slack, [])
        assert result.is_efficient

    def test_positive_slack_is_inefficient(self):
        x_slack = [0, 0]
        y_slack = [0.1]
        result = AdditiveResult(0.0, 1, dmu, x_slack, y_slack, [])
        assert not result.is_efficient
