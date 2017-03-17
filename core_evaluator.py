import pandas
from .charades import LocalizationEvaluator
from .charades import ClassificationEvaluator


class Evaluator(object):
    def __init__(self):
        self.subtask_name = None

    @classmethod
    def get_submission_specific_evaluator(cls, submission_file, gt_file):
        if 'loc' in submission_file.lower():
            return LocalizationEvaluator(gt_file, submission_file)
        if 'class' in submission_file.lower():
            return ClassificationEvaluator(gt_file, submission_file)
