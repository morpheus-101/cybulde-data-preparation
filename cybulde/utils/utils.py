import logging
import socket
import subprocess

logging.basicConfig()


def get_logger(name: str) -> logging.Logger:
    return logging.Logger(f"[{socket.gethostname()}] {name}")


def run_shell_command(cmd: str) -> str:
    return subprocess.run(cmd, text=True, shell=True, check=True, capture_output=True).stdout