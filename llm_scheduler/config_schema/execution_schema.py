import json
from enum import Enum


class Config(object):
    """
    Base class for config parser.

    Children should define the following functions:
    - from_json(json_dict: dict) -> None: Initialize from json
    - to_json() -> str: Serialize to json
    """

    def __init__(self) -> None:
        pass

    def from_bytes(self, data: bytes) -> None:
        if data is not None: # Initialize from json
            self.from_json(json.loads(data))
        return self

    def to_bytes(self) -> bytes:
        return bytes(self.to_json(), "utf-8")

    def __str__(self) -> str:
        return self.to_json()


class DataConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.payload = dict()

    def from_json(self, json_dict: dict) -> None:
        if isinstance(json_dict, dict):
            self.payload = json_dict["payload"]
            return self
        else:
            return self.from_bytes(json_dict)

    def to_json(self) -> str:
        json_dict = dict()
        json_dict["payload"] = self.payload
        return json.dumps(json_dict, indent=4)


class ModelQueryConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.model_key = ""
        self.parameters = dict()
        self.system_prompt = ""
        self.user_prompt = ""

    def from_json(self, json_dict: dict) -> None:
        if isinstance(json_dict, dict):
            self.model_key = json_dict["model_key"]
            self.parameters = json_dict["parameters"]
            self.system_prompt = json_dict["system_prompt"]
            self.user_prompt = json_dict["user_prompt"]
            return self
        else:
            return self.from_bytes(json_dict)

    def interpolate_strings(self, next_step_inputs: DataConfig) -> None:
        for varname in next_step_inputs.payload:
            # TODO(yaoyiheng): Handle interpolation with a separate lib to sync with encoding.
            self.user_prompt = self.user_prompt.replace(f"%{varname}%", next_step_inputs.payload[varname])
            self.system_prompt = self.system_prompt.replace(f"%{varname}%", next_step_inputs.payload[varname])

    def to_json(self) -> str:
        json_dict = dict()
        json_dict["model_key"] = self.model_key
        json_dict["parameters"] = self.parameters
        json_dict["system_prompt"] = self.system_prompt
        json_dict["user_prompt"] = self.user_prompt
        return json.dumps(json_dict, indent=4)


class FunctionCallConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.function_name = ""
        self.request = "" # JSON-formatted string

    def from_json(self, json_dict: dict) -> None:
        if isinstance(json_dict, dict):
            self.function_name = json_dict["function_name"]
            self.request = json_dict["request"]
            return self
        else:
            return self.from_bytes(json_dict)

    def interpolate_strings(self, next_step_inputs: DataConfig) -> None:
        for varname in next_step_inputs.payload:
            # TODO(yaoyiheng): Handle interpolation with a separate lib to sync with encoding.
            self.request = self.request.replace(f"%{varname}%", next_step_inputs.payload[varname])

    def to_json(self) -> str:
        json_dict = dict()
        json_dict["function_name"] = self.function_name
        json_dict["request"] = self.request
        return json.dumps(json_dict, indent=4)


class Metadata(Config):
    def __init__(self) -> None:
        super().__init__()
        self.timestamp = 0
        self.source = ""
        self.version = ""

    def from_json(self, json_dict: dict) -> None:
        if isinstance(json_dict, dict):
            self.timestamp = json_dict["timestamp"]
            self.source = json_dict["source"]
            self.version = json_dict["version"]
            return self
        else:
            return self.from_bytes(json_dict)

    def to_json(self) -> str:
        json_dict = dict()
        json_dict["timestamp"] = self.timestamp
        json_dict["source"] = self.source
        json_dict["version"] = self.version
        return json.dumps(json_dict, indent=4)


class StepConfig(Config):
    class StepType(Enum):
        STEP_TYPE_MODEL_QUERY = 0
        STEP_TYPE_FUNCTION_CALL = 1

    def __init__(self) -> None:
        super().__init__()
        self.id = 0
        self.name = ""
        self.description = ""
        self.step_type = StepConfig.StepType.STEP_TYPE_MODEL_QUERY
        self.input_config = DataConfig()
        self.model_query_config = ModelQueryConfig()
        self.function_call_config = FunctionCallConfig()
        self.output_config = DataConfig()
        self.metadata = Metadata()

    def from_json(self, json_dict: dict) -> None:
        if isinstance(json_dict, dict):
            self.id = json_dict["id"]
            self.name = json_dict["name"]
            self.description = json_dict["description"]
            self.step_type = StepConfig.StepType(json_dict["step_type"])
            self.input_config.from_json(json_dict["input_config"])
            self.model_query_config.from_json(json_dict["model_query_config"])
            self.function_call_config.from_json(json_dict["function_call_config"])
            self.output_config.from_json(json_dict["output_config"])
            self.metadata.from_json(json_dict["metadata"])
            return self
        else:
            return self.from_bytes(json_dict)

    def interpolate_strings(self, next_step_inputs: DataConfig) -> None:
        self.model_query_config.interpolate_strings(next_step_inputs)
        self.function_call_config.interpolate_strings(next_step_inputs)

    def to_json(self) -> str:
        json_dict = dict()
        json_dict["id"] = self.id
        json_dict["name"] = self.name
        json_dict["description"] = self.description
        json_dict["step_type"] = self.step_type.value
        json_dict["input_config"] = self.input_config.to_json()
        json_dict["model_query_config"] = self.model_query_config.to_json()
        json_dict["function_call_config"] = self.function_call_config.to_json()
        json_dict["output_config"] = self.output_config.to_json()
        json_dict["metadata"] = self.metadata.to_json()
        return json.dumps(json_dict, indent=4)


class TaskConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.task_id = ""
        self.input_config = DataConfig()
        self.steps = []
        self.output_config = DataConfig()
        self.metadata = Metadata()
        # TODO(yaoyiheng): Add next_task field to enable graph execution mode

    def from_json(self, json_dict: dict) -> None:
        if isinstance(json_dict, dict):
            self.task_id = json_dict["task_id"]
            self.input_config.from_json(json_dict["input_config"])
            self.steps = [StepConfig().from_json(step) for step in json_dict["steps"]]
            self.output_config.from_json(json_dict["output_config"])
            self.metadata.from_json(json_dict["metadata"])
            return self
        else:
            return self.from_bytes(json_dict)

    def to_json(self) -> str:
        json_dict = dict()
        json_dict["task_id"] = self.task_id
        json_dict["input_config"] = self.input_config.to_json()
        json_dict["steps"] = [step.to_json() for step in self.steps]
        json_dict["output_config"] = self.output_config.to_json()
        json_dict["metadata"] = self.metadata.to_json()
        return json.dumps(json_dict, indent=4)


class JobConfig(Config):
    class Status(Enum):
        QUEUED = "queued"
        PENDING = "pending"
        RUNNING = "running"
        SUCCESS = "success"
        FAILED = "failed"

    def __init__(self) -> None:
        super().__init__()
        self.job_id = ""
        self.status = JobConfig.Status.QUEUED
        self.task_config = TaskConfig()
        self.metadata = Metadata()
    
    def from_json(self, json_dict: dict) -> None:
        if isinstance(json_dict, dict):
            self.job_id = json_dict["job_id"]
            self.status = JobConfig.Status(json_dict["status"])
            self.task_config.from_json(json_dict["task_config"])
            self.metadata.from_json(json_dict["metadata"])
            return self
        else:
            return self.from_bytes(json_dict)

    def to_json(self) -> str:
        json_dict = dict()
        json_dict["job_id"] = self.job_id
        json_dict["status"] = self.status.value
        json_dict["task_config"] = self.task_config.to_json()
        json_dict["metadata"] = self.metadata.to_json()
        return json.dumps(json_dict, indent=4)
