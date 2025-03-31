import anthropic
import os
import time
from llm_scheduler.executor.executor import ModelQueryExecutor
from llm_scheduler.config_schema.execution_schema import ModelQueryConfig
from llm_scheduler.execution_environment.execution_environment import log_stats


ANTHROPIC_API_KEY = os.environ['ANTHROPIC_API_KEY']

class ClaudeExecutor(ModelQueryExecutor):
    def __init__(self, model_query_config: ModelQueryConfig):
        super().__init__(model_query_config)
        self.backoff_time = 0.2
        self.retry_attempts_remaining = 5
        self.client = anthropic.Anthropic(
            api_key=ANTHROPIC_API_KEY,
        )

    def execute(self) -> str:
        print(f"Executing query: {self} {self.model_query_config.user_prompt}")

        print(**self.model_query_config.parameters)

        try:
            response = self.client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": self.model_query_config.user_prompt}
                ],
                system=self.model_query_config.system_prompt,
                **self.model_query_config.parameters
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
        log_stats({
            "num_claude_output_tokens": response.usage.output_tokens,
            "num_claude_calls": 1,
        })

        # Look for text content in response
        for content in response.content:
            if content.type == "text":
                return content.text
        return str(response.content)
