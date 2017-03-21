from __future__ import print_function
import sys


class BaseEvaluator(object):
    def __init__(self, data_path, submission_path):
        self.data_path = data_path
        self.submission_path = submission_path
        self.dataset = None

    def std_err_print(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    def validate_submission(self, submission):
        complete = self.check_complete(submission)
        formatted = self.check_format(submission)
        if not complete and not formatted:
            passed_test_message = 'you passed'
        else:
            failed_test_message = 'you did not pass'
        return

    def check_complete(self, submission):
        pass

    def check_format(self, submission):
        pass

