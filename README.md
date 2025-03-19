# LLM Agent Executor

Chain LLM tasks together by specifying configuration files in JSON:

1. Each STEP in a task is a separate LLM call.

```json
{
    "id": "1",
    "name": "sample",
    "description": "A sample StepConfig",
    "step_type": 0,
    "input_config": {
        "payload": {
            "user_prompt": "Tell me a joke!",
            "system_prompt": "You're a funny assistant."
        }
    },
    "model_query_config": {
        "model_key": "GEMINI_FLASH",
        "parameters": {
            "temperature": "0.7"
        },
        "system_prompt": "You are a helpful assistant.",
        "user_prompt": "%user_prompt%" // Interpolate input variables into model query
    },
    "output_config": {
        "payload": {
            "user_prompt": "Hahaha"
        }
    },
    "metadata": {
        "timestamp": 1741667405,
        "source": "create_sample",
        "version": "1.0"
    }
}
```

2. Each TASK is a self-contained sequence of Steps. What this means is a linear sequence of data processing operations with no branching. The task can have a next task to indicate the next task in the chain, but cannot be itself (no looping yet).

```json
{
    "task_id": "",
    "input_config": {
        "payload": {}
    },
    "steps": [...], // List of Step configurations
    "output_config": {
        "payload": {}
    },
    "metadata": {
        "timestamp": 1741667405,
        "source": "create_sample",
        "version": "1.0"
    },
    "next_task": "" // ID linked to next task
}
```

3. Each job execution starts from a task and executes the DAG of tasks implicitly specified.

- Each 'job' will be triggered by serverless functions so isn't actually running a graph search per se. Task executions will be triggered based on commits of task configurations to a database.

## Debugging Usage

Config generation scripts are provided in `/proto_decoder` for quick prototyping.

First one needs to prepare requirements for pypi external dependencies using [pip-tools](https://pypi.org/project/pip-tools/):

```
pip install pip-tools
pip-compile requirements.in
```

Bazel should be installed following instructions here: https://bazel.build/install.

Build and run sepcific scripts such as `create_sample.py`, `config_reader.py`, `step_runner.py`, and `task_runner.py` using the `bazel run` command:

```
bazel run //llm_scheduler/config_tools:create_sample -- -output_dir=''

bazel run //llm_scheduler/config_tools:config_reader -- -input_path='job.json' -config_type=job

bazel run //llm_scheduler/runner:step_runner -- -input_path='step.json'

bazel run //llm_scheduler/runner:task_runner -- -input_path='task.json'
```

The default sample task just chains the output of the first step into the next step in 2 LLM calls.
