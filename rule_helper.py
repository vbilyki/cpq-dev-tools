import argparse
from commands.copy_rules_between_quotes_in_workflow import add_copy_rules_arguments, copy_rules_between_quotes_in_workflow_main


def main():
    # Create the main argument parser
    parser = argparse.ArgumentParser(description="Rule Helper CLI: A tool for managing rules in workflows")

    # Add the global `-t` argument for the Bearer token
    parser.add_argument("-t", "--token", required=True, help="Bearer token for authentication")
    parser.add_argument("--type", required=True, help="Currently working with which object type")

    # Add a subparser for different commands
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Add arguments for `copy_rules`
    copy_parser = subparsers.add_parser("copy_rules", help="Copy rules between workflows")
    add_copy_rules_arguments(copy_parser)

    # Add other parsers here
    # TBA

    # Parse the arguments
    args = parser.parse_args()

    # Route to the appropriate function based on the command
    if args.command == "copy_rules" and args.type == "workflow":
        copy_rules_between_quotes_in_workflow_main(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
