import os
import heapq
import time
from multiprocessing import Pool
from typing import List, Tuple
from fastapi import FastAPI, Form, HTTPException

app = FastAPI()

CHUNK_SIZE = 1024 * 1024  # 1 MB per chunk

@app.post("/top_n_ids/")
async def get_top_n_ids(n: int = Form(...)):
    """
    Process all files in the 'data' folder using multiprocessing and return the top n numerical IDs which have the highest numerical values.
    """
    if n <= 0:
        raise HTTPException(status_code=400, detail="n must be a positive integer.")

    # Directory containing data files
    data_dir = "data"
    if not os.path.exists(data_dir):
        raise HTTPException(status_code=404, detail=f"Directory '{data_dir}' not found.")

    # Get all data file into a list
    data_files = [os.path.join(data_dir, fname) for fname in os.listdir(data_dir) if fname.startswith("data_")]

    if not data_files:
        raise HTTPException(status_code=404, detail="No data files found in the directory.")

    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Starting processing {len(data_files)} files.")

    # Start merging
    start_time = time.time()

    # Global heap for top n results
    heap = []

    # Process files using multiprocessing
    with Pool(4) as pool: # 4 workers
        results = pool.starmap(process_file, [(file_path, n) for file_path in data_files])

    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Finished processing files. Merging results.")

    # Merge results from all workers
    for r in results:
        for value, numerical_id in r:
            heapq.heappush(heap, (value, numerical_id))
            if len(heap) > n:
                heapq.heappop(heap)

    # Extract top n results
    top_ids = [item[1] for item in sorted(heap, reverse=True)]

    # End merging
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Finished merging results.")
    end_time = time.time()
    print(f"Time taken for getting top {n} ids: {end_time - start_time:.2f} seconds.")

    return {"top_ids": top_ids}


def process_file(file_path: str, n: int) -> List[Tuple[int, str]]:
    """
    Process a data file and return the top n numerical IDs for that file.
    """
    heap = []
    file_size_str = format_file_size(os.path.getsize(file_path))

    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Processing file {file_path}, size: {file_size_str}.")

    with open(file_path, "r") as f:
        while True:
            lines = f.readlines(CHUNK_SIZE)
            if not lines:
                break

            for line in lines:
                try:
                    numerical_id, numerical_value = line.strip().split("_")
                    numerical_value = int(numerical_value)
                except ValueError:
                    continue  # Skip invalid lines

                # Maintain a local heap for the file
                heapq.heappush(heap, (numerical_value, numerical_id))
                if len(heap) > n:
                    heapq.heappop(heap)

    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Finished processing file {file_path}.")
    return heap


def format_file_size(size_bytes: int) -> str:
    """
    Returns the file size in a human-readable format (bytes, KB, MB, GB, etc.).

    :param size_bytes: file size in byte
    :return: Formatted file size as a string
    """
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    index = 0

    while size_bytes >= 1024 and index < len(units) - 1:
        size_bytes /= 1024
        index += 1

    return f"{size_bytes:.2f} {units[index]}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
