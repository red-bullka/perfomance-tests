from typing import TypedDict
from httpx import Response
from clients.http.client import HttpClient

class IssueVirtualCardRequestDict(TypedDict):
    userId: str
    accountId: str

class IssuePhysicalCardRequestDict(TypedDict):
    userId: str
    accountId: str

class CardsGatewayHTTPClient(HttpClient):
    def issue_virtual_card_api(self, request: IssueVirtualCardRequestDict) -> Response:
        return self.post("/api/v1/cards/issue-virtual-card", json=request)

    def issue_physical_card_api(self, request: IssuePhysicalCardRequestDict) -> Response:
        return self.post("/api/v1/cards/issue-physical-card", json=request)