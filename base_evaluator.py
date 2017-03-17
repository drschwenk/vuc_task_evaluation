class BaseEvaluator(object):
    def __init__(self, data_path, submission_path):
        self.data_path = data_path
        self.submission_path = submission_path
        self.dataset = None

