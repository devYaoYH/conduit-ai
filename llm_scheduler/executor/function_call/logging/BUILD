package(default_visibility = ["//visibility:public"])

load("@moral_machines_pip_deps//:requirements.bzl", "requirement")

py_library(
    name = "logging",
    srcs = ["gcp_firestore_log.py"],
    deps = [
        "//llm_scheduler/execution_environment",
        requirement("google-cloud-firestore"),
    ],
)
