import pandas as pd 
import json 
from jsonpath_ng import parse
from databricks.sdk.service.jobs import JobSettings

json_path="jobs/wf_test_update_dev.json"

with open(json_path,'r') as file:
    data=json.load(file)

print(data.get('job_id'))

json_obj=JobSettings.from_dict(data.get("new_settings"))
print(json_obj)