import datetime
import re
from sqlalchemy import inspect, text
from timebank import db
from timebank.models.users_model import User
from timebank.models.services_model import Service
from timebank.models.models_base import ServiceregisterStatusEnum


def record_sort_params_handler(args, modeldb):
    valid = True
    if args.get('field'):
        sort_field = args.get('field')
    else:
        sort_field = 'id'

    if args.get('sort'):
        sort_dir = args.get('sort')
    else:
        sort_dir = 'asc'

    if not (sort_dir == 'asc' or sort_dir == 'desc'):
        valid = False

    if sort_field:
        col_exist = False
        for col in [column.name for column in inspect(modeldb).columns]:
            if col == sort_field:
                col_exist = True
        if not col_exist:
            valid = False

    return sort_field, sort_dir, valid


def get_all_db_objects(sort_field, sort_dir, base_query):
    sort_query = base_query.order_by(text(sort_field + ' ' + sort_dir))
    return sort_query


def format_date(date):
    if date is None:
        return date
    else:
        date = date.isoformat()
        return date


class ValidationError(Exception):
    def __init__(self, value, message):
        self.value = str(value)
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.value} -> {self.message}'


def is_number(field):
    try:
        int(field)
    except ValueError:
        raise ValidationError(field, f"Number is not valid.")


def is_rating(field):
    if -1 < int(field) < 6:
        return field
    else:
        raise ValidationError(field, f"Number is not in 5* rating from 0 to 5.")


def user_exists(field):
    if not db.session.query(User).get(field):
        raise ValidationError(field, f"User id does not exist.")


def service_exists(field):
    if not db.session.query(Service).get(field):
        raise ValidationError(field, f"Service id does not exist.")


def one_of_enum_status(field):
    db_objs = ServiceregisterStatusEnum
    exist = False
    for db_obj in db_objs:
        if db_obj.name == field:
            exist = True

    if not exist:
        raise ValidationError(field, f"Status is not valid.")


def is_date(field, date_format='%Y-%m-%d'):
    if field:
        try:
            date = datetime.datetime.strptime(str(field), date_format).date()
        except ValueError:
            raise ValidationError(field, f"Incorrect data format, should be {date_format}")


def phone_number_match(number):
    if not re.match(r"\A[+]\d{3} \d{3} \d{6}\Z", number):
        raise ValidationError(number, f"Incorrect number format")
