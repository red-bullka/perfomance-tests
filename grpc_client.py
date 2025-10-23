import grpc
import greeting_pb2_grpc
import greeting_pb2


def run():
    channel = grpc.insecure_channel('localhost:50051')

    stub = greeting_pb2_grpc.GreeterStub(channel)

    request = greeting_pb2.HelloRequest(name='Мир')
    response = stub.SayHello(request)
    print("Ответ сервера:", response)


if __name__ == '__main__':
    run()