import subprocess
import time
i = 0
while True:
    subprocess.run(f"cp -rf ./test-client/test6-client.py ./test2-client/test6-client.py && cp -rf ./test-client/test6-client.py ./test3-client/test6-client.py", shell=True)
    print(f"{i}. - Copied")
    i += 1
    time.sleep(5)