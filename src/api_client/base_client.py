import logging
from typing import List, Union

from aiohttp import (
    ClientConnectionError,
    ClientOSError,
    ClientPayloadError,
    ClientResponseError,
    ClientSession,
)
from pydantic import BaseModel

from api_client.client_errors import NotFoundError


class BaseClient:
    def __init__(self, base_url: str, session: ClientSession, endpoint: str):
        self.base_url = base_url
        self.session = session
        self.endpoint = endpoint

    async def request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        try:
            async with self.session.request(method, url, **kwargs) as response:
                response.raise_for_status()

                if response.status == 204:
                    return None

                return await response.json()

        except ClientResponseError as e:
            if e.status == 404:
                logging.warning(f"Resource not found at {e.request_info.url}")
                raise NotFoundError(
                    f"Resource not found at {e.request_info.url}"
                )
            elif e.status == 403:
                logging.warning(
                    f"Access forbidden to resource at {e.request_info.url}"
                )
                raise PermissionError(
                    "Access denied to the requested resource."
                )
            elif e.status == 500:
                logging.error(f"Server error at {e.request_info.url}")
                raise RuntimeError("The server encountered an internal error.")
            else:
                logging.error(
                    f"HTTP Error {e.status} at "
                    "{e.request_info.url}: {e.message}"
                )
                raise e

        except ClientConnectionError:
            logging.error(f"Failed to connect to server at {url}")
            raise

        except ClientOSError as e:
            logging.error(f"OS error occurred while accessing {url}: {e}")
            raise

        except ClientPayloadError as e:
            logging.error(
                f"Payload error while processing response from {url}: {e}"
            )
            raise

        except Exception:
            logging.exception("Unexpected error occurred during request")
            raise

    async def close(self):
        await self.session.close()

    async def get_by_id(self, item_id: int):
        response = await self.request("GET", f"{self.endpoint}/{item_id}")
        return response

    async def list(self, **params):
        return await self.request("GET", self.endpoint, params=params)

    async def create(self, data: BaseModel):
        return await self.request(
            "POST", self.endpoint, json=data.model_dump()
        )

    async def update(self, item_id: int, data: Union[BaseModel, dict]):
        json_data = data.model_dump() if isinstance(data, BaseModel) else data
        return await self.request(
            "PUT", f"{self.endpoint}/{item_id}", json=json_data
        )

    async def delete(self, item_id: int):
        return await self.request("DELETE", f"{self.endpoint}/{item_id}")

    async def bulk_create(self, items_data: List[BaseModel]):
        data = [item.model_dump(mode="json") for item in items_data]
        return await self.request(
            "POST", f"{self.endpoint}/bulk_create", json=data
        )
