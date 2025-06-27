import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file




load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of the file, truncates the file at 10,000 charactors, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that will be read, return errors if the file cannot be read.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Test to see if a file is a python file, run the file if it is.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file that will be run, return errors if the file cannot be read, or if it is not a python file",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Check to see if a file exist, if it does, write to it. If it does not, create the file and write to it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that will be written to, return errors if the file cannot be processed.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written to a file.",
            ),
        },
    ),
)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
    ]
)

user_prompt = sys.argv

if len(sys.argv) < 2:
    print("Error")
    sys.exit(1)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Call get_files_content function
- Call get_files_info function
- Call run_python function
- Call write_file function

You are able to call these functions multiple times until you have a definitive answer

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt[1])]),
]

client = genai.Client(api_key=api_key)
model_name = "gemini-2.0-flash-001"
response = client.models.generate_content(
    model=model_name,
    contents=messages, config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt)
)

#response = client.models.generate_content(model = "gemini-2.0-flash-001", contents = messages)
def call_function(function_call_part, verbose=False):
    if "--verbose" in user_prompt:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(f" - Calling function: {function_call_part.name}")
    my_functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }
    kwargs = function_call_part.args
    kwargs["working_directory"] = "./calculator"
    if function_call_part.name not in my_functions:
        return types.Content(
                    role="tool",
                     parts=[
                        types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                        )
                    ],
                )
    else:
        called_function = my_functions[function_call_part.name](**kwargs,)
        contents = types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"result": called_function},
                        )
                    ],
                )
        if contents.parts[0].function_response.response is None:
            raise Exception("No function response")
        if "--verbose" in user_prompt:
            return f"-> {contents.parts[0].function_response.response}"
        return contents
    



if "--verbose" in user_prompt:
    print(f"User prompt: {sys.argv[1]}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    function_call_part = response.function_calls
    if response.function_calls:
    # Handle function calls here
        for function_call_part in response.function_calls:
            # Actually perform the function call!
            print(call_function(function_call_part, "--verbose" in user_prompt))
else:
    for i in range(21):
        for item in response.candidates:
            messages.append(item.content)
        if response.function_calls:
    # Collect all function responses for this turn
            tool_parts = []
            for function_call_part in response.function_calls:
                contents = call_function(function_call_part, "--verbose" in user_prompt)
                tool_parts.append(
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"result": contents},
                        )
                     )
    
                # Create one Content object with all the function responses
            content_for_messages = types.Content(
                role="tool",
                parts=tool_parts
            )
            messages.append(content_for_messages)
        else:
            print(response.text)
            break
        response = client.models.generate_content(
                model=model_name,
                contents=messages, config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt)
            )

    


