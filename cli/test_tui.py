import pexpect
import sys

def run_self_test():
    # Run the CLI self_test.py and capture output
    child = pexpect.spawn('python cli/self_test.py', encoding='utf-8', timeout=10)
    child.expect(pexpect.EOF)
    output = child.before
    print("=== CLI self_test.py output ===")
    print(output)
    # Example assertion: check for expected output string
    assert "PASS" in output or "OK" in output or "Success" in output, "Self test did not pass"

if __name__ == "__main__":
    try:
        run_self_test()
        print("TUI test passed.")
        sys.exit(0)
    except Exception as e:
        print(f"TUI test failed: {e}")
        sys.exit(1)
