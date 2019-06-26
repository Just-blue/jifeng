
from scrapy import cmdline
import os

name = 'jifeng'
cmd = 'scrapy crawl {0}'.format(name)
# os.system(cmd)

cmdline.execute(cmd.split())
