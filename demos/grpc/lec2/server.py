import grpc
from concurrent import futures
import math_pb2, math_pb2_grpc
import traceback

class MyCalc(math_pb2_grpc.CalcServicer):
    def Mult(self, request, context):
        try:
            print(request)
            print(request.x, request.y)
            return math_pb2.MultResp(result=request.x * request.Y)
        except Exception:
            traceback.print_exc()


print("start server")
server = grpc.server(futures.ThreadPoolExecutor(max_workers=1), options=[("grpc.so_reuseport", 0)])
math_pb2_grpc.add_CalcServicer_to_server(MyCalc(), server)
server.add_insecure_port("0.0.0.0:5440")
server.start()
server.wait_for_termination()
