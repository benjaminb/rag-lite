
# Question-Answering with AWS/SageMaker, Llama, and RAG

This project aims to make a question-answering service as lightweight and low-cost. 
## Setup

### Prerequisites

- Python 3.12
- AWS CLI configured with appropriate permissions
- SageMaker setup with an endpoint

### Installation

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install dependencies for FastAPI implementation:

    ```sh
    pip install -r fastapi_impl/requirements.txt
    ```

3. Install dependencies for user application:

    ```sh
    pip install -r user_app/requirements.txt
    ```

## Usage

### FastAPI Server

1. Navigate to the [fastapi_impl](http://_vscodecontentref_/14) directory:

    ```sh
    cd fastapi_impl
    ```

2. Run the FastAPI server:

    ```sh
    uvicorn app:app --host 0.0.0.0 --port 8000
    ```

### User Application

1. Navigate to the [user_app](http://_vscodecontentref_/15) directory:

    ```sh
    cd user_app
    ```

2. Run the user application:

    ```sh
    python user_app.py --type=<type> --body=<body>
    ```

    - `--type`: Type of request (`add`, `ask`, [heartbeat](http://_vscodecontentref_/16), `ask-no-ref`)
    - `--body`: The query to run or path to document to add

### Tests

1. Navigate to the [tests](http://_vscodecontentref_/17) directory:

    ```sh
    cd tests
    ```

2. Run the test scripts:

    ```sh
    ./test_heartbeat.sh
    ./test_add_doc.sh
    ./test_ask.sh
    ./test_user_app.sh
    ```

## Files

- [app.py](http://_vscodecontentref_/18): Main FastAPI application.
- [delete_db.py](http://_vscodecontentref_/19): Script to delete the Chroma database.
- [prompt_template.txt](http://_vscodecontentref_/20): Template for the prompt.
- [requirements.txt](http://_vscodecontentref_/21): Dependencies for FastAPI implementation.
- [user_app.py](http://_vscodecontentref_/22): User application to interact with the FastAPI server.
- [requirements.txt](http://_vscodecontentref_/23): Dependencies for the user application.
- [create_mock_event.py](http://_vscodecontentref_/24): Script to create a mock event for testing.
- [test_add_doc.sh](http://_vscodecontentref_/25): Script to test adding a document.
- [test_ask.sh](http://_vscodecontentref_/26): Script to test asking a question.
- [test_heartbeat.sh](http://_vscodecontentref_/27): Script to test the heartbeat endpoint.
- [test_user_app.sh](http://_vscodecontentref_/28): Script to test the user application.

## License

This project is licensed under the MIT License.