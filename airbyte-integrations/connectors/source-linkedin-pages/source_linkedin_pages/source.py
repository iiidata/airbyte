#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#


from abc import ABC
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple

import requests
import time

from airbyte_cdk import AirbyteLogger
from airbyte_cdk.models import SyncMode
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpSubStream,HttpStream
from airbyte_cdk.sources.streams.http.auth import Oauth2Authenticator, TokenAuthenticator
from urllib.parse import quote,urlencode
import os 

class LinkedinPagesStream(ABC):

    url_base = "https://api.linkedin.com/v2/"
    primary_key = None
    records_limit = 100
    # list_posts_id = []
    # list_posts_id_clean = ""

    def __init__(self, config):
        #super().__init__(authenticator=config.get("authenticator"))
        self.config = config
    
    @property
    def org(self):
        """Property to return the user Organization Id from input"""
        return self.config.get("org_id")

    def path(self, **kwargs) -> str:
        """Returns the API endpoint path for stream, from `endpoint` class attribute."""
        return self.endpoint

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        return None

    def parse_response(
        self, response: requests.Response, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None
    ) -> Iterable[Mapping]:
        return [response.json()]

    def should_retry(self, response: requests.Response) -> bool:
        if response.status_code == 429:
            error_message = (
                f"Stream {self.name}: LinkedIn API requests are rate limited. "
                f"Rate limits specify the maximum number of API calls that can be made in a 24 hour period. "
                f"These limits reset at midnight UTC every day. "
                f"You can find more information here https://docs.airbyte.io/integrations/sources/linkedin-pages. "
                f"Also quotas and usage are here: https://www.linkedin.com/developers/apps."
            )
            self.logger.error(error_message)
        return super().should_retry(response)

class LinkedinPagesHttpStream(LinkedinPagesStream,HttpStream):
    def __init__(self, config):
        LinkedinPagesStream.__init__(self,config)
        HttpStream.__init__(self,authenticator=config.get("authenticator"))

class OrganizationLookup(LinkedinPagesHttpStream):
    def path(self, stream_state: Mapping[str, Any], **kwargs) -> MutableMapping[str, Any]:

        path = f"organizations/{self.org}"
        return path

class FollowerStatistics(LinkedinPagesHttpStream):
    def path(self, stream_state: Mapping[str, Any], **kwargs) -> MutableMapping[str, Any]:

        path = f"organizationalEntityFollowerStatistics?q=organizationalEntity&organizationalEntity=urn:li:organization:{self.org}"
        return path

    def parse_response(
        self, response: requests.Response, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None
    ) -> Iterable[Mapping]:
        yield from response.json().get("elements")


class ShareStatistics(LinkedinPagesHttpStream):
    def path(self, stream_state: Mapping[str, Any], **kwargs) -> MutableMapping[str, Any]:
#organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity=urn:li:organization:2414183&timeIntervals.timeGranularityType=DAY&timeIntervals.timeRange.start=1551398400000&timeIntervals.timeRange.end=1552003200000
        ts = time.time()
        path = f"organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity=urn%3Ali%3Aorganization%3A{self.org}&timeIntervals.timeGranularityType=DAY&timeIntervals.timeRange.start={ts * 1000}&timeIntervals.timeRange.end={(ts + 86400)*1000}"
        return path

    def parse_response(
        self, response: requests.Response, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None
    ) -> Iterable[Mapping]:
        yield from response.json().get("elements")


class TotalFollowerCount(LinkedinPagesHttpStream):
    def path(self, stream_state: Mapping[str, Any], **kwargs) -> MutableMapping[str, Any]:

        path = f"networkSizes/urn:li:organization:{self.org}?edgeType=CompanyFollowedByMember"
        return path

class PostsOrganization(LinkedinPagesHttpStream):
    def __init__(self, config):
        super().__init__(config)
        self.list_posts_id = []
        self.list_posts_id_clean = ""

    def path(self, stream_state: Mapping[str, Any], **kwargs) -> MutableMapping[str, Any]:

        path = f"ugcPosts?q=authors&authors=List(urn%3Ali%3Aorganization%3A{self.org})"
        return path

    def request_headers(self, stream_state: Mapping[str, Any], **kwargs) -> Mapping[str, Any]:
        """
        If account_ids are specified as user's input from configuration,
        we must use MODIFIED header: {'X-RestLi-Protocol-Version': '2.0.0'}
        """
        return {"X-RestLi-Protocol-Version": "2.0.0"}
    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        parsed_response = response.json()
        if len(parsed_response.get("elements")) < self.records_limit:
            return None
        return {"start": parsed_response.get("paging").get("start") + self.records_limit}
    
    def request_params(
        self, stream_state: Mapping[str, Any], next_page_token: Mapping[str, Any] = None, **kwargs
    ) -> MutableMapping[str, Any]:
        params = {"count": self.records_limit}
        if next_page_token:
            params.update(**next_page_token)
        return params
    
    def parse_response(
        self, response: requests.Response, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None
    ) -> Iterable[Mapping]:
        yield from response.json().get("elements")
    

class PostsOrgInsights(LinkedinPagesStream,HttpSubStream):
    
    def __init__(self, config):
        LinkedinPagesStream.__init__(self,config)
        HttpSubStream.__init__(self,authenticator=config.get("authenticator"),parent=PostsOrganization(config))     
        
    def path(self, stream_slice: Mapping[str, Any] = None, **kwargs) -> str:
        id_list = map(lambda element : quote(element["id"]),stream_slice['parent'])
        return "socialActions?ids=List(%s)"%(",".join(id_list))

    def stream_slices(
        self, sync_mode: SyncMode, cursor_field: List[str] = None, stream_state: Mapping[str, Any] = None
    ) -> Iterable[Optional[Mapping[str, Any]]]:
        parent_stream_slices = self.parent.stream_slices(
            sync_mode=SyncMode.full_refresh, cursor_field=cursor_field, stream_state=stream_state
        )

        # iterate over all parent stream_slices
        parent_records = self.parent.read_records(
            sync_mode=SyncMode.full_refresh, cursor_field=cursor_field, stream_slice=None, stream_state=stream_state
        )
        slice_number = 0
        sub_record_list = []
        for record in parent_records:
            sub_record_list.append(record)
            if slice_number % 60 == 0:
                yield {"parent": sub_record_list}
                sub_record_list.clear()
            slice_number += 1
        yield {"parent": sub_record_list}
        sub_record_list.clear()
        
    def request_headers(self, stream_state: Mapping[str, Any], **kwargs) -> Mapping[str, Any]:
        """
        If account_ids are specified as user's input from configuration,
        we must use MODIFIED header: {'X-RestLi-Protocol-Version': '2.0.0'}
        """
        return {"X-RestLi-Protocol-Version": "2.0.0"}

    # def parse_response(
    #     self, response: requests.Response, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None
    # ) -> Iterable[Mapping]:
    #     yield from response.json().get("results").values()
        
        
        
    


class SourceLinkedinPages(AbstractSource):
    """
    Abstract Source inheritance, provides:
    - implementation for `check` connector's connectivity
    - implementation to call each stream with it's input parameters.
    """

    @classmethod
    def get_authenticator(cls, config: Mapping[str, Any]) -> TokenAuthenticator:
        """
        Validate input parameters and generate a necessary Authentication object
        This connectors support 2 auth methods:
        1) direct access token with TTL = 2 months
        2) refresh token (TTL = 1 year) which can be converted to access tokens
           Every new refresh revokes all previous access tokens q
        """
        auth_method = config.get("credentials", {}).get("auth_method")
        if not auth_method or auth_method == "access_token":
            # support of backward compatibility with old exists configs
            access_token = config["credentials"]["access_token"] if auth_method else config["access_token"]
            return TokenAuthenticator(token=access_token)
        elif auth_method == "oAuth2.0":
            return Oauth2Authenticator(
                token_refresh_endpoint="https://www.linkedin.com/oauth/v2/accessToken",
                client_id=config["credentials"]["client_id"],
                client_secret=config["credentials"]["client_secret"],
                refresh_token=config["credentials"]["refresh_token"],
            )
        raise Exception("incorrect input parameters")

    def check_connection(self, logger: AirbyteLogger, config: Mapping[str, Any]) -> Tuple[bool, any]:
        # RUN $ python main.py check --config secrets/config.json

        """
        Testing connection availability for the connector.
        :: for this check method the Customer must have the "r_liteprofile" scope enabled.
        :: more info: https://docs.microsoft.com/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin
        """
        config["authenticator"] = self.get_authenticator(config)
        stream = OrganizationLookup(config)
        stream.records_limit = 1
        try:
            next(stream.read_records(sync_mode=SyncMode.full_refresh), None)
            return True, None
        except Exception as e:
            return False, e

        # RUN: $ python main.py read --config secrets/config.json --catalog integration_tests/configured_catalog.json

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        config["authenticator"] = self.get_authenticator(config)
        return [
            OrganizationLookup(config),
            PostsOrganization(config),
            FollowerStatistics(config),
            ShareStatistics(config),
            TotalFollowerCount(config),
            PostsOrgInsights(config)
        ]
