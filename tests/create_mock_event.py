import argparse
import base64
import json


def mock_event(file_path, filename, output):
    """
    mocks the event object that would be passed to the lambda function from request:
    curl -X POST https://your-api-endpoint.com/upload \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/document.pdf" \
     -F "filename=algebra lang.pdf"
    """
    with open(file_path, 'rb') as file:
        file_content = file.read()
        encoded_content = base64.b64encode(file_content).decode('utf-8')

    event = {
        'headers': {
            'Content-Type': 'multipart/form-data',
            'filename': filename,
        },
        'body': encoded_content,
        'isBase64Encoded': True,
    }
    # write out event to json file
    with open(output, 'w') as file:
        json.dump(event, file, indent=4)


def main():
    parser = argparse.ArgumentParser(
        description='Mock event object for testing lambda function')
    parser.add_argument('--path', type=str, required=True,
                        help='path to file to be uploaded')
    parser.add_argument('--filename', type=str, required=True,
                        help='name of file to be uploaded')
    parser.add_argument('--output', type=str, default='event.json',
                        help='name of output file')
    args = parser.parse_args()

    mock_event(args.path, args.filename, args.output)


if __name__ == "__main__":
    main()
