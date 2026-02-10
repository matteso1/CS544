import flask
from flask import Flask
import grpc
import property_pb2
import property_pb2_grpc
import os

app = Flask("p2")

project = os.environ.get("PROJECT", "p2")
servers = [
    f"{project}-java-dataset-1:5000",
    f"{project}-java-dataset-2:5000",
]
channels = [grpc.insecure_channel(s) for s in servers]
stubs = [property_pb2_grpc.PropertyLookupStub(ch) for ch in channels]

next_server = 0

@app.route("/address/<parcel>")
def address(parcel):
    global next_server
    idx = next_server
    next_server = (next_server + 1) % len(stubs)
    source = str(idx + 1)
    try:
        response = stubs[idx].AddressByParcel(property_pb2.ParcelRequest(parcel=parcel))
        return flask.jsonify({"addrs": list(response.addresses), "source": source, "error": None})
    except grpc.RpcError as e:
        return flask.jsonify({"addrs": [], "source": source, "error": str(e)})

def main():
    app.run("0.0.0.0", port=8080, debug=False, threaded=False)

if __name__ == "__main__":
    main()
