import datetime
import re

# global prefix for today’s log entries
today_prefix = datetime.datetime.now().strftime("%d.%m.%Y")

def check_stdout(log_file_path: str) -> bool:
    with open(log_file_path, "r", encoding="utf-8") as log:
        for line in log:
            if not line.startswith(today_prefix):
                continue
            if "*info * [main] startup completed" in line.lower():
                return True
    return False

def check_stderr(log_file_path: str) -> bool:
    cnt = 0
    with open(log_file_path, "r", encoding="utf-8") as log:
        for line in log:
            if "quickstart started" in line.lower():
                cnt += 1
            if "startup time:" in line.lower():
                cnt += 1
    return cnt == 2

def check_error_log(log_file_path: str) -> bool:
    try:
        with open(log_file_path, "r", encoding="utf-8") as log:
            lines = log.readlines()

        # Filter today's lines
        today_lines = [line.lower() for line in lines if line.startswith(today_prefix)]

        # Check Jetty started on port 4502
        jetty_started = any("started jetty" in line and "4502" in line for line in today_lines)

        # Check for fatal errors or exceptions
        fatal_errors = any("error" in line or "fatal" in line or "exception" in line for line in today_lines)
        no_fatal_errors = not fatal_errors

        # Check warnings are only about deprecated mappings
        warn_lines = [line.lower() for line in today_lines if "**warn**" in line.lower()]
        deprecated_only = all("deprecated service mapping" in line for line in warn_lines)

        return all([jetty_started, no_fatal_errors, deprecated_only])

    except Exception as e:
        print(f"Error checking error.log: {e}")
        return False

if __name__ == "__main__":
    stdout_log_path = r"C:\Users\cbhattacha015\OneDrive - PwC\Downloads\AEM Learning\Author\crx-quickstart\logs\stdout.log"
    stderr_log_path = r"C:\Users\cbhattacha015\OneDrive - PwC\Downloads\AEM Learning\Author\crx-quickstart\logs\stderr.log"
    error_log_path = r"C:\Users\cbhattacha015\OneDrive - PwC\Downloads\AEM Learning\Author\crx-quickstart\logs\error.log"

    stdout_ok = check_stdout(stdout_log_path)
    stderr_ok = check_stderr(stderr_log_path)
    error_ok = check_error_log(error_log_path)

    print(stdout_ok and stderr_ok and error_ok)
