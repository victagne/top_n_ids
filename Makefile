# Variables
PYTHON=python
HOST=0.0.0.0
PORT=8000
DATA_DIR=data
DATA_GENERATOR_SCRIPT=data_generator.py
FASTAPI_APP=main.py
# Default value for n if not provided
N=3

.PHONY: run generate clean request

# Generate test data by calling data_generator.py
generate:
	@echo "Generating data using data_generator.py..."
	$(PYTHON) $(DATA_GENERATOR_SCRIPT)
	@echo "Data generation complete."

# Clean up test data
clean:
	@echo "Cleaning up generated data files..."
	@rm -rf $(DATA_DIR)
	@echo "Data directory $(DATA_DIR) removed."

# Start FastAPI application
run:
	@echo "Starting FastAPI application..."
	uvicorn main:app --host $(HOST) --port $(PORT) --reload


# Make a POST request to FastAPI with a specified 'N' value
request:
	@echo "Making POST request with n=$(N)..."
	curl -X POST "http://127.0.0.1:8000/top_n_ids/" -F "n=$(N)"
