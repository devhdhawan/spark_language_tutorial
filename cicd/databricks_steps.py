#<-------- IMPORT ALL THE LIBRARY HERE -------- >
import json 
from databricks.sdk import WorkspaceClient
import os
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

default_workdir = os.environ.get("SYSTEM_DEFAULTWORKINGDIRECTORY")


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
print(df)
print(df.change)
print(df.name)
print(df.name.split('.'))

#<--------- WORKSPACE CLIENT OBJECT TO ACCESS WORKSPACE RESOURCES --------->
ws=WorkspaceClient(host=host,token=token)

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
            workflow_file=file
        
            with open(workflow_file,'r') as file:
                job_json=json.load(file)
            
            res=create_workflow(ws,job_json)
            print(f"JOB ID:{res['job_id']}")
        else:
            print("NO WORKFLOW MODIFY OR CREATED NEWLY")


deploy_workflow(ws,df)

    