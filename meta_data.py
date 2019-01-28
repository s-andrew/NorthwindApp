from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey


metadata = MetaData()

ships = Table('ships', metadata,
              Column('ship_id', Integer, primary_key=True),
              Column('reg_num', String(32), nullable=False),
              Column('name', String(50)),
              Column('capasity', Float),
              Column('launching_date', DateTime))

cargos = Table('cargos', metadata,
               Column('cargo_id', Integer, primary_key=True),
               Column('reg_num', String(32), nullable=False),
               Column('value', Float),
               Column('weight', Float),
               Column('shelf_life', DateTime))

ports = Table('ports', metadata,
              Column('port_id', Integer, primary_key=True),
              Column('name', String(50)),
              Column('country', String(3)))

routes = Table('routes', metadata,
               Column('route_id', Integer, primary_key=True),
               Column('from_port_id', Integer, ForeignKey('ports.port_id')),
               Column('to_port_id', Integer, ForeignKey('ports.port_id')),
               Column('declaration_num', String(32)),
               Column('departure_date', DateTime),
               Column('arrival_date', DateTime))

freightage = Table('freightage', metadata,
                   Column('route_id', Integer, ForeignKey('routes.route_id'), primary_key=True),
                   Column('ship_id', Integer, ForeignKey('ships.ship_id'), primary_key=True),
                   Column('cargo_id', Integer, ForeignKey('cargos.cargo_id'), primary_key=True),
                   Column('loading_date', DateTime))

