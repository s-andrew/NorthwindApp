from datetime import datetime

from sqlalchemy.orm import mapper, relationship

from meta_data import ships
from meta_data import cargos
from meta_data import ports
from meta_data import routes
from meta_data import freightage


class Ship:
    ship_id = None

    def __init__(self, name: str, reg_num: str, capasity: float, launching_date: datetime):
        self.name = name
        self.reg_num = reg_num
        self.capasity = capasity
        self.launching_date = launching_date


class Cargo:
    cargo_id = None

    def __init__(self, reg_num: str, value: float, weight: float, shelf_life: datetime):
        self.reg_num = reg_num
        self.value = value
        self.weight = weight
        self.shelf_life = shelf_life


class Port:
    port_id = None

    def __init__(self, name: str, country: str):
        self.name = name
        self.country = country


class Route:
    route_id = None

    def __init__(self, from_port: Port, to_port: Port, declaration_num: str,
                 departure_date: datetime, arrival_date: datetime):
        self.from_port = from_port
        self.to_port = to_port
        self.declaration_num = declaration_num
        self.departure_date = departure_date
        self.arrival_date = arrival_date


class Freightage:
    def __init__(self, route: Route, ship: Ship, cargo: Cargo, loading_date: datetime):
        self.route = route
        self.ship = ship
        self.cargo = cargo
        self.loading_date = loading_date


mapper(Ship, ships)
mapper(Cargo, cargos)
mapper(Port, ports)
mapper(Route, routes, properties={
    'from_port': relationship(Port, foreign_keys=[routes.c.from_port_id]),
    'to_port': relationship(Port, foreign_keys=[routes.c.to_port_id])
})
mapper(Freightage, freightage, properties={
    'route': relationship(Route, foreign_keys=[freightage.c.route_id]),
    'ship': relationship(Ship, foreign_keys=[freightage.c.ship_id]),
    'cargo': relationship(Cargo, foreign_keys=[freightage.c.cargo_id])
})
