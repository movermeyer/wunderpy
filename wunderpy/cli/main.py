'''Main code called by the entry point.'''


import argparse

from wunderpy import Wunderlist
from .storage import get_token, setup
import wunderpy.cli.colors as colors


class WunderlistCLI(object):
    '''Manage state for the CLI client.'''

    def __init__(self):
        self.wunderlist = None
        self.get_wunderlist()

    def get_wunderlist(self):
        '''Get a Wunderlist instance and a token'''

        try:
            token = get_token()
        except IOError:  # first run
            setup()
            token = get_token()

        wunderlist = Wunderlist()
        wunderlist.set_token(token)
        wunderlist.update_lists()
        self.wunderlist = wunderlist

    def add(self, task, list_title):
        '''Add a task or create a list.
        If just --task is used, optionally with --list, add a task.
        If just --list is used, create an empty list.
        '''

        if task and list_title:  # adding a task to a list
            self.wunderlist.add_task(task, list=list_title)
        elif list_title != "inbox":  # creating a list
            self.wunderlist.add_list(list_title)

    def complete(self, task, list_title):
        '''Complete a task'''

        self.wunderlist.complete_task(task, list_title=list_title)

    def delete_task(self, task, list_title):
        '''Delete a task
        --list can be used to specify what list it's in
        '''

        self.wunderlist.delete_task(task, list_title)

    def delete_list(self, list_title):
        '''Delete a list specified by --list'''

        self.wunderlist.delete_list(list_title)

    def overview(self, num_tasks):
        '''Display an overview of all lists'''

        for title, task_list in self.wunderlist.lists.items():
            tasks = task_list["tasks"]
            pretty_print_list(title)

            task_count = 0
            for task_title, info in tasks.items():
                if task_count < num_tasks:
                    pretty_print_task(task_title, info)
                    task_count += 1
                else:
                    break
            print("")

    def display(self, list_title):
        '''Display all tasks in a list'''

        try:
            new_list = self.wunderlist.lists[list_title]
        except KeyError:
            print("List {} does not exist.".format(list_title))
            exit()

        pretty_print_list(list_title)

        for task_title, info in new_list["tasks"].items():
            pretty_print_task(task_title, info)


def pretty_print_list(title):
    '''Print a list title on the command line with bold and underline'''

    with colors.pretty_output(colors.BOLD, colors.UNDERSCORE) as out:
        out.write(title)


def pretty_print_task(title, info):
    '''Print a task and related information
    Format looks like [check] title (star)
    '''

    check = u"\u2713"
    star = u"\u2605"

    is_completed = check  # in other words, True
    if not info["completed_at"]:
        is_completed = " "  # not completed, False

    use_star = star  # True
    if not info["starred"]:
        use_star = ""  # False

    line = u"[{}] {} {}".format(is_completed, title, use_star)
    print(line)


def main():
    '''Entry point for the wunderlist command.
    Get options from argparse and call according methods
    in WunderlistCLI
    '''

    parser = argparse.ArgumentParser(description="A Wunderlist CLI client.")

    parser.add_argument("-a", "--add", dest="add", action="store_true",
                        default=False, help="Add a task or list.")
    parser.add_argument("-c", "--complete", dest="complete",
                        action="store_true", default=False,
                        help="Complete a task.")
    parser.add_argument("-d", "--delete", dest="delete", action="store_true",
                        default=False, help="Delete a task or list.")
    parser.add_argument("-o", "--overview", dest="overview",
                        action="store_true", default=False,
                        help="Display an overview of your Wunderlist.")
    parser.add_argument("--display", dest="display", action="store_true",
                        default=False, help="Display all items in a list "
                        "specified with --list.")
    parser.add_argument("-l", "--list", dest="list", default="inbox",
                        help="Used to specify a list, either for a task in a "
                        "certain list, or for a command that only operates "
                        "on lists. Default is inbox.")
    parser.add_argument("-n", "--num", dest="num_tasks", type=int, default=5,
                        help="Choose the number of tasks to display from "
                        "each list [default 5]")                    
    parser.add_argument("-t", "--task", dest="task",
                        help="Used to specify a task name.")
    args = parser.parse_args()

    cli = WunderlistCLI()

    if args.add:
        cli.add(args.task, args.list)
    elif args.complete:
        cli.complete(args.task, args.list)
    elif args.delete:
        if args.task:
            cli.delete_task(args.task, args.list)
        else:
            cli.delete_list(args.list)
    elif args.overview:
        cli.overview(args.num_tasks)
    elif args.display:
        cli.display(args.list)
    else:
        cli.overview(args.num_tasks)
