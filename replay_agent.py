#!/usr/bin/env python3
"""
Python implementation of the ReplayAgent for testing ACP agents.

This agent reads a replay file containing OUT: (expected) and IN: (response) markers,
validates JSON communication, and simulates agent interaction via stdin/stdout.
"""

import json
import sys
import time
from typing import Any, Dict


class ReplayAgent:
    def __init__(self, source_file: str, project_root: str):
        """
        Initialize the ReplayAgent.

        Args:
            source_file: Path to the replay file containing OUT:/IN: markers
            project_root: Path to replace in cwd fields for comparison
        """
        self.source_file = source_file
        self.project_root = project_root

    def start(self):
        """Start processing the replay file."""
        try:
            with open(self.source_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.rstrip('\n')

                    if "OUT:" in line:
                        self._handle_out_line(line)
                    elif "IN:" in line:
                        self._handle_in_line(line)

            sys.stdout.flush()
            time.sleep(1)

        except FileNotFoundError:
            print(f"ERROR: Replay file not found: {self.source_file}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
            sys.exit(1)

    def _handle_out_line(self, line: str):
        """Handle OUT: line - compare expected JSON with actual stdin input."""
        expected_json = self._extract_json(line, "OUT:")
        actual_input = sys.stdin.readline().rstrip('\n')

        if not self._compare_jsons(expected_json, actual_input):
            print("ERROR: JSON mismatch", file=sys.stderr)
            print(f"Expected: {expected_json}", file=sys.stderr)
            print(f"Actual: {actual_input}", file=sys.stderr)
            # Note: exitProcess(1) is commented out in original, so not exiting here

    def _handle_in_line(self, line: str):
        """Handle IN: line - send response JSON to stdout."""
        response_json = self._extract_json(line, "IN:")
        print(response_json)
        sys.stdout.flush()

    def _extract_json(self, line: str, marker: str) -> str:
        """Extract JSON string after the marker."""
        index = line.find(marker)
        return line[index + len(marker):].strip()

    def _compare_jsons(self, expected: str, actual: str) -> bool:
        """
        Compare two JSON strings, with special handling for cwd replacement.

        Args:
            expected: Expected JSON string
            actual: Actual JSON string from stdin

        Returns:
            True if JSONs match (after cwd replacement), False otherwise
        """
        try:
            expected_obj = json.loads(expected)
            actual_obj = json.loads(actual)

            # Replace cwd in expected JSON
            expected_obj = self._replace_cwd_in_json(expected_obj)

            return expected_obj == actual_obj

        except json.JSONDecodeError as e:
            print(f"ERROR: Failed to parse JSON: {e}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"ERROR: Failed to compare JSON: {e}", file=sys.stderr)
            return False

    def _replace_cwd_in_json(self, element: Any) -> Any:
        """
        Replace cwd field in JSON params with project_root.

        Args:
            element: JSON element (can be dict, list, or primitive)

        Returns:
            Modified JSON element with cwd replaced
        """
        if not isinstance(element, dict):
            return element

        # Check if this has params.cwd
        if "params" in element and isinstance(element["params"], dict):
            if "cwd" in element["params"]:
                # Create a copy with replaced cwd
                new_element = element.copy()
                new_params = element["params"].copy()
                new_params["cwd"] = self.project_root
                new_element["params"] = new_params
                return new_element

        return element


def main():
    """Main entry point for the replay agent."""
    # Handle help and version flags
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "help"]:
        print("ACP Replay Agent v1.0.0")
        print("\nA tool for testing Agent Client Protocol (ACP) implementations")
        print("by replaying recorded communication sessions.")
        print("\nUsage:")
        print("  replay_agent.py <replay_file_path> <project_root>")
        print("\nArguments:")
        print("  replay_file_path  Path to replay log file with OUT:/IN: markers")
        print("  project_root      Project root path to replace 'cwd' fields")
        print("\nExample:")
        print("  replay_agent.py examples/example.log /Users/anna/dev/project")
        print("\nFor more information: https://github.com/yourusername/acp-replay")
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1] in ["-v", "--version", "version"]:
        print("ACP Replay Agent v1.0.0")
        sys.exit(0)

    if len(sys.argv) < 3:
        print("Usage: replay_agent.py <replay_file_path> <project_root>", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print("  replay_agent.py /path/to/replay.txt /path/to/project", file=sys.stderr)
        print("\nFor help: replay_agent.py --help", file=sys.stderr)
        sys.exit(1)

    replay_file = sys.argv[1]
    project_root = sys.argv[2]

    agent = ReplayAgent(replay_file, project_root)
    agent.start()

    # Keep alive (similar to CountDownLatch.await() in Kotlin)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
