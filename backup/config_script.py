import os
import re

path='C:/Users/hdhawan/Desktop/Learning/Devops/spark_language_tutorial/pyspark/config_template.py'


dict={
'ENV':'DEV',
'DATABRICKS_HOST':'https://adb-1816948890627837.17.azuredatabricks.net/',
'GET_ALIAS':'_mainrepo',
'REPO_ID':'2318070819290975',
'dev_env_name':'dev-dbricks-env',
'dev_resource_grp':'ProjectAlphaDEV',
'dev_ser_conn_name':'dev-service-conn'
}

# print(dict['dev_resource_grp'])

def update_config(path):
    with open(path,'r') as file:
        src_content=file.read()

    pattern=r'<<.*?>>'

    match_var_lst=re.findall(pattern,src_content)

    modified_data=src_content
    for match in match_var_lst:
        map_val=dict[match[2:-2]]
        
        modified_data=modified_data.replace(match,map_val)
    
    return modified_data


data=update_config(path)
print(data)

# print(src_content)
# update_content=src_content.replace('<<ENV>>',env)
# print(update_content)