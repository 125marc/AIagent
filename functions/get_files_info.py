import os

def get_files_info(working_directory, directory="."):
    if directory == None:
        return f"Error: Must enter a directory"
    if os.path.isdir(os.path.join(working_directory, directory)):
        if not os.path.abspath(os.path.join(working_directory, directory)).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        else:
            list_of_file_info = []
            for item in os.listdir(os.path.join(working_directory, directory)):
                list_of_file_info.append(f"- {item}: file_size: {os.path.getsize(os.path.join(working_directory, directory,item))} bytes, is_dir={os.path.isdir(os.path.join(working_directory, directory,item))}")
            file_info ="\n".join(list_of_file_info)
            return file_info
    
    else:
        return f'Error: "{directory}" is not a directory'
    

