#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#


import sys

from airbyte_cdk.entrypoint import launch
from source_linkedin_iiidata import SourceLinkedinIiidata

if __name__ == "__main__":
    source = SourceLinkedinIiidata()
    launch(source, sys.argv[1:])
