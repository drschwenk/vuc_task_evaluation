#!/usr/bin/env python
import os
from chooser import EvaluatorSelector


def write_score_file(scores, out_path):
    with open(os.path.join(out_path, 'scores.txt'), 'w') as output_file:
        output_form = ['{0}:{1}\n'.format(metric, result) for metric, result in scores.items()]
        output_file.writelines(output_form)


def score(input_dir, output_dir):
    gt_data_base_path = os.path.join(input_dir, 'ref')
    submission_base_path = os.path.join(input_dir, 'res')
    gt_filename = os.listdir(gt_data_base_path)
    gt_file = os.path.join(gt_data_base_path, gt_filename.pop())
    assert not gt_filename  # there should never be more than one file in the ref data dir
    submission_files = os.listdir(submission_base_path)
    submissions = [os.path.join(submission_base_path, f) for f in submission_files]
    evaluators = [EvaluatorSelector.get_submission_specific_evaluator(f, gt_file) for f in submissions]
    if len(evaluators) > 1:
        submission_scores = dict(evaluator.evaluate_submission() for evaluator in evaluators if evaluator)
    else:
        submission_scores = dict(evaluators[0].evaluate_submission())
    write_score_file(submission_scores, output_dir)

