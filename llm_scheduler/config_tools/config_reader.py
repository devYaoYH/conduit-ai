import argparse
import sys
from llm_scheduler.config_schema.execution_schema import StepConfig, TaskConfig, JobConfig

def setup_args():
    parser = argparse.ArgumentParser(description='Decode and pretty print protocol buffers')
    parser.add_argument('-input_path', type=str, help='Path to the binary protobuf file')
    parser.add_argument('-config_type', type=str, choices=['step', 'task', 'job'], help='Type of the config message')
    return parser.parse_args()


def main():
    args = setup_args()

    try:
        # Read the binary protobuf file
        with open(args.input_path, 'rb') as f:
            data = f.read()
        
        # Parse the message based on type
        match args.config_type:
            case 'step':
                message = StepConfig().from_bytes(data)
            case 'task':
                message = TaskConfig().from_bytes(data)
            case 'job':
                message = JobConfig().from_bytes(data)
            case _:
                print(f"Error: Unknown config type {args.config_type}", file=sys.stderr)
                sys.exit(1)
        
        # Output based on format preference
        print(message)
            
    except FileNotFoundError:
        print(f"Error: Could not find file {args.input_path}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
