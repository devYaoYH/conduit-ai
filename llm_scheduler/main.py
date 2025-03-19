import argparse
from llm_scheduler.config_schema.execution_schema import TaskConfig
from llm_scheduler.runner.task_runner import execute_task


def process_request(request):
    """Cloud Function entry point that handles HTTP requests."""

    # Parse request data
    request_json = request.get_json()

    task_config = TaskConfig().from_json(request_json.get('task_config'))

    result = execute_task(task_config)

    return result


def main():
    parser = argparse.ArgumentParser(description='Execute a single TaskConfig')
    parser.add_argument('-input_path', type=str, help='Path to the json file')
    args = parser.parse_args()
    
    with open(args.input_path, 'rb') as f:
        data = f.read()

    task_config = TaskConfig().from_bytes(data)

    print(execute_task(task_config))


if __name__ == '__main__':
    main()
