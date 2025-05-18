import os
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_all_tests(folder_path):
    if not os.path.isdir(folder_path):
        logger.error(f"Folder {folder_path} does not exist")
        return
    
    # Get all .py files starting with 'tc'
    test_files = [f for f in os.listdir(folder_path) if f.startswith('tc') and f.endswith('.py')]
    test_files.sort()
    
    if not test_files:
        logger.warning(f"No test files found in {folder_path}")
        return
    
    for test_file in test_files:
        file_path = os.path.join(folder_path, test_file)
        logger.info(f"Running test: {test_file}")
        try:
            result = subprocess.run(['python', file_path], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"{test_file} completed successfully")
                print(f"{test_file}: Success\n{result.stdout}")
            else:
                logger.error(f"{test_file} failed with exit code {result.returncode}")
                print(f"{test_file}: Failed\n{result.stderr}")
        except Exception as e:
            logger.error(f"Error running {test_file}: {str(e)}")
            print(f"{test_file}: Error - {str(e)}")
        
        # Small delay to ensure browser/resources are released
        logger.info("Waiting 2 seconds before next test")
        import time
        time.sleep(2)

if __name__ == "__main__":
    # Specify the folder containing test files
    test_folder = "AutomationTesting"
    run_all_tests(test_folder)