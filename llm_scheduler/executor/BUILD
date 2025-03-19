package(default_visibility = ["//visibility:public"])

py_library(
    name = "executor",
    srcs = [
        "executor.py",
    ],
    deps = [
        "//llm_scheduler/config_schema",
    ],
)

py_library(
    name = "builder",
    srcs = [
        "builder.py",
    ],
    deps = [
        ":executor",
        "//llm_scheduler/config_schema",
        "//llm_scheduler/executor/model_query",
        "//llm_scheduler/executor/function_call",
    ],
)
