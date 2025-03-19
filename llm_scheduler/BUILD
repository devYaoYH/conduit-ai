package(default_visibility = ["//visibility:public"])

load("@moral_machines_pip_deps//:requirements.bzl", "requirement")  # Updated pip deps name

# TODO(yaoyiheng): Package and deploy to GCP Cloud Function endpoint
# This is the main entrypoint for the Cloud Function binary
py_binary(
    name = "main",
    srcs = ["main.py"],
    deps = [
        "//llm_scheduler/config_schema",
        "//llm_scheduler/executor",
        "//llm_scheduler/runner",
    ],
    python_version = "PY3",
)
