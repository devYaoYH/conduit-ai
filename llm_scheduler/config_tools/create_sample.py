import os
import time
import argparse
from llm_scheduler.config_schema.execution_schema import ModelQueryConfig, StepConfig, TaskConfig, JobConfig, FunctionCallConfig

def create_sample_step_config():
    config = StepConfig()
    config.id = "1"
    config.name = "sample"
    config.description = "A sample StepConfig"
    config.step_type = StepConfig.StepType.STEP_TYPE_MODEL_QUERY
    
    # Set input configuration
    input_config = config.input_config
    input_config.payload["user_prompt"] = "Tell me a joke!"
    input_config.payload["system_prompt"] = "You're a funny assistant."

    # Set ModelQueryConfig
    model_query_config = config.model_query_config
    model_query_config.model_key = "GEMINI_FLASH"
    model_query_config_params = model_query_config.parameters
    model_query_config_params["temperature"] = "0.7"
    model_query_config.system_prompt = "%system_prompt%"
    model_query_config.user_prompt = "%user_prompt%"

    # Set output configuration
    output_config = config.output_config
    output_config.payload["user_prompt"] = "Hahaha"

    # Set metadata
    config.metadata.timestamp = round(time.time())
    config.metadata.source = "create_sample"
    config.metadata.version = "1.0"

    return config


def create_sample_function_call_config():
    config = create_sample_step_config()
    config.description = "A sample FunctionCall StepConfig"
    config.step_type = StepConfig.StepType.STEP_TYPE_FUNCTION_CALL
    config.model_query_config = ModelQueryConfig()
    config.function_call_config.function_name = "gcp_firestore_log"
    config.function_call_config.request = '%data%'
    return config


def create_sample_task_config():
    config = TaskConfig()
    config.id = "t1"
    config.name = "sample_task"
    config.description = "A sample TaskConfig"

    config.input_config.payload["user_prompt"] = "Tell me a joke!"
    config.input_config.payload["system_prompt"] = "You're a funny assistant."

    initial_step = create_sample_step_config()
    explanation_step = create_sample_step_config()
    data_extraction_step = create_sample_step_config()

    explanation_step.model_query_config.user_prompt = "Explain the following joke to me:\n\n%context%\n\nChoose whether the joke is funny or not and output either FUNNY or DULL enclosed with <answer></answer> tags."
    explanation_step.model_query_config.system_prompt = "You are a undertaker with a bad temper and no sense of humor."

    data_extraction_step.model_query_config.user_prompt = "Extract whether the verdict is FUNNY or DULL from the following explanation:\n\n%context%\n\nOutput a single word FUNNY or DULL."
    data_extraction_step.model_query_config.system_prompt = "You are an expert data analyst working on cleaning datasets. Sometimes the required information will be presented in tags like <answer></answer> and you'll need to extract it. Othertimes the data might be slightly malformed and you'll have to infer the answer from the given data. Strictly follow the output format rules."

    config.steps = [initial_step, explanation_step, data_extraction_step]

    # Set metadata
    config.metadata.timestamp = round(time.time())
    config.metadata.source = "create_sample"
    config.metadata.version = "1.0"

    return config


def create_sample_job_config():
    config = JobConfig()
    config.id = "j1"
    config.name = "sample_job"
    config.description = "A sample JobConfig"
    config.status = JobConfig.Status.QUEUED
    config.task_config = create_sample_task_config()

    # Set metadata
    config.metadata.timestamp = round(time.time())
    config.metadata.source = "create_sample"
    config.metadata.version = "1.0"

    return config

def main():
    parser = argparse.ArgumentParser(description='Create a sample StepConfig protobuf message')
    parser.add_argument('-output_dir', type=str, help='Output directory where the json config files should be written')
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(args.output_dir)), exist_ok=True)

    gen_config_list = {
        "step_config": create_sample_step_config(),
        "function_call_config": create_sample_function_call_config(),
        "task_config": create_sample_task_config(),
        "job_config": create_sample_job_config(),
    }

    for config_name, config in gen_config_list.items():
        config_path = args.output_dir + f"/sample_{config_name}.json"
        # Serialize to file
        with open(config_path, "w") as f:
            f.write(str(config))
        print(f"Created sample {config_name} json file at: {config_path}")

if __name__ == "__main__":
    main()
