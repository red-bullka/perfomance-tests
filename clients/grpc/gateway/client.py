from grpc import Channel, insecure_channel


def build_gateway_grpc_client() -> Channel:
    return insecure_channel('http://localhost:9003')