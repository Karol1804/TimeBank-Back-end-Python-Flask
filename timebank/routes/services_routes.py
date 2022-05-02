from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from timebank.models.services_model import Service
from timebank.models.users_model import User
from timebank import app, db
from timebank.libs.response_helpers import record_sort_params_handler, get_all_db_objects, is_number, ValidationError, \
    user_exists, is_estimate


@app.route('/api/v1/services', methods=['GET'])
def api_services():
    sort_field, sort_dir, valid = record_sort_params_handler(request.args, Service)
    if not valid:
        return {'Bad Request': 'services not found'}, 400

    db_objs = get_all_db_objects(sort_field, sort_dir, db.session.query(Service)).all()
    if len(db_objs):
        response_obj = []
        for obj in db_objs:
            response_obj.append(dict(
                id=obj.id,
                title=obj.title,
                User=dict(
                    id=obj.User.id,
                    phone=obj.User.phone,
                    user_name=obj.User.user_name,
                    time_account=obj.User.time_account,
                ),
                avg_rating=obj.avg_rating,
                estimate=obj.estimate,
            ))
        return jsonify(response_obj), 200
    else:
        return '', 404


@app.route('/api/v1/service/<services_id>', methods=['GET'])
def api_single_service_get(services_id):
    db_query = db.session.query(Service)
    obj = db_query.get(services_id)

    if not obj:
        return {'Bad Request': f'Service {services_id} not found'}, 400

    response_obj = [dict(
        id=obj.id,
        title=obj.title,
        User=dict(
            id=obj.User.id,
            phone=obj.User.phone,
            user_name=obj.User.user_name,
            time_account=obj.User.time_account,
        ),
        avg_rating=obj.avg_rating,
        estimate=obj.estimate,
    )]

    response = jsonify(response_obj)
    return response, 200


@app.route('/api/v1/service/<services_id>', methods=['PUT'])
def api_single_service_put(services_id):

    db_query = db.session.query(Service)
    db_obj = db_query.get(services_id)

    if not db_obj:
        return {'Bad Request': f'Service {services_id} not found'}, 400

    req_data = None
    if request.content_type == 'application/json':
        req_data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        req_data = request.form

    if 'user_id' in req_data:
        try:
            is_number(req_data['user_id'])
            user_exists(req_data['user_id'])
        except ValidationError:
            return '', 400

        db_obj.user_id = int(req_data['user_id'])

    if 'title' in req_data:
        db_obj.title = req_data['title']

    if 'estimate' in req_data:
        try:
            is_number(req_data['estimate'])
            is_estimate(req_data['estimate'])
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400

        db_obj.estimate = req_data['estimate']

    try:
        db.session.commit()
        db.session.refresh(db_obj)
    except IntegrityError as e:
        return jsonify({'error': str(e.orig)}), 405

    return '', 204


@app.route('/api/v1/service/<services_id>', methods=['DELETE'])
def api_single_service_delete(services_id):

    db_query = db.session.query(Service)
    db_test = db_query.get(services_id)
    db_obj = db_query.filter_by(id=services_id)

    if not db_test:
        return {'Bad Request': f'Service {services_id} not found'}, 400

    try:
        db_obj.delete()
        db.session.commit()
    except IntegrityError as e:
        return jsonify({'error': str(e.orig)}), 405
    else:
        return '', 204


@app.route('/api/v1/service-create', methods=['POST'])
def api_single_service_create():
    db_obj = Service()

    req_data = None
    if request.content_type == 'application/json':
        req_data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        req_data = request.form

    try:
        is_number(req_data['user_id'])
        user_exists(req_data['user_id'])
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

    try:
        is_number(req_data['estimate'])
        is_estimate(req_data['estimate'])
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

    db_obj.user_id = int(req_data['user_id'])
    db_obj.title = req_data['title']
    db_obj.estimate = int(req_data['estimate'])

    try:
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
    except IntegrityError as e:
        return jsonify({'error': str(e.orig)}), 405

    return api_single_service_get(db_obj.id)


# metoda pro autocomplete - /api/v1/service-search?ord=asc&field=title&s=tit
@app.route('/api/v1/service-search', methods=['GET'])
def api_service_search():
    field, sort_dir, valid = record_sort_params_handler(request.args, Service)
    if not valid:
        return '', 400

    if request.args.get('s'):
        search_string = request.args.get('s')
    else:
        return '', 400

    response_obj = []
    if len(search_string) > 1:
        db_query = db.session.query(Service)
        db_filter = db_query.filter(Service.title.like('%' + search_string + '%'))

        if field and sort_dir:
            db_objs = db_filter.order_by(text(field + ' ' + sort_dir)).all()
        else:
            db_objs = db.filter.all()

        if len(db_objs):

            for obj in db_objs:
                response_obj.append(dict(
                    id=obj.id,
                    title=obj.title,
                    user_id=obj.user_id,
                    estimate=obj.estimate,
                    avg_rating=obj.avg_rating
                ))

    return jsonify(response_obj), 200


# Vytvor zoznam sluzieb ktory odfiltruje zoznam sluzieb podla konkretneho poskytovatela:
@app.route('/api/v1/services-user/<user_id>', methods=['GET'])
def api_service_user_id(user_id):
    sort_field, sort_dir, valid = record_sort_params_handler(request.args, Service)

    if not valid:
        return '', 400

    db_objs = get_all_db_objects(sort_field, sort_dir, db.session.query(Service)).all()

    db_query = db.session.query(User)
    obj = db_query.get(user_id)

    if not obj:
        return '{"Message": "No user with that ID!"}', 404

    if len(db_objs):
        response_obj = []
        for service in db_objs:
            if service.user_id == obj.id:
                response_obj.append(dict(
                    title=service.title,
                    phone=obj.phone,
                    user_name=obj.user_name,
                    estimate=service.estimate,
                    rating=service.avg_rating,
                    user_id=obj.id
            ))
        return jsonify(response_obj), 200
    else:
        return '', 404