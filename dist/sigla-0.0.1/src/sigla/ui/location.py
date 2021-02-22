"""Send greetings."""

import arrow
import sys

def greet(tz):
    """Greet a location."""
    now = arrow.now(tz)
    friendly_time = now.format("h:mm a")
    location = tz.split("/")[-1].replace("_"," ")
    return f"Hello, {location}! The time is {friendly_time}."


def cli(args=None):
    """
        Process command line arguments.
    """
    if not args:
        args = sys.argv[1:]
    tz = args[0]
    print(greet(tz))