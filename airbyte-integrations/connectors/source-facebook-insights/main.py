#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#


import sys

from airbyte_cdk.entrypoint import launch
from source_facebook_insights import SourceFacebookInsights

if __name__ == "__main__":
    source = SourceFacebookInsights()
    launch(source, sys.argv[1:])
