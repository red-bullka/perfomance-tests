import grpc
from concurrent import futures
import greeting_pb2
import greeting_pb2_grpc

class GreeterServicer(greeting_pb2_grpc.GreeterServicer):
    def SayHello(self, request: greeting_pb2.HelloRequest, context):
        name = request.name
        message = f"Привет, {name}!"
        print("Запрос от клиента:", request)
        return greeting_pb2.HelloReplay(message=message)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    greeting_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)

    server.add_insecure_port('[::]:50051')
    print('Запуск сервера на порту 50051...')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()