
print("Hello Everyone !! Welcome to GITHUB ACTIONS.")

import pandas as pd
import os

repo_root_dir = os.getenv("GITHUB_WORKSPACE")
print(f"REPO PATH:{repo_root_dir}")

changelog_path=os.path.json(repo_root_dir,"cicd/change_log.csv")
print(f"Change Log CSV FILE PATH:{changelog_path}")

df=pd.read_csv(changelog_path,delimiter="\t")


print(df)