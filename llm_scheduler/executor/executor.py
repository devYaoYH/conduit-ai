from llm_scheduler.config_schema.execution_schema import ModelQueryConfig, FunctionCallConfig

class Executor(object):
    """Base class for all executors."""

    def execute(self) -> str:
        """Execute the configured operation and return the result as a string."""
        pass


class ModelQueryExecutor(Executor):
    """Base class for model query executors."""

    def __init__(self, model_query_config: ModelQueryConfig):
        self.model_query_config = model_query_config


class FunctionCallExecutor(Executor):
    """Base class for function call executors."""

    def __init__(self, function_call_config: FunctionCallConfig):
        self.function_call_config = function_call_config
