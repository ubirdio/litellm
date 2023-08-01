#### What this tests ####
#    This tests error logging (with custom user functions) for the `completion` + `embedding` endpoints w/ callbacks

import sys, os
import traceback
import pytest

sys.path.insert(0, os.path.abspath('../..'))  # Adds the parent directory to the system path
import litellm
from litellm import embedding, completion

litellm.success_callback = ["posthog"]
litellm.failure_callback = ["slack", "sentry", "posthog"]

# litellm.set_verbose = True

def logger_fn(model_call_object: dict):
    # print(f"model call details: {model_call_object}")
    pass

user_message = "Hello, how are you?"
messages = [{ "content": user_message,"role": "user"}]

def test_completion_openai():
    try:
        response = completion(model="updated-model", messages=messages, logger_fn=logger_fn)
        # Add any assertions here to check the response
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

def test_completion_non_openai():
    try:
        response = completion(model="claude-instant-1", messages=messages, logger_fn=logger_fn)
        # Add any assertions here to check the response
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

def test_embedding_openai():
    try:
        response = embedding(model='updated-model', input=[user_message], logger_fn=logger_fn)
        # Add any assertions here to check the response
        print(f"response: {str(response)[:50]}")
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")

def test_bad_azure_embedding():
    try:
        response = embedding(model='chatgpt-test', input=[user_message], logger_fn=logger_fn)
        # Add any assertions here to check the response
        print(f"response: {str(response)[:50]}")
    except Exception as e:
        pass
def test_good_azure_embedding():
    try:
        response = embedding(model='azure-embedding-model', input=[user_message], azure=True, logger_fn=logger_fn)
        # Add any assertions here to check the response
        print(f"response: {str(response)[:50]}")
    except Exception as e:
        pytest.fail(f"Error occurred: {e}")
