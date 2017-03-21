import pytest
import os.path
from .tqa import TqaEvaluator

tqa_base_path = './test/tqa'


@pytest.fixture
def tqa_evaluator(tqa_submission, gt_path='./val_ans.json'):
    evaluator = TqaEvaluator(gt_path, tqa_submission)
    return evaluator


@pytest.mark.parametrize("tqa_submission, expected", [
        (os.path.join(tqa_base_path, 'random.json'), 0.2392164249387832),
        (os.path.join(tqa_base_path, 'perfect.json'), 1.0),
    ])
def test_tqa_submissions(tqa_evaluator,tqa_submission, expected):
    accuracies = tqa_evaluator.evaluate_submission()
    assert accuracies[0][1] == expected


@pytest.mark.parametrize("tqa_submission, expected", [
    (os.path.join(tqa_base_path, 'missing_vals.json'), AssertionError),
    (os.path.join(tqa_base_path, 'extra_vals.json'), AssertionError),
    (os.path.join(tqa_base_path, 'malformed_bad_prefix.json'), AssertionError),
    (os.path.join(tqa_base_path, 'malformed_bad_id_number.json'), AssertionError),
    (os.path.join(tqa_base_path, 'malformed_bad_answer.json'), AssertionError),
])
def test_tqa_structural(tqa_evaluator, tqa_submission, expected):
    with pytest.raises(expected):
        tqa_evaluator.evaluate_submission()
