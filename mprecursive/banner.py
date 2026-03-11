"""CLI banner utilities for MPRecursive.

Developed by: raymsm
GitHub: https://github.com/raymsm
"""

CYAN = "\033[96m"
RESET = "\033[0m"


def render_banner() -> str:
    """Return the startup banner with ANSI colors."""
    return (
        f"{CYAN}╔══════════════════════════════════════╗\n"
        "║        MPRecursive CLI Tool          ║\n"
        "║   Markdown / Document PDF Engine     ║\n"
        "║                                      ║\n"
        "║       Developed by raymsm            ║\n"
        "║     github.com/raymsm                ║\n"
        f"╚══════════════════════════════════════╝{RESET}"
    )
