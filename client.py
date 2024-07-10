from soap import SOAPClient

wsdl_url = 'http://127.0.0.1:8088/mockNumberConversionSoapBinding?WSDL'
client = SOAPClient(wsdl_url, service=None, port=None)



# Call a SOAP method
response = client.call_method('mockNumberConversionSoapBinding')

