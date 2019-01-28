from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Length


class ShipForm(FlaskForm):
    pass


class PortForm(FlaskForm):
    pass


class CargoForm(FlaskForm):
    reg_num = StringField('Registration Number', validators=[DataRequired(), Length(max=32)])
    value = StringField('Value')
    weight = StringField('Weight')
    shelf_life = DateTimeField('Shelf Life')
    submit = SubmitField('Add')


class RouteForm(FlaskForm):
    from_port = SelectField('From', coerce=int, choices=None, validators=[DataRequired()])
    to_port = SelectField('To', coerce=int, choices=None, validators=[DataRequired()])
    declaration_num = StringField('Declaration Number', validators=[DataRequired(), Length(max=32)])
    departure_date = DateTimeField('Departure')
    arrival_date = DateTimeField('Arrival')
    submit = SubmitField('Add')

    def __init__(self, *args, **kwargs):
        ports = kwargs.pop('ports', None)
        super(RouteForm, self).__init__(*args, **kwargs)
        if ports is not None:
            self.from_port.choices = [(port.port_id, port.name) for port in ports]
            self.to_port.choices = [(port.port_id, port.name) for port in ports]


class FreightageForm(FlaskForm):
    route = SelectField('Route', coerce=int, choices=None, validators=[DataRequired()])
    ship = SelectField('Ship', coerce=int, choices=None, validators=[DataRequired()])
    cargo = SelectField('Cargo', coerce=int, choices=None, validators=[DataRequired()])
    loading_date = DateTimeField('Loading Date')
    submit = SubmitField('Add')

    def __init__(self, *args, **kwargs):
        routes = kwargs.pop('routes', None)
        ships = kwargs.pop('ships', None)
        cargos = kwargs.pop('cargos', None)
        super(FreightageForm, self).__init__(*args, **kwargs)

        if routes is not None:
            self.route.choices = [(route.route_id, route.declaration_num) for route in routes]
        if ships is not None:
            self.ship.choices = [(ship.ship_id, ship.name) for ship in ships]
        if cargos is not None:
            self.cargo.choices = [(cargo.cargo_id, cargo.reg_num) for cargo in cargos]
