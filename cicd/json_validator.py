import json 
import os
import pandas as pd 

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
