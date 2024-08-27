import os
import subprocess


def tpu_setup():
    """
    Function installs required dependencies to run Coral EdgeTPU
    :return:
    """
    coral_option = "libedgetpu1-max"
    # coral_option = "libedgetpu1-std"
    try:
        print(
            "\033[94mAttempting to install missing packages and hardware drivers from Coral\033[0m"
        )
        # Additional commands from the .sh file
        commands = [
            'echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list',
            "curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -",
            "apt-get update",
            f"apt-get install {coral_option}",
            "python3 -m pip install --extra-index-url https://google-coral.github.io/py-repo/ pycoral~=2.0",
        ]

        for command in commands:
            try:
                # Try running the command without sudo
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError:
                # If command failed, try running with sudo
                os.system(f"sudo {command}")

        print(f"\033[92mSet up installation completed.\033[0m")
    except Exception:
        print(f"\033[91mSet up installation failed to complete.\033[0m")
