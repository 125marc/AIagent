import os
import subprocess

def run_python_file(working_directory, file_path):

    abs_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_path):
        return f'Error: File "{file_path}" not found.'
    _, extension = os.path.splitext(file_path)
    if extension != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    try:
        out_put = subprocess.run(["python", file_path], cwd=working_directory, capture_output=True, text=True, timeout=30)
        out_put_stdout = out_put.stdout
        out_put_stderr = out_put.stderr
        if out_put.returncode != 0:
            return f"STDOUT:{out_put_stdout}, STDERR:{out_put_stderr}, Process exited with code {out_put.returncode}"
        if out_put_stderr == '' and out_put_stderr == '':
            return "No outout produced."
        return f"STDOUT:{out_put_stdout}, STDERR:{out_put_stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"


    

    
    
