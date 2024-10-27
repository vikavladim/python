import argparse
import json
import logging

import grpc
import ship_pb2
import ship_pb2_grpc
from google.protobuf import json_format


def parse_args():
    parser = argparse.ArgumentParser(description='Reporting client')
    parser.add_argument('right_ascention_hours', type=float, help='Right ascention hours')
    parser.add_argument('right_ascention_minutes', type=float, help='Right ascention minutes')
    parser.add_argument('right_ascention_seconds', type=float, help='Right ascention seconds')
    parser.add_argument('declination_degrees', type=float, help='Declination degrees')
    parser.add_argument('declination_minutes', type=float, help='Declination minutes')
    parser.add_argument('declination_seconds', type=float, help='Declination seconds')
    return parser.parse_args()


def run():
    args = parse_args()
    coordinates = ship_pb2.Coordinates(
        right_ascention=ship_pb2.RigthAscention(
            hours=args.right_ascention_hours,
            minutes=args.right_ascention_minutes,
            seconds=args.right_ascention_seconds
        ),
        declination=ship_pb2.Declination(
            degrees=args.declination_degrees,
            minutes=args.declination_minutes,
            seconds=args.declination_seconds
        )
    )

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ship_pb2_grpc.ShipServiceStub(channel)
        response = stub.get_ships(coordinates)
        print(json_format.MessageToJson(
            response,
            preserving_proto_field_name=True,
            always_print_fields_with_no_presence=True))


if __name__ == "__main__":
    logging.basicConfig()
    run()
