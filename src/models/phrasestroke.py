from datetime import datetime
import dateutil.parser
import json
import IPython

class PhraseStroke:
    def __init__(self, start_time, phrase, terminating, end_time = datetime.now()):
        self.end_timestamp = str(end_time)
        self.start_timestamp = str(start_time)
        self.duration = (dateutil.parser.parse(self.end_timestamp) - dateutil.parser.parse(self.start_timestamp)).total_seconds()
        self.phrase = phrase
        self.terminating = terminating

    @classmethod
    def from_json(cls, jd):
        print(jd)
        return cls(jd['start_timestamp'], jd['phrase'], jd['terminating'], jd['end_timestamp'])