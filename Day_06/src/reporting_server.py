import logging
from concurrent import futures

import grpc

import ship_pb2_grpc
import ship_pb2

import random
from faker import Faker
from google.protobuf.json_format import MessageToJson

fake = Faker()

prepared_officers = []

for _ in range(30):
    officer = ship_pb2.Officer(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        rank=fake.job())
    prepared_officers.append(officer)


def generate_ship_response():
    alignment = random.choice([ship_pb2.Alignment.Ally, ship_pb2.Alignment.Enemy])
    ship_class = random.choice(
        [
            ship_pb2.ShipClass.Corvette,
            ship_pb2.ShipClass.Destroyer,
            ship_pb2.ShipClass.Cruiser,
            ship_pb2.ShipClass.Frigate,
            ship_pb2.ShipClass.Carrier,
            ship_pb2.ShipClass.Dreadnought
        ]
    )
    if alignment == ship_pb2.Alignment.Enemy and random.random() < 0.3:
        name = "Unknown"
    else:
        name = fake.name()
    length = random.uniform(50, 5e4)
    crew_size = random.randint(1, 1000)
    is_armed = random.choice([True, False])
    officers = []
    for _ in range(random.randint(1, 5)):
        # officer = ship_pb2.Officer(
        #     first_name=fake.first_name(),
        #     last_name=fake.last_name(),
        #     rank=fake.job()
        # )
        # officers.append(officer)
        officers.append(random.choice(prepared_officers))


    return ship_pb2.ShipResponse(
        alignment=alignment,
        ship_class=ship_class,
        name=name,
        length=length,
        crew_size=crew_size,
        is_armed=is_armed,
        officers=officers
    )


class ShipService(ship_pb2_grpc.ShipServiceServicer):
    def get_ships(self, request, context):
        print(request)
        return ship_pb2.ShipResponseList(responses=[generate_ship_response() for _ in range(10)])


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    ship_pb2_grpc.add_ShipServiceServicer_to_server(ShipService(), server)
    server.add_insecure_port("localhost:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
