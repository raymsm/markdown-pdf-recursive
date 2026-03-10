"""CLI banner utilities for MPRecursive.

Developed by: raymsm
GitHub: https://github.com/raymsm
"""

try:
    from colorama import Fore, Style
except ModuleNotFoundError:
    class _NoColor:
        CYAN = ""
        RESET_ALL = ""

    Fore = Style = _NoColor()


def render_banner() -> str:
    """Return the startup banner with ANSI colors."""
    return (
        f"{Fore.CYAN}╔══════════════════════════════════════╗\n"
        "║        MPRecursive CLI Tool          ║\n"
        "║   Markdown / Document PDF Engine     ║\n"
        "║                                      ║\n"
        "║       Developed by raymsm            ║\n"
        "║     github.com/raymsm                ║\n"
        f"╚══════════════════════════════════════╝{Style.RESET_ALL}"
    )
