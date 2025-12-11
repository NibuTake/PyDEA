import numpy as np

from Pyfrontier.frontier_model import EnvelopDEA


def test_label_is_set_in_result():
    """Test that labels are correctly set in result and DMU."""
    inputs = np.array([[1, 2], [2, 3], [3, 4]])
    outputs = np.array([[2], [3], [4]])
    labels = np.array(["三重県", "京都府", "東京都"])

    dea = EnvelopDEA("CRS", "in")
    dea.fit(inputs, outputs, labels=labels)

    for r in dea.result:
        assert r.label == labels[r.id]
        assert r.dmu.label == labels[r.id]
