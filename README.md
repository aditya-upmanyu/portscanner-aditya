# Advanced Python Port Scanner

This is a fast, multi-threaded port scanner with banner grabbing capabilities, written in Python. It's designed to quickly identify open ports on a target machine and attempt to discover the version of the service running on each open port.

## Features

- **Multi-threaded Scanning**: Utilizes a thread queue to scan many ports simultaneously, making it significantly faster than a linear scanner.
- **Banner Grabbing**: For each open port, the tool attempts to grab the service banner to identify the running software (e.g., "SSH-2.0-OpenSSH_8.2", "Microsoft ESMTP").
- **Multiple Target Scanning**: You can scan multiple hosts in a single command by separating them with a comma.
- **Colored Output**: Uses `termcolor` to provide a clear, color-coded output for open ports and status messages.
- **Cross-Platform**: Works on Windows, macOS, and Linux, with `colorama` included for Windows compatibility.

## Prerequisites

Before you can run the script, you need to install its dependencies. This project requires Python 3.x and two external libraries.

- `termcolor`: For adding color to the terminal output.
- `colorama`: Required for `termcolor` to work correctly on Windows.

## Installation

1.  **Clone the repository or download the script.**
    - Save the code as `advanced_scanner.py`.

2.  **Install the required libraries using pip:**
    ```
    pip install termcolor colorama
    ```

## Usage

Run the script from your terminal. It will prompt you for the target(s) and the number of ports to scan.

