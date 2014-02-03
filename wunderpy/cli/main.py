'''Command line script for wunderpy.'''


import argparse
from datetime import date, timedelta

from wunderpy import Wunderlist
from .storage import get_token, setup
import colors


class WunderlistCLI(object):
    def __init__(self):
        self.wunderlist = None
        self.get_wunderlist()

    def get_wunderlist(self):
        try:
            token = get_token()
        except IOError:  # first run
            setup()
            token = get_token()

        wunderlist = Wunderlist()
        wunderlist.set_token(token)
        wunderlist.update_lists()
        self.wunderlist = wunderlist

    def add(self, task, list):
        '''Add a task or create a list.
        If just --task is used, optionally with --list, add a task.
        If just --list is used, create an empty list.
        '''

        if task and list:  # adding a task to a list
            self.wunderlist.add_task(task, list=list)
        elif list != "inbox":  # creating a list
            self.wunderlist.add_list(list)

    def complete(self, task, list):
        self.wunderlist.complete_task(task, list_title=list)

    def delete_task(self, task, list):
        self.wunderlist.delete_task(task, list)

    def delete_list(self, list):
        self.wunderlist.delete_list(list)

    def overview(self, num_tasks, only_incomplete):
        for title, list in self.wunderlist.lists.iteritems():
            tasks = list["tasks"]
            with colors.pretty_output(colors.BOLD, colors.UNDERSCORE) as out:
                out.write(title)

            task_count = 0
            for task_title, info in tasks.iteritems():
                # if only_incomplete is true, we want to make sure it hasn't
                # already been completed:
                if not only_incomplete or not info["completed_at"]:
                    if task_count < num_tasks:
                        pretty_print_task(task_title, info)
                        task_count += 1
                    else:
                        break
            print("")

    def tasks_within_n_days(self, n):
        cur_date = date.today()
        for title, list in self.wunderlist.lists.iteritems():
            needs_header = True
            tasks = list["tasks"]
            for task_title, info in tasks.iteritems():
                # only display tasks that are incomplete and have a due date
                if not info["completed_at"] and info["due_date"]:
                    task_date = info["due_date"].split('-')
                    year = int(task_date[0])
                    month = int(task_date[1])
                    day = int(task_date[2])
                    task_date = date(year, month, day)
                    if task_date <= cur_date + timedelta(n):
                        if needs_header:
                            needs_header = False
                            with colors.pretty_output(colors.BOLD,
                                                      colors.UNDERSCORE) as o:
                                o.write(title)
                        pretty_print_task(task_title, info)
        print("")

    def today(self):
        return self.tasks_within_n_days(0)

    def week(self):
        return self.tasks_within_n_days(6)

    def display(self, list_title, only_incomplete):
        try:
            list = self.wunderlist.lists[list_title]
        except KeyError:
            print("That list does not exist.")
            exit()

        with colors.pretty_output(colors.BOLD, colors.UNDERSCORE) as out:
            out.write(list_title)

        for task_title, info in list["tasks"].iteritems():
            # if only_incomplete is true, we want to make sure it hasn't
            # already been completed:
            if not only_incomplete or not info["completed_at"]:
                pretty_print_task(task_title, info)


def pretty_print_task(title, info):
    CHECK = u"\u2713".encode("utf-8")
    STAR = u"\u2605".encode("utf-8")

    is_completed = CHECK  # in other words, True
    if not info["completed_at"]:
        is_completed = " "  # not completed, False

    use_star = STAR  # True
    if not info["starred"]:
        use_star = ""  # False

    line = "[{}] {} {}".format(is_completed, title, use_star)
    print(line)


def main():
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
    parser.add_argument("--week", dest="week", action="store_true",
                        default=False, help="Display all incomplete tasks"
                        "that are overdue or due in the next week.")
    parser.add_argument("--today", dest="today", action="store_true",
                        default=False, help="Display all incomplete tasks "
                        "that are overdue or due today.")
    parser.add_argument("--display", dest="display", action="store_true",
                        default=False, help="Display all items in a list "
                        "specified with --list.")
    parser.add_argument("-i", "--incomplete", dest="only_incomplete",
                        action="store_true", default=False,
                        help="Only show incomplete tasks in overview.")
    parser.add_argument("-n", "--num", dest="num_tasks", type=int, default=5,
                        help="Choose the number of tasks to display from "
                        "each list. [default 5]")
    parser.add_argument("-l", "--list", dest="list", default="inbox",
                        help="Used to specify a list, either for a task in a "
                        "certain list, or for a command that only operates "
                        "on lists. Default is inbox.")
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
    elif args.today:
        cli.today()
    elif args.week:
        cli.week()
    elif args.overview:
        cli.overview(args.num_tasks, args.only_incomplete)
    elif args.display:
        cli.display(args.list, args.only_incomplete)
    else:
        cli.overview(args.num_tasks, args.only_incomplete)
