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
spn='85a4d344-30ac-400b-94e6-dcca17c1022a'

# print(df)

print("******** GETTING THE CONTEXT VARS ********")

vars=json.loads(os.getenv('CONTEXT_VARS'))

print(vars)

json_service_principal=parse("run_as.service_principal_name")

json_notebook_path=parse("tasks[*].notebook_tasks.notebook_path")

def get_match_value(data,json_expr):
    return [match.value for match in json_expr.find(data)]

def validate_notebook_path(path,spn):

    path_expected=os.path.join('/Workspace/Repos/',spn)
    if path.startwith(path_expected):
        print(f"PATH IS VALID {path}")
    else:
        print(f"PATH IS INVALID EXPECTED PATH IS :{path_expected}")
        

def validate_json(json_df):
    print("JSON VALIDATION IS START FROM HERE")
    for job_json_dict in json_df.to_dict('records'):

        _,json_path=job_json_dict.values()

        json_dir,json_name=os.path.split(json_path)

        json_name,_=os.path.splitext(json_name)
        print(f"JSON NAME:{json_name}")

        try:
            with open(json_path,'r') as file:
                data=json.load(file)
        except Exception as e:
            print(f"Invalid JSON {e}")


        job_id=data.get('job_id',None)

        if job_id:
            print("JOB JSON IS TO UPDATE THE EXISTING JOB")

        else:
            
            spn_lst=get_match_value(data,json_service_principal)

            if all(spn==match_value for match_value in spn_lst):
                print(f"Valid SPN:{spn}")
            else:
                print(f"INVALID SPN EXPECTING :{spn}")

            
            all_notebooks=get_match_value(data,json_notebook_path)
            print(f"ALL NOTEBOOK PATH LIST:{all_notebooks}")

            for path in all_notebooks:
                print("START VALIDATING THE ALL NOTEBOOKS PATH")
                validate_notebook_path(path,spn)
                    


            
        
validate_json(json_df)


        
            


    