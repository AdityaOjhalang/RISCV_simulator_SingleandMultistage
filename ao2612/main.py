import argparse
import os

from models import DataMem, InsMem
from rv32i_simulator import SingleStageCore

def process_test_case(test_case_path, output_path):
    # Instantiate memories with the path to the test case files
    imem = InsMem("Imem", test_case_path)
    dmem_ss = DataMem("SS", test_case_path)

    # Create the core simulation with the instruction and data memories
    # Pass the output_path to ensure that outputs are directed to the right folder
    ssCore = SingleStageCore(output_path, imem, dmem_ss)

    # Run the simulation
    while not ssCore.halted:
        ssCore.step()

    # Output the data memory and other results to the output directory
    dmem_ss.output_data_mem(output_path)
    ssCore.calculate_performance_metrics(output_path)

def main():
    # Create an argument parser for command-line options
    parser = argparse.ArgumentParser(description='RV32I processor')
    # The default path is 'input', which is at the same level as the script's directory
    parser.add_argument('--inputdir', default="input", type=str, help='Directory containing the input test cases.')
    args = parser.parse_args()

    # Obtain the absolute path to the script's parent directory (i.e., the 'IMPORTANT CODE' directory)
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Use the script's parent directory to build the correct paths for input and output directories
    input_dir = os.path.join(script_dir, args.inputdir)
    output_dir = os.path.join(script_dir, "output_ao2612")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each test case directory in the input directory
    for test_case in os.listdir(input_dir):
        test_case_path = os.path.join(input_dir, test_case)

        # Check if the path is a directory to ignore files like .DS_Store
        if os.path.isdir(test_case_path):
            test_case_output_path = os.path.join(output_dir, test_case)
            
            # Ensure the output directory for this test case exists
            os.makedirs(test_case_output_path, exist_ok=True)

            print(f"Processing {test_case}")
            process_test_case(test_case_path, test_case_output_path)
            print(f"Results for {test_case} saved in {test_case_output_path}")
        else:
            print(f"Ignoring file {test_case}")

if __name__ == "__main__":
    main()

