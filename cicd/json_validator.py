import json 
import os
import pandas as pd 
from jsonpath_ng import parse

repo_dir_path=os.getenv('GITHUB_WORKSPACE')
print(f"REPO DIRECTORY PATH {repo_dir_path}")

change_log_path=os.path.join(repo_dir_path,'cicd/change_log.csv')
print(f"CHANGE LOG CSV PATH {change_log_path}")

df=pd.read_csv(change_log_path,delimiter="\t",names=['change','name'])
df=df[df['change']!='D']

json_df=df[df.name.str.endswith('.json')]
print(json_df)

env_lst=["dev","prod"]


# print(df)

print("******** GETTING THE CONTEXT VARS ********")

vars=json.loads(os.getenv('CONTEXT_VARS'))

print(vars)

json_service_principal=parse("run_as.service_principal_name")

def get_match_value(data,json_expr):
    return [match.value for match in json_expr.find(data)]


def validate_json(json_df):
    print("JSON VALIDATION IS START FROM HERE")
    for job_json_dict in json_df.to_dict('records'):

        _,json_path=json_df.values()

        json_dir,json_name=os.path.split(json_path)

        json_name,_=os.path.splitext(json_name)
        print(f"JSON NAME:{json_name}")

        try:
            with open(json_path,'r') as file:
                data=json.loads(file)
        except:
            print("Invalid JSON")

        SPN=get_match_value(data,json_service_principal)
        print(f"SERVICE PRINCIPAL:{SPN}")
        
validate_json(json_df)


        
            


    