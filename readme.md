# NEXUS ATTACK v1.0 - Advanced Attack Tool

**NEXUS ATTACK** is a modular and powerful DDOS attack script designed to target both the network infrastructure (Layer 4) and the application layer (Layer 7). This tool combines different attack vectors into a single interface, allowing you to perform flexible and effective tests.

## Legal Disclaimer

**THIS TOOL IS FOR LEGAL AND EDUCATIONAL PURPOSES ONLY.**

Using this script against systems, networks, or websites without permission is illegal and can have serious consequences. The developer is not responsible for any illegal use of this tool. Only use it on systems you own or have explicit permission to test.

## Core Features

-   **Multi-Layer Attacks:** Capable of launching attacks on both network (L4) and application (L7) layers.
-   **Modular Menu:** Easily select the attack layer and method through a user-friendly menu.
-   **Layer 7 (Application) Attacks:**
    -   **Advanced HTTP Flood:** Smart HTTP requests that mimic real user behavior (random User-Agent, Referer, etc.) and bypass caching mechanisms (cache-busting).
    -   **Proxy Support:** Ability to route attack traffic through a list of proxies to anonymize and distribute the attack source.
-   **Layer 4 (Network) Attacks:**
    -   **TCP SYN Flood:** A classic and effective attack aimed at exhausting the server's connection resources.
    -   **UDP Flood:** A high-volume data packet attack designed to saturate the target's network bandwidth.
-   **High Performance:** Capable of sending thousands of concurrent requests or packets thanks to its multi-threading architecture.

## Requirements

-   Python 3.x
-   `requests` library

## Installation and Usage

1.  **Clone or download the project:**

    ```bash
    git clone https://github.com/onlycmd/nexus-script.git
    cd your-project
    ```

2.  **Install the required Python library:**

    ```bash
    pip install requests
    ```
    or
    ```bash
    pip3 install requests
    ```

3.  **(Optional) Create a Proxy List:**

    If you want to use proxies for Layer 7 attacks, edit the `proxies.txt` file in the project directory. Add your proxy addresses in `IP:PORT` format, one per line. If the file is left empty or not found, the attack will be launched directly without proxies.

4.  **Run the script:**

    ```bash
    python nexus.py
    ```

5.  **Make Your Selections from the Menu:**
    -   First, choose the attack layer (1: Layer 7, 2: Layer 4).
    -   Based on your choice, enter the relevant attack method and target information (URL or IP:Port), number of threads, and duration.

The script will automatically stop after the specified duration. You can manually stop the attack by pressing `CTRL + C`.

## Running on a VPS (Recommended)

This script is fully compatible with any Linux-based VPS (e.g., Ubuntu, Debian, CentOS) and it is the recommended environment for running powerful attacks due to superior network bandwidth and system resources.

1.  **Connect to your VPS:**
    ```bash
    ssh your-user@your-vps-ip
    ```

2.  **Install Python and Git:**
    If they are not already installed, update your package manager and install them.
    ```bash
    # For Debian/Ubuntu
    sudo apt-get update
    sudo apt-get install python3 python3-pip git -y
    ```

3.  **Clone the project:**
    Follow the installation steps above to clone the repository and install the `requests` library.

4.  **Run the script:**
    You can now run the script as described in the usage section. For long-running attacks, it is recommended to use a terminal multiplexer like `screen` or `tmux` to keep the script running even after you disconnect from the SSH session.
    ```bash
    # Example using screen
    screen -S attack
    python3 nexus.py
    # You can now detach from the screen session by pressing CTRL+A then D. The script will continue to run.
    ```

## Contributing

If you wish to contribute to the project, please open a pull request. All contributions are welcome!

## License

This project is licensed under the MIT License.

