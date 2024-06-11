import os
import subprocess
import time
import datetime

UNIT_TEST_PATH = ".\\tests\\unit\\"

if os.environ.get("PYTHONIOENCODING") is None or os.environ.get("PYTHONIOENCODING") != "UTF-8":
    os.environ["PYTHONIOENCODING"] = "UTF-8"

tests_list = os.listdir(UNIT_TEST_PATH)
tests_list = [f for f in tests_list if os.path.isfile(os.path.join(UNIT_TEST_PATH, f))]
tests_list = list(filter(lambda file: file.find(".bak") == -1, tests_list))

print(f"Mutation tests started at: {datetime.datetime.now()}")
start_time = time.time()

for test in tests_list:
    print(f"RUNNING TEST: {test}")
    proces = subprocess.Popen(f"mutmut run {UNIT_TEST_PATH}{test}")
    proces.wait()

end_time = time.time()
running_for = end_time - start_time

print(f"Mutation tests ended at: {datetime.datetime.now()}")
print(f"Mutation tests ran for: {running_for}")
