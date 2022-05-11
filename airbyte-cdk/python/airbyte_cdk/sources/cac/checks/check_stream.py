#
# Copyright (c) 2021 Airbyte, Inc., all rights reserved.
#
from typing import TYPE_CHECKING, Tuple

from airbyte_cdk.models.airbyte_protocol import SyncMode
from airbyte_cdk.sources.cac.checks.connection_checker import ConnectionChecker

if TYPE_CHECKING:
    pass


class CheckStream(ConnectionChecker):
    # FIXME: needs to implemeent an interface
    def __init__(self, stream, vars=None, config=None):
        # print(f"stream_config: {stream}")
        # print(f"stremconfig.config: {stream}")
        self._stream = stream
        # print(f"created chck stream with: {self._stream_config}")
        self._vars = vars
        self._config = config

    def check_connection(self, logger, config) -> Tuple[bool, any]:
        try:
            # print(f"stream: {self._stream_config}")
            # stream = LowCodeComponentFactory().create_component(self._stream_config, self._vars, config)
            # print("stream was created!!!!!")
            records = self._stream.read_records(sync_mode=SyncMode.full_refresh)
            print(f"RECORDS: {records}")
            next(records)
            return True, None
        except Exception as error:
            return False, f"Unable to connect to stream {self._stream} - {error}"