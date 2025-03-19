package(default_visibility = ["//visibility:public"])

py_library(
    name = "runner",
    srcs = [
        "step_runner.py",
        "task_runner.py",
    ],
    deps = [
        "//llm_scheduler/config_schema",
        "//llm_scheduler/executor:builder",
        "//llm_scheduler/execution_environment",
    ],
)

py_binary(
    name = "step_runner",
    srcs = ["step_runner.py"],
    deps = [
        ":runner",
    ],
    python_version = "PY3",
)

py_binary(
    name = "task_runner",
    srcs = ["task_runner.py"],
    deps = [
        ":runner",
    ],
    python_version = "PY3",
)
