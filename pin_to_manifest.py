import argparse
import boto3
import json
import os
import requests


ART_API_TOKEN = os.environ.get('ARTIFACTORY_API_KEY')
ART_URL = 'https://taii217.jfrog.io/artifactory'
s3_bucket = 'artifactory-taii217'
s3_client = boto3.client('s3')

HEADERS = {
   'Authorization': f"Bearer {ART_API_TOKEN}"
}

import re

def parse_filename(filename):
    pattern = re.compile(r'^([a-zA-Z0-9_-]+)_([a-zA-Z0-9.-]+)\.([a-zA-Z0-9]+)$')
    if not (match := pattern.match(filename)):
        return None
    name, version, ext = match[1], match[2], match[3]
    return name, version, ext


def search_builinfo(stack_tag: str, glbal_build_id: str):
    url = f'{ART_URL}/api/search/aql'
    filters = {
        "repo":{"$match":"artifactory-build-info"},
        "@STACK_TAG" : {
            "$eq": stack_tag
        },
        "@GLOBAL_BUILD_ID" : {
            "$eq": glbal_build_id
        }
    }
    headers = {
        'Content-Type': 'text/plain'
    } | HEADERS
    body = f"items.find({json.dumps(filters)})"
    response = requests.post(url, data=body, headers=headers)
    return response.json() if response.status_code == 200 else {}

def get_packages(stack_tag: str, glbal_build_id: str):
    try:
        build_infos = search_builinfo(stack_tag, glbal_build_id)
        info = build_infos.get('results', {})[0]
        if not info:
            return False, 'build info not found!'
        
        build_info_path = f"{ART_URL}/{info['repo']}/{info['path']}/{info['name']}"

        response = requests.get(build_info_path, headers=HEADERS)
        return (True, response.json()) if response.status_code == 200 else (False, "File build info not found")
    except Exception as e:
        return False , str(e)



def pin_to_manifest_file(build_info_data: dict, stack_tag: str):
    results = []
    try:
        artifacts = build_info_data.get('modules')[0].get("artifacts")
        for artifact in artifacts:
            name, version, ext = parse_filename(artifact.get("name"))
            results.append(f"{name}=={version}")

        # public data
        s3_client.put_object(Bucket=s3_bucket, Key=f"{stack_tag}.manifest", Body= "\n".join(results))
        return True
    except Exception as e:
        print(e)
        return False


def main():
    parser = argparse.ArgumentParser(description='Pinning step')
    parser.add_argument('--global-build-id')
    parser.add_argument('--stack-tag')

    args = parser.parse_args()

    success, build_info_data = get_packages(args.stack_tag, args.global_build_id)
    if not success:
        print("pin to manifest: get build info fail")
        return 
    if not pin_to_manifest_file(build_info_data, args.stack_tag):
        print("pin to manifest: failed")
    return "pin to manifest: success"


if __name__ == '__main__':
    main()