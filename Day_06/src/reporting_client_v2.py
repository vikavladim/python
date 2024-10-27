import argparse
import json
import logging

import grpc
from ship_pb2 import *
import ship_pb2_grpc
from google.protobuf import json_format
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from typing import List


class OfficerPydantic(BaseModel):
    first_name: str
    last_name: str
    rank: str


class SpaceshipPydantic(BaseModel):
    alignment: Alignment = Alignment.Ally
    name: str
    ship_class: ShipClass
    length: float
    crew_size: int
    is_armed: bool
    officers: List[OfficerPydantic] = []

    @model_validator(mode='after')
    def checker(self):
        if self.alignment==Alignment.Ally and self.name == 'Unknown':
            raise ValueError('Unknown ally')
        if ((self.ship_class == ShipClass.Corvette
                and (self.length < 80 or self.length > 250 or self.crew_size < 4 or self.crew_size > 10))
            or (self.ship_class == ShipClass.Frigate and (
                        self.length < 300 or self.length > 600 or self.crew_size < 10 or self.crew_size > 15 or self.alignment == Alignment.Enemy))
            or (self.ship_class == ShipClass.Cruiser and (
                        self.length < 500 or self.length > 1000 or self.crew_size < 15 or self.crew_size > 30))
            or (self.ship_class == ShipClass.Destroyer and (
                        self.length < 800 or self.length > 2000 or self.crew_size < 50 or self.crew_size > 80 or self.alignment == Alignment.Enemy))
            or (self.ship_class == ShipClass.Carrier and (
                        self.length < 1000 or self.length > 4000 or self.crew_size < 120 or self.crew_size > 250 or self.is_armed == True))
            or (self.ship_class == ShipClass.Dreadnought and (
                        self.length < 5000 or self.length > 20000 or self.crew_size < 300 or self.crew_size > 500 or self.alignment == Alignment.Enemy))):
                raise ValueError("Ivanlid")
        return self

    class Config:
        arbitrary_types_allowed = True
        # json_encoders = {
        #     Officer: lambda x: x.__dict__,
        # }

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
    coordinates = Coordinates(
        right_ascention=RigthAscention(
            hours=args.right_ascention_hours,
            minutes=args.right_ascention_minutes,
            seconds=args.right_ascention_seconds
        ),
        declination=Declination(
            degrees=args.declination_degrees,
            minutes=args.declination_minutes,
            seconds=args.declination_seconds
        )
    )

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ship_pb2_grpc.ShipServiceStub(channel)
        response = stub.get_ships(coordinates)
        # print(json_format.MessageToJson(
        #     response,
        #     preserving_proto_field_name=True,
        #     always_print_fields_with_no_presence=True))
        for ship in response.responses:
            try:
                SpaceshipPydantic(**json.loads(json_format.MessageToJson(
                    ship,
                    preserving_proto_field_name=True,
                    always_print_fields_with_no_presence=True)))
                print(ship)
            except ValueError as e:
                print(f'Корабль не прошёл проверку: {e}')


if __name__ == "__main__":
    logging.basicConfig()
    run()
