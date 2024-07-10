import logging
from typing import Any, Dict, Optional
from zeep import Client, Settings
from zeep.transports import Transport
from requests import Session

logger = logging.getLogger('default')

class SOAPClient:
    def __init__(self, wsdl: str, service: Optional[str] = None, port: Optional[str] = None) -> None:
        self.wsdl: str = wsdl
        self.service: Optional[str] = service
        self.port: Optional[str] = port
        self.client: Client = self._initialize_client()
        self.headers: Dict[str, str] = {}

    def _initialize_client(self) -> Client:
        session = Session()
        settings = Settings(strict=False, xml_huge_tree=True)
        transport = Transport(session=session)
        client = Client(wsdl=self.wsdl, transport=transport, settings=settings)
        return client

    def set_headers(self, headers: Dict[str, str], override_headers: bool = False) -> None:
        if override_headers:
            self.headers = headers
        else:
            self.headers.update(headers)

    def _get_service_proxy(self) -> Any:
        if self.service and self.port:
            return self.client.bind(self.service, self.port)
        elif self.service:
            return self.client.service[self.service]
        else:
            return self.client.service

    def call_method(self, method_name: str, *args: Any, **kwargs: Any) -> Any:
        try:
            service_proxy = self._get_service_proxy()
            method = getattr(service_proxy, method_name)
            response = method(*args, **kwargs)
            return response
        except Exception as e:
            logger.error(f"An unexpected error occurred in SOAP request: {e}")
            raise e