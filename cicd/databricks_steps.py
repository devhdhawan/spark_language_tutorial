#<-------- IMPORT ALL THE LIBRARY HERE -------- >
import json 
from databricks.sdk import WorkspaceClient
from databricks_cli.workspace.api import WorkspaceApi,WorkspaceFileInfo
from databricks_cli.repos.api import ReposApi
from databricks_cli.sdk.api_client import ApiClient
from databricks.sdk.service.workspace import ImportFormat,Language
import os
import re
import pandas as pd 
import argparse
# import chardet

parser = argparse.ArgumentParser(
    description="This script performs deployment tasks for "
)
parser.add_argument("--token", required=True)
args = parser.parse_args()

host = os.environ.get("DATABRICKS_HOST")
token = args.token[:]

repo_id=os.environ.get('REPO_ID')
default_workdir = os.environ.get("SYSTEM_DEFAULTWORKINGDIRECTORY")
git_dir = os.path.join(default_workdir, os.environ.get("GIT_ALIAS"))

#<-------- GET THE REPO PATH -------- >
repo_root_dir = os.environ.get("REPO_ROOTPATH")
print(f"REPO PATH:{repo_root_dir}")


#<-------- CREATE THE PATH TO ACCESS THE CHANGE LOG FILE -------- >
# changelog_path=os.path.join(repo_root_dir,"cicd/change_log.csv")
changelog_path = os.path.join(default_workdir, "_changelog", "drop", "change_log.csv")
print(f"Change Log CSV FILE PATH:{changelog_path}")

#<-------- READ CSV PATH -------- >
df=pd.read_csv(changelog_path,delimiter="\t",names=['change','name'])
df=df[df['change']!='D']


#<--------- WORKSPACE CLIENT OBJECT TO ACCESS WORKSPACE RESOURCES --------->
ws=WorkspaceClient(host=host,token=token)

api_client = ApiClient(host=host,token=token,jobs_api_version='2.1')

print(f"DATABRICKS HOST:{ws}")

def create_workflow(ws,job_json):
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    }

    #<--------- CREATE THE JOB WORKFLOW --------->
    res = ws.api_client.do(
        "POST", "/api/2.1/jobs/create", body=job_json, headers=headers
    )

    return res


def deploy_workflow(ws,df):

    #<--------- LIST OF FILES MODIFIED --------->
    change_file_lst=list(df.name)
    print(f"List of file change:{change_file_lst}")
    for file in change_file_lst:

        #<--------- CHECK IF THE JOB JSON IS MODIFIED OR NEWLY ADDED --------->
        if file.split('.')[1]=='json':
            print(f"JSON FILE : {file}")

            workflow_file_name=file
            workflow_file_path=os.path.join(git_dir,workflow_file_name)

            with open(workflow_file_path,'r') as file:
                job_json=json.load(file)
            
            res=create_workflow(ws,job_json)
            print(f"JOB ID:{res['job_id']}")
        else:
            print("NO WORKFLOW MODIFY OR CREATED NEWLY")

def update_config(data):
    
    pattern=r'<<.*?>>'
    match_var_lst=re.findall(pattern,data)
    
    for match in match_var_lst:
        map_val=os.environ.get(match[2:-2])
        data=data.replace(match,map_val)
    
    return data

def generate_config(src_config_path):

    modified_content=None
    with open(src_config_path,'r') as file:
        src_content=file.read()
    
    modified_content=update_config(src_content)

    return modified_content

def deploy_repo(api_client):
    
    #<--------- SET THE FORMAT AND LANGUAGE --------->
    fmt=ImportFormat.SOURCE
    language=Language.PYTHON
    overwrite=True

    print(f"FORMAT:{fmt} Language:{language}")

    #<--------- CREATE THE SOURCE AND TARGET CONFIG PATH  --------->
    src_config_path=os.path.join(git_dir,'pyspark/config_template.py')
    target_config_path=os.path.join(git_dir,'pyspark/config.py')

    print(f"SOURCE CONFIG PATH:{src_config_path}")
    print(f"TARGET CONFIG PATH:{target_config_path}")

    try:
        #<--------- DELETE THE EXISTING TARGET CONFIG FILE --------->

        print("START DELETING THE TARGET FILE FROM THE REPOS")
        ws.workspace.delete(target_config_path,recursive=True)
        print("SUCCESSFULLY DELETED THE CONFIG FILE")

    except Exception as e:
        print(f"Failed to delete config file in workspace {e}")
    
    
    #<--------- GET THE CONFIG FILE  --------->
    modified_content=generate_config(src_config_path)
    print(modified_content)

    try:
        tag_name = f"{os.environ.get('BUILD_DEFINITIONID')}_{os.environ.get('BUILD_BUILDNUMBER')}"

        ws.repos.update(repo_id=repo_id,branch=None,tag_name=tag_name)
    except Exception as e:
        print("NOT ABLE TO UPDATE THE REPOS IN DATABRICKS")
        print(e)


    finally:
        ws.workspace.upload(
            path=target_config_path,
            content=modified_content,
            format=fmt,
            language=language,
            overwrite=overwrite,
        )
     
     

def deployment(ws,api_client,df):

    #<--------- DEPLOYING JOB WORKFLOW --------->
    deploy_workflow(ws,df)

    #<--------- DEPLOYING CODE CHANGE --------->
    deploy_repo(ws)



deployment(ws,api_client,df)
    