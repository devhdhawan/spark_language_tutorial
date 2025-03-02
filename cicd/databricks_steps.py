#<-------- IMPORT ALL THE LIBRARY HERE -------- >
import json 
from databricks.sdk import WorkspaceClient
import os
import pandas as pd 
# import chardet


#<-------- GET THE REPO PATH -------- >
repo_root_dir = os.getenv("GITHUB_WORKSPACE")
print(f"REPO PATH:{repo_root_dir}")


#<-------- CREATE THE PATH TO ACCESS THE CHANGE LOG FILE -------- >
changelog_path=os.path.join(repo_root_dir,"cicd/change_log.csv")
print(f"Change Log CSV FILE PATH:{changelog_path}")

#<-------- READ CSV PATH -------- >
df=pd.read_csv(changelog_path,delimiter="\t",names=['change','name'])
df=df[df['change']!='D']

#<--------- WORKSPACE CLIENT OBJECT TO ACCESS WORKSPACE RESOURCES --------->
ws=WorkspaceClient()

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
    change_file_lst=list(df.change)
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

    