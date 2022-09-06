#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#


import sys
import traceback

from airbyte_cdk.entrypoint import launch
from source_linkedin_pages import SourceLinkedinPages

if __name__ == "__main__":
    source = SourceLinkedinPages()
    try :
        launch(source, sys.argv[1:])
    except Exception as ex:
        print(traceback.format_exc())

