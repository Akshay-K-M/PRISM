import logging
from pathlib import Path


EXTRACTOR_NAMES = {"Executable",
                   "Initiator",
                   "Union",
                   "Database_Restorer",
                   "FromClause",
                   "cs2",
                   "Union_fc",
                   "Zero_Result_Executable",
                   "Null_Free_Executable",
                   "Scale Down",
                   "View_Minimizer",
                   "NEP_Minimizer",
                   "Where_clause",
                   "Result_Comparator",
                   "Filter",
                   "Group_By",
                   "Order_By",
                   "NEP Extractor",
                   "Projection",
                   "Limit",
                   "Aggregation",
                   "Outer_Join",
                   "Equi_Join",
                   "InequalityPredicate"}

BOOLEAN_RELATED = {"Where_clause",
                   "Filter",
                   "Equi_Join",
                   "InequalityPredicate"}

def get_format_args(msg, args):
    f_msg = format(str(msg))
    f_args = [f_msg]
    for arg in args:
        f_args.append(format(str(arg)))
    f_msg = ""
    for i in range(len(f_args)):
        f_msg += "%s "
    return f_msg, f_args

def create_logger(name="", level=""):
    if name in BOOLEAN_RELATED:
        return Log(name, level)
    return Log()


class Log(logging.Logger):
    isDummy = False
    # creating a formatter
    formatter = logging.Formatter('%(asctime)s- %(name)s - %(levelname)-8s: %(message)s')

    def __init__(self, name="", level=""):
        if level != "":
            super().__init__(name, level)
            self.base_path = Path(__file__).parent.parent.parent.parent
            log_file = (self.base_path / "unmasque.log").resolve()
            fh = logging.FileHandler(log_file, 'a')
            fh.setLevel(level)
            fh.setFormatter(self.formatter)
            self.addHandler(fh)
            self.isDummy = False
        else:
            self.isDummy = True

    def __del__(self):
        if not self.isDummy:
            fh = self.handlers[0]
            self.removeHandler(fh)
            fh.close()

    def debug(self, msg, *args):
        if self.isDummy:
            return
        f_msg, f_args = get_format_args(msg, args)
        super().debug(f_msg, *f_args)

    def error(self, msg, *args):
        if self.isDummy:
            return
        f_msg, f_args = get_format_args(msg, args)
        super().error(f_msg, *f_args)

    def info(self, msg, *args):
        if self.isDummy:
            return
        f_msg, f_args = get_format_args(msg, args)
        super().info(f_msg, *f_args)

    def warning(self, msg, *args):
        if self.isDummy:
            return
        f_msg, f_args = get_format_args(msg, args)
        super().info(f_msg, *f_args)
