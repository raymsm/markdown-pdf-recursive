from mprecursive.cli import build_parser


def test_cli_argument_parsing() -> None:
    parser = build_parser()
    args = parser.parse_args([
        "./vault",
        "--output",
        "vault.pdf",
        "--toc",
        "--sort",
        "modified",
        "--ignore",
        ".git",
        "--verbose",
    ])

    assert args.path == "./vault"
    assert args.output == "vault.pdf"
    assert args.toc is True
    assert args.sort == "modified"
    assert args.ignore == [".git"]
    assert args.verbose is True
