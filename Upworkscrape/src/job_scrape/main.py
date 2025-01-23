import sys
from crew import Upworkscrapecrew
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def run():
    # keywords =['Agennts','Agents','AI']
    result = Upworkscrapecrew().crew().kickoff()
    # Debugging: Print the result directly
    print("Result received:")
    print(result)  # Show the raw result

def train():
    # inputs = get_file_inputs()

    if len(sys.argv) > 2:
        iterations = int(sys.argv[2])
    else:
        raise ValueError("Number of iterations not provided.")
    
    try:
        print("Training started...")
        Upworkscrapecrew().crew().train(n_iterations=iterations, inputs=inputs)
        print("Training complete.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while training the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "train":
        train()
    else:
        run()
