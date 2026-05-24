import os

from utils import LoopReporter


def test_loop_reporter():
    columns = os.get_terminal_size().columns
    printout_components = ["add", " some", " printout"]
    loop_reporter = LoopReporter()
    loop_reporter.add_printout(printout_components[0])
    loop_reporter.add_printout(printout_components[1])
    loop_reporter.add_printout(printout_components[2])
    final_printout = (
        printout_components[0] + printout_components[1] + printout_components[2]
    )
    final_printout += " " * (columns - len(final_printout)) + "\r"
    assert loop_reporter.print() == final_printout


def test_loop_reporter_carriage_return():
    loop_reporter = LoopReporter()
    loop_reporter.add_printout("some printout")
    printout = loop_reporter.print()
    assert printout[-1] == "\r"


def test_loop_reporter_terminal_limit():
    columns = os.get_terminal_size().columns
    long_text = "test" * int(columns / 2)
    loop_reporter = LoopReporter()
    loop_reporter.add_printout(long_text)
    printout = loop_reporter.print()
    # + 1 for "\r"
    assert len(printout) == (columns + 1)
