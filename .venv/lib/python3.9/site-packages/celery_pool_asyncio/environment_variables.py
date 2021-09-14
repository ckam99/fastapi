import os

def init_deny_targets():
    """Read and parse environment variable"""
    deny_targets = os.getenv('CPA_MONKEY_DENY')

    if not deny_targets:
        return frozenset()

    deny_targets = deny_targets.split(',')
    return frozenset(deny_targets)


deny_targets = init_deny_targets()


def monkey_available(key):
    return key not in deny_targets
