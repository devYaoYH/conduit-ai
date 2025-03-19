from llm_scheduler.config_schema.execution_schema import StepConfig
from llm_scheduler.executor.executor import Executor
from llm_scheduler.executor.model_query.gemini_executor import GeminiExecutor
from llm_scheduler.executor.function_call.function_executor import FunctionExecutor


def build_executor(step_config: StepConfig) -> Executor:
    """Build an executor based on the step configuration."""
    if step_config.step_type == StepConfig.StepType.STEP_TYPE_MODEL_QUERY:
        match step_config.model_query_config.model_key:
            case "GEMINI_FLASH":
                return GeminiExecutor(step_config.model_query_config)
            case _:
                raise ValueError(f"Unknown model key: {step_config.model_query_config.model_key}")
    elif step_config.step_type == StepConfig.StepType.STEP_TYPE_FUNCTION_CALL:
        return FunctionExecutor(step_config.function_call_config)
    else:
        raise ValueError(f"Unknown step type: {step_config.step_type}")
