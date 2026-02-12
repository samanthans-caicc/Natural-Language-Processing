try:
    import openai
    print(f"OpenAI is installed. Version: {openai.__version__}")
except ImportError:
    print("OpenAI is not installed or not found in the current Python environment.")
except Exception as e:
    print(f"An error occurred: {e}")
