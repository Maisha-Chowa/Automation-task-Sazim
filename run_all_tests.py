import subprocess
import sys


def main() -> int:
    cmd = [sys.executable, "-m", "pytest"]
    extra_args = sys.argv[1:]
    if extra_args:
        cmd.extend(extra_args)
    else:
        cmd.extend(["tests", "-q"])

    result = subprocess.run(cmd, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
