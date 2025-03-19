from llm_scheduler.executor.executor import FunctionCallExecutor
from llm_scheduler.config_schema.execution_schema import FunctionCallConfig

# Register built-in functions below
# TODO(yaoyiheng): One of which will be triggering another custom
#                  cloud function for full flexibility
from llm_scheduler.executor.function_call.logging.gcp_firestore_log import gcp_firestore_log


class FunctionExecutor(FunctionCallExecutor):
    def __init__(self, function_call_config: FunctionCallConfig):
        super().__init__(function_call_config)

    def execute(self) -> str:
        print(f"Executing function: {self.function_call_config}")
        match self.function_call_config.function_name:
            case "gcp_firestore_log":
                return gcp_firestore_log(self.function_call_config.request)
        return "Function call executed"
