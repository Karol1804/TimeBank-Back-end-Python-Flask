from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, \
    jwt_required, get_jwt_identity, unset_jwt_cookies
from sqlalchemy.exc import IntegrityError, NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

from timebank.models.users_model import User
from timebank import app, db
from timebank.libs.response_helpers import record_sort_params_handler, get_all_db_objects, is_number, ValidationError, \
    phone_number_match


@app.route('/api/v1/users', methods=['GET'])
def api_users():
    sort_field, sort_dir, valid = record_sort_params_handler(request.args, User)
    if not valid:
        return '', 400
    db_objs = get_all_db_objects(sort_field, sort_dir, db.session.query(User)).all()

    if len(db_objs):
        response_obj = []
        for obj in db_objs:
            response_obj.append(dict(
                id=obj.id,
                phone=obj.phone,
                user_name=obj.user_name,
                time_account=obj.time_account,
            ))

        return jsonify(response_obj), 200
    else:
        return '', 404


@app.route('/api/v1/user/<user_id>', methods=['GET'])
def api_single_user_get(user_id):

    db_query = db.session.query(User)
    obj = db_query.get(user_id)

    if not obj:
        return '', 404

    response_obj = [dict(
        id=obj.id,
        phone=obj.phone,
        user_name=obj.user_name,
        time_account=obj.time_account,
    )]

    response = jsonify(response_obj)
    return response, 200


@app.route('/api/v1/user/<user_id>', methods=['PUT'])
def api_single_user_put(user_id):

    db_query = db.session.query(User)
    db_obj = db_query.get(user_id)

    if not db_obj:
        return '', 404

    req_data = None
    if request.content_type == 'application/json':
        req_data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        req_data = request.form

    if 'phone' in req_data:
        try:
            phone_number_match(req_data['phone'])
            db_obj.phone = req_data['phone']
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400

    if 'user_name' in req_data:
        db_obj.user_name = req_data['user_name']

    if 'password' in req_data:
        db_obj.password = generate_password_hash(req_data['password'])

    if 'time_account' in req_data:
        try:
            is_number(req_data['time_account'])
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400

        db_obj.time_account = int(req_data['time_account'])

    try:
        db.session.commit()
        db.session.refresh(db_obj)
    except IntegrityError as e:
        return jsonify({'error': str(e.orig)}), 405

    return '', 204


@app.route('/api/v1/user/<user_id>', methods=['DELETE'])
def api_single_user_delete(user_id):

    db_query = db.session.query(User)
    db_test = db_query.get(user_id)
    db_obj = db_query.filter_by(id=user_id)

    if not db_test:
        return '', 404

    try:
        db_obj.delete()
        db.session.commit()
    except IntegrityError as e:
        return jsonify({'error': str(e.orig)}), 405
    else:
        return '', 204


@app.route('/api/v1/user-create', methods=['POST'])
def api_single_user_create():
    db_obj = User()

    req_data = None
    if request.content_type == 'application/json':
        req_data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        req_data = request.form
    try:
        phone_number_match(req_data['phone'])
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    db_obj.phone = req_data['phone']
    db_obj.password = generate_password_hash(req_data['password'])
    db_obj.user_name = req_data['user_name']
    db_obj.time_account = 0
    try:
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)

        print(db_obj.id)
    except IntegrityError as e:
        return jsonify({'error': str(e.orig)}), 405

    return api_single_user_get(db_obj.id)


@app.route('/api/v1/user/<user_id>/set-password', methods=['PUT'])
def api_single_user_set_password(user_id):

    db_query = db.session.query(User)
    db_obj = db_query.get(user_id)
    if not db_obj:
        return '', 404

    req_data = None
    if request.content_type == 'application/json':
        req_data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        req_data = request.form

    db_obj.password = generate_password_hash(req_data['password'])
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify({'error': str(e.orig)}), 405

    return '', 204


@app.route('/api/v1/user/login', methods=['POST'])
def api_single_user_login():
    if request.method == 'POST':
        req_data = None
        if request.content_type == 'application/json':
            req_data = request.json
        elif request.content_type == 'application/x-www-form-urlencoded':
            req_data = request.form
        if not req_data['phone'] and not req_data['password']:
            return '', 400
        phone = req_data['phone']
        password = req_data['password']

    else:
        return '', 400

    db_query = db.session.query(User)
    try:
        db_obj = db_query.filter_by(phone=phone).one()
    except NoResultFound:
        return '', 404

    if not check_password_hash(db_obj.password, password):
        return '', 401

    identity = phone
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)

    response = jsonify({'login': True, 'phone': phone, 'id': db_obj.id, 'access_token': access_token})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response, 201


@app.route('/api/v1/user/logout', methods=['POST'])
@jwt_required(optional=True)
def api_single_user_logout():
    identity = get_jwt_identity()
    db_query = db.session.query(User)
    try:
        db_obj = db_query.filter_by(phone=identity).one()
    except NoResultFound:
        return '', 400

    response = jsonify({'logout': True, "msg": "see ya again"})
    unset_jwt_cookies(response)
    return response, 201


@app.route('/api/v1/user/profile', methods=['GET'])
@jwt_required()
def api_single_user_profile():
    phone = get_jwt_identity()

    db_query = db.session.query(User)
    try:
        obj = db_query.filter_by(phone=phone).one()
    except NoResultFound:
        return '', 404

    response_obj = [dict(
        id=obj.id,
        phone=obj.phone,
        user_name=obj.user_name,
        time_account=obj.time_account,
    )]

    response = jsonify(response_obj)
    return response, 200


@app.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200
