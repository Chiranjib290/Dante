import datetime
import re

# global prefix for today’s log entries
today_prefix = datetime.datetime.now().strftime("%d.%m.%Y")

def check_stdout(log_file_path: str) -> bool:
    with open(log_file_path, "r", encoding="utf-8") as log:
        for line in log:
            if not line.startswith(today_prefix):
                continue
            if "*INFO * [main] Startup completed" in line:
                return True
    return False

def check_stderr(log_file_path: str) -> bool:
    cnt = 0
    with open(log_file_path, "r", encoding="utf-8") as log:
        for line in log:
            if "Quickstart started" in line:
                cnt += 1
            if "Startup time:" in line:
                cnt += 1
    return cnt == 2

def check_error_log(log_file_path: str) -> bool:
    try:
        with open(log_file_path, "r", encoding="utf-8") as log:
            lines = log.readlines()

        today_lines = [line for line in lines if line.startswith(today_prefix)]

        # Jetty started check
        jetty_started = any("Started Jetty" in line and "4502" in line for line in today_lines)

        # Fatal error patterns
        fatal_patterns = [
            r"\bException\b",
            r"\bFATAL\b",
            r"\bSEVERE\b",
            r"\*\*ERROR\*\*",
            r"^\s+at\s"  # stack trace lines
        ]
        fatal_error_regex = re.compile("|".join(fatal_patterns), re.IGNORECASE)
        fatal_errors_present = any(fatal_error_regex.search(line) for line in today_lines)
        no_fatal_errors = not fatal_errors_present

        # Bundles and services started
        bundles_started = any("BundleEvent STARTED" in line for line in today_lines)
        services_registered = any("ServiceEvent REGISTERED" in line for line in today_lines)

        # Warnings are only about deprecated mappings
        warn_lines = [line for line in today_lines if "**WARN**" in line]
        deprecated_only = all("Deprecated service mapping" in line for line in warn_lines)

        return all([jetty_started, no_fatal_errors, bundles_started, services_registered, deprecated_only])

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

    aem_launched_correct = stdout_ok and stderr_ok and error_ok
    
    print(aem_launched_correct)
