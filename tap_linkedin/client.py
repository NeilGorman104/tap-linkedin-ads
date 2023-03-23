"""REST client handling, including LinkedInStream base class."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Iterable

import requests
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
import os
from dotenv import load_dotenv

load_dotenv(".env")
LinkedInAccounts = os.getenv("TAP_LINKEDIN_ACCOUNTS")
LinkedInOwner = os.getenv("TAP_LINKEDIN_OWNER")
LinkedInCampaign = os.getenv("TAP_LINKEDIN_CAMPAIGN")
StartDateMonth = os.getenv("TAP_LINKEDIN_START_DATE_MONTH")
StartDateDay = os.getenv("TAP_LINKEDIN_START_DATE_DAY")
StartDateYear = os.getenv("TAP_LINKEDIN_START_DATE_YEAR")
EndDateMonth = os.getenv("TAP_LINKEDIN_END_DATE_MONTH")
EndDateDay = os.getenv("TAP_LINKEDIN_END_DATE_DAY")
EndDateYear = os.getenv("TAP_LINKEDIN_END_DATE_YEAR")

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class LinkedInStream(RESTStream):
    """LinkedIn stream class."""

    url_base = "https://api.linkedin.com/rest/"

    records_jsonpath = "$.elements[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.paging.start"  # Or override `get_next_page_token`.

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=self.config.get("access_token", ""),
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
            headers["LinkedIn-Version"] = self.config.get("linkedin_version")
            headers["X-Restli-Protocol-Version"] = self.config.get("x-restli-protocol-version")
            headers["Content-Type"] = self.config.get("application/json")

            
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("refresh_token")

        
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        # If pagination is required, return a token which can be used to get the
        #       next page. If this is the final page, return "None" to end the
        #       pagination loop.

        resp_json = response.json()
        if (previous_token == None):
            previous_token = 1

        if (resp_json.get("elements"))== []:
            next_page_token = None
        else:
            next_page_token = previous_token + 1

        return next_page_token

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["start"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key


        path = str(self.path)


        if str(self.path) == "adDirectSponsoredContents":
            params["q"] = "account"
            params["account"] = ("urn:li:sponsoredAccount:" + str(LinkedInAccounts))
            params["owner"] = ("urn:li:organization:" + str(LinkedInOwner))

        elif str(self.path) == "adAccounts" or str(self.path) == "adCampaigns" or str(self.path) == "adCampaignGroups":
            params["q"] = "search"
            params["sort.field"] = "ID"
            params["sort.order"] = "ASCENDING"

        elif str(self.path) == "adAccountUsers":
            params["q"] = "accounts"
            params["accounts"] = ("urn:li:sponsoredAccount:" + str(LinkedInAccounts))

        # TODO: Add method to prevent encoding of params["campaigns"]
        #       and pass the URN as a list without encoding
        elif str(self.path) == "creatives":
            params["campaigns"] = ("urn:li:sponsoredCampaign:" + str(LinkedInCampaign))
            params["q"] = "criteria"

        elif str(self.path) == "adAnalytics" and str(self.name) == "ad_analytics_by_campaign":
            params["q"] = "analytics"
            params["pivot"] = "CAMPAIGN"
            params["timeGranularity"] = "DAILY"
            params["dateRange.start.day"] = str(StartDateDay)
            params["dateRange.start.month"] = str(StartDateMonth)
            params["dateRange.start.year"] = str(StartDateYear)
            params["dateRange.end.day"] = str(EndDateDay)
            params["dateRange.end.month"] = str(EndDateMonth)
            params["dateRange.end.year"] = str(EndDateYear)
            params["campaigns[0]"] = ("urn:li:sponsoredCampaign:" + str(LinkedInCampaign))


        elif str(self.path) == "adAnalytics" and str(self.name) == "ad_analytics_by_creative":
            params["q"] = "analytics"
            params["pivot"] = "CREATIVE"
            params["timeGranularity"] = "DAILY"
            params["dateRange.start.day"] = str(StartDateDay)
            params["dateRange.start.month"] = str(StartDateMonth)
            params["dateRange.start.year"] = str(StartDateYear)
            params["dateRange.end.day"] = str(EndDateDay)
            params["dateRange.end.month"] = str(EndDateMonth)
            params["dateRange.end.year"] = str(EndDateYear)
            params["campaigns[0]"] = ("urn:li:sponsoredCampaign:" + str(LinkedInCampaign))



        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:

        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        # TODO: Delete this method if not needed.
        return row
