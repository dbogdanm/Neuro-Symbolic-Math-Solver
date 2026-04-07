import json
input_file = 'tests/math500.jsonl'
output_file = 'tests/math500_noanswers.jsonl'

with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
    for line in f_in:
        data = json.loads(line)
        new_data = {"problem": data["problem"]}
        f_out.write(json.dumps(new_data) + '\n')
