# -*- coding:utf-8 -*-
from Urlmanager.encyclopedia_url import main as url_main
from DataOutput.encyclopedia_html import main as dop_main
from Analysis.encyclopedia_als import main as als_main
from Storage.encyclopedia_sto import main as sto_main


if __name__ == '__main__':
    url_main()
    dop_main()
    als_main()
    sto_main()
