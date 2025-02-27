
print("Hello Everyone !! Welcome to GITHUB ACTIONS.")

import pandas as pd
import os
import json

repo_root_dir = os.getenv("GITHUB_WORKSPACE")
print(f"REPO PATH:{repo_root_dir}")

changelog_path=os.path.join(repo_root_dir,"cicd/change_log.csv")
print(f"Change Log CSV FILE PATH:{changelog_path}")

df=pd.read_csv(changelog_path,delimiter="\t",names=['change','name'])

df=df[df['change']!='D']

vars=json.loads(os.getenv('CONTEXT_VARS'))
print(vars)

print(df)