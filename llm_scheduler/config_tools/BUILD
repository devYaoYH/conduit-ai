package(default_visibility = ["//visibility:public"])

py_library(
    name = "config_tools",
    srcs = ["config_reader.py", "create_sample.py"],
    deps = [
        "//llm_scheduler/config_schema",
    ],
)

py_binary(
    name = "config_reader",
    srcs = ["config_reader.py"],
    deps = [
        "//llm_scheduler/config_schema",
    ],
    python_version = "PY3",
)

py_binary(
    name = "create_sample",
    srcs = ["create_sample.py"],
    deps = [
        "//llm_scheduler/config_schema",
    ],
    python_version = "PY3",
)
