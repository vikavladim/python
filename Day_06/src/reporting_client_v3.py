import argparse
import json
import logging
from operator import or_

import grpc
from select import select

from ship_pb2 import *
import ship_pb2_grpc
from google.protobuf import json_format
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from typing import List
from models import *


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
        if self.alignment == Alignment.Ally and self.name == 'Unknown':
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
    parser = argparse.ArgumentParser(description='Reporting Client')
    subparsers = parser.add_subparsers(dest='command')

    scan_parser = subparsers.add_parser('scan', help='Scan')
    scan_parser.add_argument('right_ascention_hours', type=float, help='Right ascention hours')
    scan_parser.add_argument('right_ascention_minutes', type=float, help='Right ascention minutes')
    scan_parser.add_argument('right_ascention_seconds', type=float, help='Right ascention seconds')
    scan_parser.add_argument('declination_degrees', type=float, help='Declination degrees')
    scan_parser.add_argument('declination_minutes', type=float, help='Declination minutes')
    scan_parser.add_argument('declination_seconds', type=float, help='Declination seconds')

    list_traitors_parser = subparsers.add_parser('list_traitors', help='Вывести список предателей')
    return parser.parse_args()


def clear_db():
    session.query(ship_officers).delete()
    session.query(Spaceship).delete()
    session.query(Officer).delete()
    session.commit()

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance is None:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
    return instance


def scan(args):
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
        for ship in response.responses:
            try:
                spaceship = SpaceshipPydantic(**json.loads(json_format.MessageToJson(
                    ship,
                    preserving_proto_field_name=True,
                    always_print_fields_with_no_presence=True)))

                spaceship_sql = Spaceship(**spaceship.dict(exclude={'officers'}))
                session.add(spaceship_sql)

                for officer in spaceship.officers:
                    officer_sql = get_or_create(session, Officer, first_name=officer.first_name,
                                                last_name=officer.last_name, rank=officer.rank)
                    spaceship_sql.officers.append(officer_sql)

                session.commit()

            except ValueError as e:
                print(f'Корабль не прошёл проверку: {e}')


def list_traitors():
    q1=(session.query(Officer.first_name, Officer.last_name, Officer.rank)
                .join(ship_officers)
                .join(Spaceship)
                .filter(Spaceship.alignment == Alignment.Enemy))

    q2=(session.query(Officer.first_name, Officer.last_name, Officer.rank)
                .join(ship_officers)
                .join(Spaceship)
                .filter(Spaceship.alignment == Alignment.Ally))

    traitors = q1.intersect(q2)

    for traitor in traitors:
        print(json.dumps({
            "first_name": traitor.first_name,
            "last_name": traitor.last_name,
            "rank": traitor.rank
        }))


def run():
    args = parse_args()

    if args.command == 'scan':
        scan(args)
    elif args.command == 'list_traitors':
        list_traitors()


if __name__ == "__main__":
    # clear_db()
    logging.basicConfig()
    run()
