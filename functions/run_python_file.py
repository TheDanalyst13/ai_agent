import os
import subprocess

def run_python_file(working_directory:str, file_path: str, args: list[str] | None = None) -> str:

    try:    
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python", target_dir]
            if args:
                command.extend(args)
            result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                rtn = f"Process exited with code {result.returncode}"
            else:
                rtn = ""
            if not result.stdout:
                if not result.stderr:
                    std = f"No output produced"
                else:
                    std = f"STDERR: {result.stderr}"
            elif result.stdout:
                if not result.stderr:
                    std = f"STDOUT: {result.stdout}"
                else:
                    std = f"STDOUT: {result.stdout}, STDERR: {result.stderr}"
            parts = []
            if rtn:
                parts.append(rtn)
            parts.append(std)
            return "\n".join(parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes or runs a specified .py file and returns its output, optionally accepting command-line arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "script path relative to the working directory"
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                },
            },
            "required": [
                "file_path",
            ],
        },
    },
}