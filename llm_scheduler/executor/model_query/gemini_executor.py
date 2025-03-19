import os
import time
from google import genai
from llm_scheduler.executor.executor import ModelQueryExecutor
from llm_scheduler.config_schema.execution_schema import ModelQueryConfig


GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

class GeminiExecutor(ModelQueryExecutor):
    def __init__(self, model_query_config: ModelQueryConfig):
        super().__init__(model_query_config)
        self.backoff_time = 0.2
        self.retry_attempts_remaining = 5
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def execute(self) -> str:
        print(f"Executing query: {self} {self.model_query_config.user_prompt}")
        try:
            model_config = self.model_query_config.parameters
            model_config["system_instruction"] = self.model_query_config.system_prompt
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=self.model_query_config.user_prompt,
                config=model_config,
            )
        except Exception as e:
            print(f"Error executing query: {e}")
            if self.retry_attempts_remaining > 0:
                time.sleep(self.backoff_time)
                self.retry_attempts_remaining -= 1
                self.backoff_time *= 2
                return self.execute()
            else:
                raise ValueError("Failed to execute query after multiple retries.")
        return response.text
