import grpc
from concurrent import futures
import math_pb2, math_pb2_grpc

channel = grpc.insecure_channel("localhost:5440")
stub = math_pb2_grpc.CalcStub(channel)

resp = stub.Mult(math_pb2.MultReq(x=3, y=0))
print(resp.result)
