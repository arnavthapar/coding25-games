import json

test_string = '{"a":5, "b":5}'

# Converted and printed 
res = json.loads(test_string)
print(str(res))