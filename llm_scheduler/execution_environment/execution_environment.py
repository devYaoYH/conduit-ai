import time
import datetime

def format_time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def init(exe_id: str = None):
    """ Set an execution ID for batch retrieval of results. """
    global execution_id
    # Defaults to timestamp if not given an execution ID
    execution_id = exe_id if exe_id is not None else format_time(time.time())


def get_execution_id():
    if execution_id is None:
        return ""
    else:
        return execution_id
