import argparse
from llm_scheduler.executor.builder import build_executor
from llm_scheduler.config_schema.execution_schema import StepConfig


def execute_step(step_config: StepConfig) -> str:
    print(f"Executing step: {step_config}")
    try:
        executor = build_executor(step_config)
        return executor.execute()
    except ValueError as e:
        raise ValueError(f"Failed to build executor: {e}")


def main():
    parser = argparse.ArgumentParser(description='Execute a single StepConfig')
    parser.add_argument('--input_path', type=str, help='Path to the json file')
    args = parser.parse_args()

    with open(args.input_path, 'rb') as f:
        data = f.read()

    step_config = StepConfig().from_bytes(data)

    print(execute_step(step_config))


if __name__ == '__main__':
    main()
