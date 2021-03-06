import logging, coloredlogs
import getpass

logging.basicConfig(
    filename="/tmp/beta_daq.log",
    filemode="a",
    format="[%(asctime)s] [User:{}] [%(threadName)s] [%(name)s] [%(levelname)s]: %(message)s".format(getpass.getuser()),
)
log = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=log)

from BetaDAQ import BetaDAQ


def run_daq():
    log.info("BetaScope DAQ is created")

    DAQ = BetaDAQ()
    DAQ.BetaMeas()

    log.info("DAQ is closed")
    DAQ.instruments["hv_ps"].Close()
