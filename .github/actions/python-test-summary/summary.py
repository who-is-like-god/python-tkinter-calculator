import sys
import xml.etree.ElementTree as ET


def summarize_report(report_path):
    tree = ET.parse(report_path)
    root = tree.getroot()

    suites = [root] if root.tag == "testsuite" else root.findall(".//testsuite")

    tests = sum(int(suite.get("tests", 0)) for suite in suites)
    failures = sum(int(suite.get("failures", 0)) for suite in suites)
    errors = sum(int(suite.get("errors", 0)) for suite in suites)
    skipped = sum(int(suite.get("skipped", 0)) for suite in suites)

    passed = tests - failures - errors - skipped

    print("================= PYTEST SUMMARY ==================")
    print(f"Total tests: {tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    print(f"Skipped: {skipped}")


if __name__ == "__main__":
    summarize_report(sys.argv[1])
