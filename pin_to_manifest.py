import argparse
import boto3
import gzip
import json
import os
import re
import shutil
import sys
import urllib.request
import time
import requests


ART_API_TOKEN = os.environ['ARTIFACTORY_API_KEY'] or 'eyJ2ZXIiOiIyIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYiLCJraWQiOiJmRnk1RlNBdXhrZTJFWG9ZaVF6djJlRTRPNnBucVd4VGo1aXlYSjRoWk00In0.eyJzdWIiOiJqZmFjQDAxaGc2c2hlZHZ6YXEwMDJkZWtwam0wNjFqL3VzZXJzL2FjYyIsInNjcCI6ImFwcGxpZWQtcGVybWlzc2lvbnMvYWRtaW4iLCJhdWQiOiIqQCoiLCJpc3MiOiJqZmZlQDAwMCIsImlhdCI6MTcwMjMwODEyOSwianRpIjoiNjNmMzc0ZWQtMmZhZi00M2ZiLTk2NTEtYjEzZGUwOTE0Y2QyIn0.AqamRUrBCVd7zkb9nbGreF709ZKJCma7jomd0tiks1jK-SsoiFl2vSPQg39zte75yKachGWGV66FUVz7VLmM-bcz3mSp-6Eks-DzHJUJlOnTdGj7801OID3u_ZCEXxDyjx9CG7JUw6wHyNb86epCaK16yeCsfQF_vo3UDvXBnGbWIY8qtR2QXVy-yQ9lbN87UY_9O-Q7zOkRVu4luLpkrhly8VvrVITgpHldcOF-RxnlpyOXg0Zmz0GwIHfw_QqNl1bKsd9RKdeMTb1qI5LkJcPoRukwKe7V02J90CB-GyOtGiFcCsSNynT204g6vdWK40qJlC0MCQvpdRGCma4jEQ'
workspace = os.environ['WORKSPACE']
ART_URL = 'https://artifactory.menloinfra.com/artifactory'
s3_bucket = 'menlosec-builds'
s3_client = boto3.client('s3')

HEADERS = {
   'Authorization': ART_API_TOKEN,
   'Content-Type': 'text/plain'
}


def search_artifact(repo_name: str, filter_pattern: str):
    url = f'{ART_URL}/api/search/aql'
    filters = {
        "repo":{
            "$eq": repo_name
        },
        "name":{
            "$match": filter_pattern
        }
    }

    body = f"items.find({json.dumps(filters)})"

    return requests.post(url, data=body, headers=HEADERS)

def get_packages(repo_name: str):
    repo_name = ''
    artifacts = search_artifact(repo_name, "*").json()

    packages = []
    for artifact in artifacts.get('results'):
       packages.append({
          "name": artifact.get('name'),
          "path": artifact.get('path')
       })
      

def pin_manifest(manifest, list_of_pkg: list, debs_list: dict):
   updated_manifest = False
   pinning_packages = set(list_of_pkg) & set([*debs_list])
   log.info(f'Update version of package in {manifest}')
   with open(manifest, 'r') as manifest_file:
      lines = manifest_file.readlines()
   with open(manifest, 'w') as manifest_file:
      for line in lines:
         match = re.match(r'^(\s*\w+:|)([^=\s]+)(\s*=\s*)(.+)$', line)

         if match:
            prefix, package, eq, ver = match.groups()
            pin_version = package in pinning_packages and debs_list.get(package)
            if pin_version and pin_version != ver:
               log.info(f'updating pin for {package} from {ver} to {pin_version}')
               line = prefix + package + eq + pin_version + '\n'
               updated_manifest = True
         manifest_file.write(line)

   return updated_manifest


def args_parse_env(args):
   args.repo = args.repo or os.environ['REPO_PATH']
   args.source_branch = args.source_branch or os.environ['SOURCE_BRANCH']
   args.os_version = args.os_version or os.environ['OS_VERSION']
   args.pinned_branch = args.pinned_branch or os.environ['PINNED_BRANCH']
   args.cherry_pick = args.cherry_pick or os.environ.get('CHERRY_PICK_BRANCH', '')
   args.build_id = args.build_id or os.environ['GLOBAL_BUILD_ID']
   args.stack_tag = args.stack_tag or os.environ['STACK_TAG']
   args.jenkins_host = args.jenkins_host or os.environ['JENKINS_HOST']
   args.package_type = args.package_type or os.environ['PACKAGE_TYPE']
   return args


def main():
   parser = argparse.ArgumentParser(description='Pinning step')
   parser.add_argument('--config')
   parser.add_argument('--source-branch')
   parser.add_argument('--os-version')
   parser.add_argument('--repo')
   parser.add_argument('--cherry-pick')
   parser.add_argument('--pinned-branch')
   parser.add_argument('--build-id')
   parser.add_argument('--stack-tag')
   parser.add_argument('--jenkins-host')
   parser.add_argument('--package-type')

   args = parser.parse_args()
   args = args_parse_env(args)



if __name__ == '__main__':
   main()