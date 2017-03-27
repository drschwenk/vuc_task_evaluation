import pytest
import os.path
from .score_submission import EvaluatorSelector


tqa_base_path = './test/tqa'
charades_base_path = './test/charades'
thor_base_path = './test/thor'
tqa_gt_path = os.path.join(tqa_base_path, 'val_ans.json')
charades_gt_path = os.path.join(charades_base_path, 'Charades_v1_test.csv')



@pytest.fixture
def evaluator(submission, gt_path):
    submission_evaluator = EvaluatorSelector.get_submission_specific_evaluator(submission, gt_path)
    return submission_evaluator


###
#TQA tests here
###
@pytest.mark.parametrize("submission, gt_path, expected", [
        (os.path.join(tqa_base_path, 'random.json'), tqa_gt_path, 0.2392164249387832),
        (os.path.join(tqa_base_path, 'perfect.json'), tqa_gt_path, 1.0)])
def test_tqa_submissions(evaluator, submission, expected):
    accuracies = evaluator.evaluate_submission()
    assert accuracies[0][1] == expected


@pytest.mark.parametrize("submission, gt_path, expected", [
    (os.path.join(tqa_base_path, 'missing_vals.json'), tqa_gt_path, AssertionError),
    (os.path.join(tqa_base_path, 'extra_vals.json'), tqa_gt_path, AssertionError),
    (os.path.join(tqa_base_path, 'malformed_bad_prefix.json'), tqa_gt_path, AssertionError),
    (os.path.join(tqa_base_path, 'malformed_bad_id_number.json'), tqa_gt_path, AssertionError),
    (os.path.join(tqa_base_path, 'malformed_bad_answer.json'), tqa_gt_path, AssertionError)])
def test_tqa_structural(evaluator, submission, gt_path, expected):
    with pytest.raises(expected):
        evaluator.evaluate_submission()


###
# Charades tests here
###
@pytest.mark.parametrize("submission, gt_path, expected", [
    (os.path.join(charades_base_path, 'charades_class_sample.txt'), charades_gt_path, 0.18614618839020669),
    (os.path.join(charades_base_path, 'charades_loc_sample.txt'), charades_gt_path, 0.089389146288006677),
    (os.path.join(charades_base_path, 'charades_loc_scrambled.txt'), charades_gt_path, 0.089389146288006677),
    (os.path.join(charades_base_path, 'charades_class_scrambled.txt'), charades_gt_path, 0.18614618839020669),
    ])
def test_charades_submissions(evaluator, submission, gt_path, expected):
    mean_ap = evaluator.evaluate_submission()
    assert mean_ap[1] == expected


@pytest.mark.parametrize("submission, gt_path, expected", [
    (os.path.join(charades_base_path, 'charades_loc_missing.txt'), charades_gt_path, AssertionError),
    (os.path.join(charades_base_path, 'charades_class_missing.txt'), charades_gt_path, AssertionError),
    (os.path.join(charades_base_path, 'charades_class_obj_class_missing.txt'), charades_gt_path, AssertionError),
    (os.path.join(charades_base_path, 'charades_loc_obj_class_missing.txt'), charades_gt_path, AssertionError),
    ])
def test_charades_structural(evaluator, submission, gt_path, expected):
    with pytest.raises(expected):
        evaluator.evaluate_submission()