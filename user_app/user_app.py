import argparse
import base64
import json
import requests
from textwrap import wrap
from datetime import datetime


API_URL = "enter your API host url here"

APP_ROUTES = {
    "heartbeat": "/heartbeat",
    "ask": "/ask_question",
    "add": "/add_document",
    "ask_no_ref": "/ask_question_no_refs"
}


def format_ask_request(query):
    url = API_URL + APP_ROUTES["ask"]
    payload = {
        "body": query,
        "headers": {}
    }
    headers = {"Content-Type": "application/json"}
    return {'url': url, 'headers': headers, 'json': payload}


def format_add_request(file_path):
    url = API_URL + APP_ROUTES["add"]
    with open(file_path, 'rb') as file:
        file_content = file.read()
        encoded_content = base64.b64encode(file_content).decode('utf-8')

    payload = {
        "headers": {
            "Content-Type": "multipart/form-data",
            "filename": file_path.split("/")[-1],
        },
        "body": encoded_content,
        "isBase64Encoded": True,
    }
    headers = {"Content-Type": "application/json"}
    return {'url': url, 'headers': headers, 'json': payload}


def format_ask_no_ref_request(query):
    url = API_URL + APP_ROUTES["ask_no_ref"]
    payload = {
        "body": query,
        "headers": {}
    }
    headers = {"Content-Type": "application/json"}
    return {'url': url, 'headers': headers, 'json': payload}


def print_response(response):
    print("===Body===:")
    print(response['body'])
    print("===References===")
    for reference in response['references']:
        print(f"Source: {reference['source']}, Page: {reference['page']}")
        print(wrap(reference['content'], width=60,
              initial_indent="  ", subsequent_indent="  "))
        print("******")


def main():
    parser = argparse.ArgumentParser(description='Add documents or query the RAG system')
    parser.add_argument(
        '--type', help='"add" to add a document, "ask" to query the system, "heartbeat" to check the system status. Also "ask-no-ref" to query without references')
    parser.add_argument(
        '--body', help='The query to run or path to document to add')
    args = parser.parse_args()

    if args.type == "heartbeat":
        response = requests.get(API_URL + APP_ROUTES["heartbeat"])
        print(response.json())
        return

    REQUEST_FUNCTIONS = {
        "ask": format_ask_request,
        "ask-no-ref": format_ask_no_ref_request,
        "add": format_add_request,
    }
    request = REQUEST_FUNCTIONS[args.type](args.body)
    response = requests.post(**request)
    data = response.json()

    # Decode the 'references' field if it's a string
    if isinstance(data.get('references'), str):
        data['references'] = json.loads(data['references'])

    # Save response
    data['request_type'] = args.type
    data['request_body'] = args.body

    print_response(data)

    filename = '../responses/response' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.json'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Response saved to {filename}")


if __name__ == '__main__':
    main()
