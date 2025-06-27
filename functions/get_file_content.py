import os

def get_file_content(working_directory, file_path):

    abs_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    MAX_CHARS = 10000
    try:
        with open(abs_path, "r") as f:
            file_content_string = f.read()
            if len(file_content_string) > MAX_CHARS:
                return f"{file_content_string[:MAX_CHARS]}" + f"[...File \"{file_path}\" truncated at 10000 characters]"
            return file_content_string
    except Exception as e:
        return f"Error, unable to read file {file_path}"
