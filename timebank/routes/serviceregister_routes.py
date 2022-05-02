import datetime
from math import ceil
from statistics import mean

from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from timebank.models.serviceregister_model import Serviceregister
from timebank import app, db
from timebank.libs.response_helpers import record_sort_params_handler, get_all_db_objects, is_number, ValidationError, \
    user_exists, service_exists, is_rating
from timebank.models.services_model import Service


@app.route('/api/v1/serviceregister', methods=['GET'])
def api_get_all_service_register():
    sort_field, sort_dir, valid = record_sort_params_handler(request.args, Serviceregister)
    if not valid:
        return '', 400
    db_objs = get_all_db_objects(sort_field, sort_dir, db.session.query(Serviceregister)).all()

    if len(db_objs):
        response_obj = []
        for obj in db_objs:
            response_obj.append(dict(
                id=obj.id,
                Service=dict(
                    id=obj.Service.id,
                    title=obj.Service.title,
                    estimate=obj.Service.estimate,
                    avg_rating=obj.Service.avg_rating,
                ),
                User=dict(
                    id=obj.User.id,
                    phone=obj.User.phone,
                    user_name=obj.User.user_name,
                    time_account=obj.User.time_account,
                ),
                hours=obj.hours,
                service_status=obj.service_status.name,
                end_time=obj.end_time
            ))

        return jsonify(response_obj), 200
    else:
        return '', 404


@app.route('/api/v1/serviceregister/<serviceregister_id>', methods=['GET'])
def api_single_registerservice_get(serviceregister_id):
    db_query = db.session.query(Serviceregister)
    obj = db_query.get(serviceregister_id)

    if not obj:
        return '', 404

    response_obj = [dict(
        id=obj.id,
        Service=dict(
            id=obj.Service.id,
            title=obj.Service.title,
            estimate=obj.Service.estimate,
            avg_rating=obj.Service.avg_rating,
        ),
        User=dict(
            id=obj.User.id,
            phone=obj.User.phone,
            user_name=obj.User.user_name,
            time_account=obj.User.time_account,
        ),
        hours=obj.hours,
        service_status=obj.service_status.name,
        end_time=obj.end_time
    )]

    response = jsonify(response_obj)
    return response, 200


@app.route('/api/v1/serviceregister/<serviceregister_id>', methods=['PUT'])
def api_single_serviceregister_put(serviceregister_id):
    db_query = db.session.query(Serviceregister)
    db_obj = db_query.get(serviceregister_id)

    if not db_obj:
        return '', 404

    req_data = None
    if request.content_type == 'application/json':
        req_data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        req_data = request.form

    if 'service_id' in req_data:
        try:
            is_number(req_data['service_id'])
            service_exists(req_data['service_id'])
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400

        db_obj.service_id = int(req_data['service_id'])

    if 'customer_id' in req_data:
        try:
            is_number(req_data['customer_id'])
            user_exists(req_data['customer_id'])
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400

        db_obj.service_id = int(req_data['customer_id'])

    try:
        db.session.commit()
        db.session.refresh(db_obj)
    except IntegrityError as e:
        return jsonify({'error': str(e.orig)}), 405

    return '', 204


@app.route('/api/v1/serviceregister/<serviceregister_id>', methods=['DELETE'])
def api_single_registerservice_delete(serviceregister_id):
    db_query = db.session.query(Serviceregister)
    db_test = db_query.get(serviceregister_id)
    db_obj = db_query.filter_by(id=serviceregister_id)

    if not db_test:
        return '', 404

    try:
        db_obj.delete()
        db.session.commit()
    except IntegrityError as e:
        return jsonify({'error': str(e.orig)}), 405
    else:
        return '', 204


@app.route('/api/v1/serviceregister-create', methods=['POST'])
def api_single_serviceregister_create():
    db_obj = Serviceregister()

    req_data = None
    if request.content_type == 'application/json':
        req_data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        req_data = request.form

    try:
        is_number(req_data['service_id'])
        service_exists(req_data['service_id'])
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    db_obj.service_id = req_data['service_id']
    db_query2 = db.session.query(Service)
    db_obj2 = db_query2.get(db_obj.service_id)
    if db_obj2.user_id == req_data['consumer_id']:
        return jsonify({'error': 'User and consumer are the same'}), 400
    try:
        is_number(req_data['consumer_id'])
        user_exists(req_data['consumer_id'])
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    db_obj.consumer_id = req_data['consumer_id']
    db_obj.service_status = "inprogress"

    try:
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
    except IntegrityError as e:
        return jsonify({'error': str(e.orig)}), 405

    return api_single_registerservice_get(db_obj.id)


@app.route('/api/v1/serviceregister/<serviceregister_id>/<hours>/', methods=['PUT'])
@app.route('/api/v1/serviceregister/<serviceregister_id>/<hours>/<rating>', methods=['PUT'])
def api_single_serviceregister_finish_rating(serviceregister_id, hours, rating=None):
    try:
        is_number(serviceregister_id)
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    try:
        is_number(hours)
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    if rating:
        try:
            is_number(rating)
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        try:
            is_rating(rating)
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400

    db_query = db.session.query(Serviceregister)
    db_obj = db_query.get(serviceregister_id)

    if not db_obj:
        return '', 404

    # db_query2 = service related to selected serv.reg.
    db_query2 = db.session.query(Service)
    db_obj2 = db_query2.get(db_obj.service_id)
    if db_obj.service_status.name == "ended":
        return '', 400

    db_obj.service_status = "ended"
    db_obj.end_time = datetime.datetime.now()
    db_obj.hours = hours
    db_obj.rating = rating
    db_obj2.User.time_account += int(hours)

    try:
        db.session.commit()
        db.session.refresh(db_obj)
    except IntegrityError as e:
        return jsonify({'error': str(e.orig)}), 405

    db_query3 = db.session.query(Serviceregister)
    db_obj_3 = db_query3.all()
    if rating:
        lst = []
        for row in db_obj_3:
            if row.service_id == db_obj.service_id and row.rating != None:
                lst.append(row.rating)
        db_obj2.avg_rating = ceil(mean(lst))

    try:
        db.session.commit()
        db.session.refresh(db_obj)
    except IntegrityError as e:
        return jsonify({'error': str(e.orig)}), 405
    # db_obj2.avg_rating =
    return '', 200
