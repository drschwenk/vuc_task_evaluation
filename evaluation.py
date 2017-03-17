from __future__ import division
import numpy as np
import pandas as pd
import json
import string
from collections import defaultdict
from collections import Counter


class BaseEvaluator(object):
    def __init__(self, data_path, submission_path):
        self.data_path = data_path
        self.submission_path = submission_path
        self.dataset = None

