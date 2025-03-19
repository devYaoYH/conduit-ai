import argparse
import llm_scheduler.execution_environment.execution_environment as env
from llm_scheduler.runner.step_runner import execute_step
from llm_scheduler.config_schema.execution_schema import StepConfig, TaskConfig, DataConfig


def prepare_input(previous_outputs: DataConfig, step_config: StepConfig) -> None:
    if previous_outputs is not None:
        next_step_inputs = step_config.input_config
        for varname in next_step_inputs.payload:
            try:
                # This should look something like:
                # extract_data(next_step_inputs.input_config[varname], previous_outputs)
                # which will mutate a next_step_inputs.input_config[varname] DataPacket config
                next_step_inputs.payload[varname] = previous_outputs.payload[varname]
            except KeyError as e:
                print(f"[Warning] Variable {varname} not found in previous outputs")
        # Pass-through context from previous output
        if "context" in previous_outputs.payload:
            next_step_inputs.payload["context"] = previous_outputs.payload["context"]

    # TODO(yaoyiheng): Interpolate strings for the function call step as well
    # Interpolate strings in the model query step configuration
    if step_config.step_type == StepConfig.StepType.STEP_TYPE_MODEL_QUERY:
        step_config.model_query_config.interpolate_strings(next_step_inputs)
    elif step_config.step_type == StepConfig.StepType.STEP_TYPE_FUNCTION_CALL:
        step_config.function_call_config.interpolate_strings(next_step_inputs)


def extract_output(response: str, step_config: StepConfig) -> DataConfig:
    next_step_outputs = DataConfig()
    for varname in step_config.output_config.payload:
        # Pass-through unused inputs to outputs
        if varname in step_config.input_config.payload:
            next_step_outputs.payload[varname] = step_config.input_config.payload[varname]
        else:
            # TODO(yaoyiheng): Actual data extraction may be requied based on the dataType
            next_step_outputs.payload[varname] = response
    # Always append current response to output payload
    if "context" in step_config.input_config.payload:
        next_step_outputs.payload["context"] = step_config.input_config.payload["context"] + "\n\n" + response
    else:
        next_step_outputs.payload["context"] = response
    return next_step_outputs


def execute_task(task_config: TaskConfig) -> str:
    print(f"Executing task: {task_config}")
    # The initial input is the task's input
    previous_outputs = task_config.input_config
    for step_config in task_config.steps:
        print(f"Step input: {previous_outputs}")
        # Insert outputs from previous step into input
        prepare_input(previous_outputs, step_config)
        # Run the step
        response = execute_step(step_config)
        print(f"Step response: {response}")
        # Extract the outputs
        previous_outputs = extract_output(response, step_config)
    # Extract the task output from final step_config
    # TODO(buggy): previous_outputs falls through implicitly from for-loop
    for varname in task_config.output_config.payload:
        if varname in previous_outputs.payload:
            task_config.output_config.payload[varname] = previous_outputs.payload[varname]


def main():
    parser = argparse.ArgumentParser(description='Execute a single TaskConfig')
    parser.add_argument('--input_path', type=str, help='Path to the json file')
    args = parser.parse_args()
    
    for file in args.input_path.split(","):
        with open(file, 'rb') as f:
            data = f.read()

        task_config = TaskConfig().from_bytes(data)

        print(execute_task(task_config))

        # Log to file task outputs
        with open(file + ".log", 'w') as f:
            f.write(task_config.output_config.to_json())


if __name__ == '__main__':
    env.init()
    main()
