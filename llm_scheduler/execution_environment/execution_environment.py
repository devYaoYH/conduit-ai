import time
import datetime

def format_time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def init(exe_id: str = None):
    """ Set an execution ID for batch retrieval of results. """
    global execution_id, stats
    # Defaults to timestamp if not given an execution ID
    execution_id = exe_id if exe_id is not None else format_time(time.time())
    stats = dict()


def get_execution_id():
    if execution_id is None:
        return ""
    else:
        return execution_id

def log_stats(data):
    global stats
    for key, value in data.items():
        if key in stats:
            stats[key] += value
        else:
            stats[key] = value

def print_stats():
    global execution_id, stats
    print("Execution ID: " + execution_id)
    print("Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
