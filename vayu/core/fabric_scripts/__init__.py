import utils
from vayu.core.constants.model import machine_info

mm = machine_info("root","139.59.35.6","ahjvayu2017")

output = utils.copyMultipleFiles(mm)
print output