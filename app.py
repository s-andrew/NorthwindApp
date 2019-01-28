from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import raiseload

from config import Config
from meta_data import metadata

from entities import Ship
from entities import Cargo
from entities import Port
from entities import Route
from entities import Freightage

from forms import ShipForm
from forms import PortForm
from forms import CargoForm
from forms import RouteForm
from forms import FreightageForm


def application_factory():
    app = Flask(__name__)
    app.config.from_object(Config)

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    metadata.create_all(engine)
    Session = scoped_session(sessionmaker(bind=engine))

    @app.route('/')
    def home_page():
        return render_template('home.html')

    @app.route('/ships', methods=['GET', 'POST'])
    def get_all_ships():
        session = Session()
        ships = session.query(Ship).all()
        return render_template('ships.html', ships=ships)

    @app.route('/ships/<int:ship_id>')
    def get_one_ship(ship_id):
        session = Session()
        ship = session.query(Ship).filter(Ship.ship_id == ship_id).first()
        freightages = session.query(Freightage).filter(Freightage.ship == ship).all()
        return render_template('ship.html', ship=ship, freightages=freightages)

    @app.route('/ports', methods=['GET', 'POST'])
    def get_all_ports():
        session = Session()
        ports = session.query(Port).all()
        return render_template('ports.html', ports=ports)

    @app.route('/ports/<int:port_id>')
    def get_one_port(port_id):
        session = Session()
        port = session.query(Port).filter(Port.port_id == port_id).first()
        routes = session.query(Route).all()
        return render_template('port.html', port=port, routes=routes)

    @app.route('/cargos', methods=['GET', 'POST'])
    def get_all_cargos():
        session = Session()
        form = CargoForm()
        if form.validate_on_submit():
            new_cargo = Cargo(
                form.reg_num.data,
                form.value.data,
                form.weight.data,
                form.shelf_life.data
            )
            session.add(new_cargo)
            session.commit()
            return redirect(url_for('get_all_cargos'))
        cargos = session.query(Cargo).all()
        session.close()
        return render_template('cargos.html', cargos=cargos, form=form)

    @app.route('/cargos/<int:cargo_id>')
    def get_one_cargo(cargo_id):
        session = Session()
        cargo = session.query(Cargo).filter(Cargo.cargo_id == cargo_id).first()
        freightages = session.query(Freightage).filter(Freightage.cargo == cargo).all()
        return render_template('cargo.html', cargo=cargo, freightages=freightages)


    @app.route('/routes', methods=['GET', 'POST'])
    def get_all_routes():
        session = Session()
        ports = session.query(Port).all()
        form = RouteForm(ports=ports)
        if form.validate_on_submit():
            from_port = session.query(Port).filter(Port.port_id == form.from_port.data).first()
            to_port = session.query(Port).filter(Port.port_id == form.to_port.data).first()
            new_route = Route(
                from_port,
                to_port,
                form.declaration_num.data,
                form.departure_date.data,
                form.arrival_date.data
            )
            session.add(new_route)
            session.commit()
            return redirect(url_for('get_all_routes'))
        routes = session.query(Route).all()
        return render_template('routes.html', routes=routes, form=form)

    @app.route('/route/<int:route_id>')
    def get_one_route(route_id):
        session = Session()
        route = session.query(Route).filter(Route.route_id == route_id).first()
        return render_template('route.html', route=route)

    @app.route('/freightage', methods=['GET', 'POST'])
    def get_all_freightage():
        session = Session()
        ships = session.query(Ship).all()
        cargos = session.query(Cargo).all()
        routes = session.query(Route).all()

        form = FreightageForm(ships=ships, cargos=cargos, routes=routes)
        if form.validate_on_submit():
            ship = session.query(Ship).filter(Ship.ship_id == form.ship.data).first()
            cargo = session.query(Cargo).filter(Cargo.cargo_id == form.cargo.data).first()
            route = session.query(Route).filter(Route.route_id == form.route.data).first()

            new_freightage = Freightage(
                route,
                ship,
                cargo,
                form.loading_date.data
            )
            session.add(new_freightage)
            session.commit()

            return redirect(url_for('get_all_freightage'))

        freightages = session.query(Freightage).all()
        return render_template('freightage.html', freightages=freightages, form=form)

    return app


if __name__ == '__main__':
    application = application_factory()
    application.run(host='localhost', port=5000, debug=True)




