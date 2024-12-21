# top_n_ids
This project demonstrates how to process large datasets with FastAPI and Python. It includes an API for processing uploaded data and returning the top `n` numerical IDs with the highest numerical values. The project also includes a script to generate test data for use with the FastAPI app.

## Requirements
Before running the project, ensure that you have the following installed:
- Python 3.9 or higher
- pip (Python package installer)
- Make (for automation)

## Installation

### Step 1: Clone the repository

If you haven't already, clone the project to your local machine:

```bash
git clone https://github.com/victagne/top_n_ids.git
cd top_n_ids
```

### Step 2: Set up the virtual environment

It is recommended to use a virtual environment to manage the project's dependencies:

```bash
python3 -m venv .venv
```
### Step 3: Activate the virtual environment

Activate the virtual environment:

- On Linux/macOS:
```bash
source .venv/bin/activate
```

- On Windows:
```bash
.\.venv\Scripts\activate
```

### Step 4: Install required dependencies

Install the necessary Python packages by running:
```bash
pip install -r requirements.txt
```
Make sure that `requirements.txt` includes the necessary dependencies like `fastapi`, `uvicorn`, and any other libraries used in the project.

## Usage
### Step 1: Generate test data
The `data_generator.py` script generates test data that can be used with the FastAPI application. You can generate data using the `make` command.
By default, the data will be generated in the `data` directory.

To generate data, run:
```bash
make generate
```
By default, this will create 100 files, each with 10_000_000 lines of random data in the format `<numerical_id>_<numerical_value>` where `numerical_id` is self-incrementing and `numerical_value` is sampled randomly between 1 and 100000 inclusively. All data files are stored in the `data` directory.

### Step 2: Run the FastAPI app
To start the FastAPI application, run:
```bash
make run
```
This will start the FastAPI app on `http://127.0.0.1:8000`. The app is set to reload automatically if any changes are made to the code.

### Step 3: Make a POST request to the FastAPI endpoint
You can make a `POST` request to the FastAPI endpoint `/top_n_ids/` using the make request command.
By default, it will request the top 3 numerical IDs, but you can specify the value of `N` as a parameter. For example, to request the top 5 IDs:
```bash
make request N=5
```
This will send a POST request to `http://127.0.0.1:8000/top_n_ids/` with the specified value 5 of `N`.
Logs can be viewed directly in the FastAPI terminal.

### Step 4: Clean up generated data
To remove the generated data files and the `data` directory, run:
```bash
make clean
```

## Makefile Targets
- `make run`: Starts the FastAPI application.
- `make generate`: Generates test data using the `data_generator.py` script.
- `make request N=<number>`: Sends a `POST` request to the FastAPI app with the specified `N` value to get the top `N` numerical IDs.
- `make clean`: Cleans up the generated data files.

## Example Flow
### 1. Generate data:
```bash
make generate
```

### 2. Start the FastAPI application:
```bash
make run
```

### 3. Make a request (default x=3):
```bash
make request
```
This command should be run in another terminal.

## Discussion

### Technical Implementation Details
- **Multiprocessing**: In this project, we use 4 processes (workers) to process data concurrently. By default, it is 4, but we can adjust the number of processes according to the hardware, or not specify the number of processes and let the program decide for itself. This approach helps in splitting the work across multiple processes, speeding up the overall execution for tasks such as sorting or finding the top `N` numerical IDs.
- **min-heap**: `min-heap` is used to efficiently maintain the smallest of the top `N` numerical values. Each process has its own `min-heap`, finally we merge all of them into a global `min-heap`. When a new value is processed, the program checks if the heap size exceeds `N`. If it does, the smallest value is removed, ensuring that the heap always holds the top `N` values. This operation is performed in logarithmic time (`O(log N)`), which is efficient even for large datasets.
- **File Processing**: Files are processed in chunks to manage memory usage efficiently and fewer file IO operations. By reading files in chunks (typically 1 MB each), only a small portion of the file is kept in memory at any time, making it feasible to process large files without consuming too much memory. In addition, compared with line-by-line reading, although chunk-reading consumes a little more memory, it can significantly reduce the number of file pointer movements, making I/O more efficient.
- **Time Complexity**: The time complexity for processing each file chunk is `O(C * log N)`, where `C` is chunk size and `N` is the number of top results we want to calculate. For `M` chunks, the overall time complexity is `O(M * C * log N)` (where `M` is the number of chunks). The `log N` factor comes from heap operations, and the total number of chunks is proportional to the size of the file divided by the chunk size.
- **Space Complexity**: The space complexity is dominated by the size of the `min-heap`, which stores at most `N` elements. Therefore, the space complexity is `O(N)` for each process. Given that data is processed in parallel, the space complexity per process remains manageable even for large datasets. The file is processed in chunks, so only a small portion of the file is kept in memory at any given time.
- **Disk Space**: The amount of disk space used depends on the size of the generated data files. Each file has the format `<numerical_id>_<numerical_value>`, which will require disk space proportional to the number of lines and the size of each line in the file. The `data_generator.py` script generates a large amount of test data, with each file containing up to 10,000,000 lines. The total disk usage is primarily based on the number of generated files and the size of each line in the file. For example, generating 100 files with 10,000,000 lines each, which means 1B rows in total. Each line has around 15 characters, it will occupy approximately `100 * 150MB ≈ 14.65GB` of disk space.

## Potential Optimizations
- **Dynamic Worker Allocation**： The number of workers is currently fixed to the number 4, or the number of CPU cores if we don't specify pool size. In real scenario, dynamically adjusting the pool size based on data size, system load and available resources could enhance performance.
- **Distributed Processing:**: Integrating distributed systems like Apache Spark to handle processing across a cluster of machines.

## Conclusion
This project demonstrates how to work with FastAPI, including creating endpoints, and processing data efficiently. The `Makefile` simplifies the process of running the app, generating test data, and making requests to the FastAPI API to get top `N` ids.

## Author
- Lifeng Wan
- lifeng.wan.mtl@gmail.com