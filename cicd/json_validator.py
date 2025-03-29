import json 
import os

print("******** GETTING THE CONTEXT VARS ********")

vars=json.loads(os.getenv('CONTEXT_VARS'))

print(vars)
