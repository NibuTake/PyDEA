import numpy as np

from Pyfrontier.domain import DMU, AdditiveResult, EnvelopResult, MultipleResult

dmu = DMU(np.array([1, 2]), np.array([1]), id=0)


class TestEnvelopResult:
    def test_score1_with_no_slack(self):
        x_slack = [0, 0]
        y_slack = [0]
        result = EnvelopResult(1.0, 1, dmu, [1, 1], x_slack, y_slack, "in")
        assert result.is_efficient
        assert not result.has_slack

    def test_score1_with_slack(self):
        x_slack = [0, 0]
        y_slack = [0.5]
        result = EnvelopResult(1.0, 1, dmu, [1, 1], x_slack, y_slack, "in")
        assert not result.is_efficient
        assert result.has_slack

    def test_score09_result(self):
        x_slack = [0, 0]
        y_slack = [0.5]
        result = EnvelopResult(0.9, 1, dmu, [1, 1], x_slack, y_slack, "in")
        assert not result.is_efficient

    def test_virtual_dmu_input_oriented(self):
        # Input-oriented: projected_input = score * input - x_slack
        #                 projected_output = output + y_slack
        x_slack = [0.1, 0.2]
        y_slack = [0.5]
        score = 0.8
        result = EnvelopResult(score, 1, dmu, [1, 1], x_slack, y_slack, "in")

        virtual = result.virtual_dmu

        # Verify projected input: 0.8 * [1, 2] - [0.1, 0.2] = [0.8, 1.6] - [0.1, 0.2] = [0.7, 1.4]
        expected_input = np.array([0.7, 1.4])
        np.testing.assert_array_almost_equal(virtual.input, expected_input)

        # Verify projected output: [1] + [0.5] = [1.5]
        expected_output = np.array([1.5])
        np.testing.assert_array_almost_equal(virtual.output, expected_output)

        # Verify DMU id is preserved
        assert virtual.id == dmu.id

    def test_virtual_dmu_output_oriented(self):
        # Output-oriented: projected_input = input - x_slack
        #                  projected_output = score * output + y_slack
        x_slack = [0.1, 0.2]
        y_slack = [0.5]
        score = 1.2
        result = EnvelopResult(score, 1, dmu, [1, 1], x_slack, y_slack, "out")

        virtual = result.virtual_dmu

        # Verify projected input: [1, 2] - [0.1, 0.2] = [0.9, 1.8]
        expected_input = np.array([0.9, 1.8])
        np.testing.assert_array_almost_equal(virtual.input, expected_input)

        # Verify projected output: 1.2 * [1] + [0.5] = [1.2] + [0.5] = [1.7]
        expected_output = np.array([1.7])
        np.testing.assert_array_almost_equal(virtual.output, expected_output)

        # Verify DMU id is preserved
        assert virtual.id == dmu.id

    def test_virtual_dmu_efficient_unit(self):
        # For efficient units (score=1, no slack), virtual DMU should equal original DMU
        x_slack = [0, 0]
        y_slack = [0]
        result = EnvelopResult(1.0, 1, dmu, [1, 1], x_slack, y_slack, "in")

        virtual = result.virtual_dmu

        np.testing.assert_array_almost_equal(virtual.input, dmu.input)
        np.testing.assert_array_almost_equal(virtual.output, dmu.output)
        assert virtual.id == dmu.id


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
