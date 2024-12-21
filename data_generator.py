import random
import os
import time
from multiprocessing import Pool

# Number of lines per file
LINES_PER_FILE = 10_000_000
# Total number of files to generate
TOTAL_FILES = 100
# Output directory
OUTPUT_DIR = "data"

def generate_file(file_index: int):
    # Ensure the output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    output_file = os.path.join(OUTPUT_DIR, f"data_{file_index}.txt")
    start_id = file_index * LINES_PER_FILE + 1

    start_time = time.time()  # Start time for file generation

    with open(output_file, 'w') as f:
        for i in range(LINES_PER_FILE):
            numerical_id = start_id + i
            numerical_value = random.randint(1, 100000)  # Random numerical value
            f.write(f"{numerical_id}_{numerical_value}\n")

    end_time = time.time()  # End time for file generation
    print(f"File {output_file} generated. Time taken: {end_time - start_time:.2f} seconds.")


# Main function
def main():
    # Start time for overall data generation
    overall_start_time = time.time()

    print(f"Starting data generation at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(overall_start_time))}")

    # Use multiprocessing to generate files in parallel
    with Pool(4) as pool:  # 4 workers
        pool.map(generate_file, range(TOTAL_FILES))

    # End time for overall data generation
    overall_end_time = time.time()
    print(f"Data generation completed at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(overall_end_time))}")
    print(f"Total time taken: {overall_end_time - overall_start_time:.2f} seconds.")


if __name__ == "__main__":
    main()
