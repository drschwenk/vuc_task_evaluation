from __future__ import division
import json
import string
from collections import defaultdict
from collections import Counter
from .base_evaluator import BaseEvaluator


class TqaEvaluator(BaseEvaluator):

    def __init__(self, data_path, submission_path):
        super(TqaEvaluator, self).__init__(data_path, submission_path)
        self.dataset = None
        self.all_subtasks = ['text', 'diagram']

    def load_groundtruth(self):
        with open(self.data_path, 'r') as f:
            self.dataset = json.load(f)

    def evaluate_submission(self):
        with open(self.submission_path, 'r') as f:
            submission = json.load(f)
        self.load_groundtruth()
        self.validate_submission(submission)
        n_correct = self.count_correct(submission)
        n_total = Counter([qid.split('_')[0] for qid in self.dataset])
        dq_accuracy = n_correct['DQ'] / n_total['DQ']
        ndq_accuracy = n_correct['NDQ'] / n_total['NDQ']
        scores = list(zip(self.all_subtasks, [ndq_accuracy, dq_accuracy]))
        return scores

    def count_correct(self, predicted_answers):
        correct = []
        for qid, ans in predicted_answers.items():
            if self.answered_correctly(ans, qid):
                correct.append(qid.split('_')[0])
        correct_by_type = Counter(correct)
        correct_by_type['overall'] = sum(correct_by_type.values())
        return correct_by_type

    def answered_correctly(self, submission_answer, qid):
        return submission_answer == self.dataset[qid]

    def check_format(self, predicted_answers):
        errors = defaultdict(list)
        for qid, answer in predicted_answers.items():
            id_prefix, id_number = qid.split('_')[:2]
            if id_prefix not in ['DQ', 'NDQ']:
                errors[qid].append('bad id prefix')
            if len(id_number) != 6:
                errors[qid].append('bad id number')
            if answer not in string.ascii_letters:
                errors[qid].append('answer not a letter index')
        for qid, error in errors.items():
            self.std_err_print(qid, ' ', error)
        assert not errors

    def check_complete(self, predicted_answers):
        errors = []
        all_dataset_questions = self.dataset
        ndq_gt = set([qk for qk in all_dataset_questions.keys() if 'N' in qk])
        ndq_sub = set([qk for qk in predicted_answers.keys() if 'N' in qk])
        dq_sub = set([qk for qk in predicted_answers.keys() if 'N' not in qk])
        if dq_sub:
            questions_missing = dq_sub.difference(set(predicted_answers.keys()))
        else:
            questions_missing = ndq_gt.difference(ndq_sub)
        questions_extra = set(predicted_answers.keys()).difference(set(all_dataset_questions.keys()))
        no_duplicate_questions = len(set(predicted_answers.keys())) == len(predicted_answers.keys())
        assert no_duplicate_questions
        if questions_missing:
            self.std_err_print('***Warning***\n', 'unanswered questions detected')
        if questions_extra:
            self.std_err_print('***Warning***\n', 'extra questions detected')
        if errors:
            self.std_err_print('errors found ')
            for qid, error in errors.items():
                self.std_err_print(qid, ' ', error)
        assert not questions_missing and not questions_extra
