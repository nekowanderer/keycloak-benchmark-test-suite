#!/usr/bin/env python3

"""
Execute the main program of the Keycloak test results aggregator.
This script serves as a simplified entry point for invoking the test_results_aggregator package.
"""

import sys
import os
print(f"[aggregate_results.py] sys.argv: {sys.argv}")
print(f"[aggregate_results.py] SCENARIO_SUFFIX env: {os.environ.get('SCENARIO_SUFFIX')}")

from test_results_aggregator.main import main

if __name__ == "__main__":
    # Pass command line arguments to the main program
    if len(sys.argv) > 1:
        print(f"[aggregate_results.py] Setting aggregator.sample_scenario = {sys.argv[1]}")
    sys.exit(main()) 