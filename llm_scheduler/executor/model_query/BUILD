package(default_visibility = ["//visibility:public"])

load("@moral_machines_pip_deps//:requirements.bzl", "requirement")

py_library(
    name = "model_query",
    srcs = [
        "gemini_executor.py",
        "claude_executor.py",
    ],
    deps = [
        "//llm_scheduler/config_schema",
        "//llm_scheduler/executor:executor",
        requirement("anthropic"),
        requirement("google-genai"),
    ],
)
