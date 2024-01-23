from nanotopy.versions import nano_to_rpc


def get_commands_for_version():
    return nano_to_rpc.COMMANDS


# Usage example:
commands = get_commands_for_version()
print(commands)
