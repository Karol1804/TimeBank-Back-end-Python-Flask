# Import funkcii a modulov
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, \
    jwt_required, get_jwt_identity, unset_jwt_cookies
from sqlalchemy.exc import IntegrityError, NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

from timebank.models.users_model import User
from timebank import app, db
from timebank.libs.response_helpers import record_sort_params_handler, get_all_db_objects, is_number, ValidationError, \
    phone_number_match


# Funckia na vytiahnutie vsetkych pouzivatelov z databazi
@app.route('/api/v1/users', methods=['GET'])
def api_users():
    sort_field, sort_dir, valid = record_sort_params_handler(request.args, User)
    if not valid:
        return '', 400
    db_objs = get_all_db_objects(sort_field, sort_dir, db.session.query(User)).all()
    # Pokial je aspon jeden objekt v db_objs prejdeme podmienkou
    if len(db_objs):
        response_obj = []
        for obj in db_objs:
            # Do prazdneho listu response_obj pridavame vsetky dictionaries ktore mame v db_objs
            response_obj.append(dict(
                id=obj.id,
                phone=obj.phone,
                user_name=obj.user_name,
                time_account=obj.time_account,
            ))

        return jsonify(response_obj), 200
    else:
        return '{"Message": "No user to be found."}', 404


# Funkcia na vytiahnutie jedneho pouzivatela z databazky podla user_id
@app.route('/api/v1/user/<user_id>', methods=['GET'])
def api_single_user_get(user_id):

    # Vytiahnem z databazy model User
    db_query = db.session.query(User)
    # do premennej obj si ulozim konkretneho pouzivatela podla user_id
    obj = db_query.get(user_id)

    if not obj:
        return '{"Message": "No user to be found."}', 404

    response_obj = [dict(
        id=obj.id,
        phone=obj.phone,
        user_name=obj.user_name,
        time_account=obj.time_account,
    )]

    response = jsonify(response_obj)
    return response, 200


# Funkcia na updatovanie pouzivatela z databazi
@app.route('/api/v1/user/<user_id>', methods=['PUT'])
def api_single_user_put(user_id):

    db_query = db.session.query(User)
    db_obj = db_query.get(user_id)

    if not db_obj:
        return '{"message": "No user to be found."}', 404

    req_data = None
    # Skontroluje ci je telo poziadavky vo formate application/json a ak je tak z neho vytiahne data
    if request.content_type == 'application/json':
        req_data = request.json
    # Skontroluje ci je telo poziadavky vo formate application/x-www-form-urlencoded a ak je tak z neho vytiahne data
    elif request.content_type == 'application/x-www-form-urlencoded':
        req_data = request.form

    if 'phone' in req_data:
        try:
            # Kontrola telefonneho cisla ci je v spravnom tvare podla funckie phone_number_match
            phone_number_match(req_data['phone'])
            db_obj.phone = req_data['phone']
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400

    if 'user_name' in req_data:
        db_obj.user_name = req_data['user_name']

    # Podmienka ktora zahashuje heslo ktore uzivatej zada v requeste
    if 'password' in req_data:
        db_obj.password = generate_password_hash(req_data['password'])

    # Podmienka ktora skontroluje ci je v requeste cislo. Pokial nie tak vyhodi error
    if 'time_account' in req_data:
        try:
            is_number(req_data['time_account'])
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400

        db_obj.time_account = int(req_data['time_account'])

    try:
        # Potvrdi zmenu v databaze
        db.session.commit()
        db.session.refresh(db_obj)
    except IntegrityError as e:
        return jsonify({'error': str(e.orig)}), 405

    return '{"Message": "user succesfully updated."}', 204


# Funkcia na zmazanie pouzivatela z databazi
@app.route('/api/v1/user/<user_id>', methods=['DELETE'])
def api_single_user_delete(user_id):

    db_query = db.session.query(User)
    db_test = db_query.get(user_id)
    db_obj = db_query.filter_by(id=user_id)

    if not db_test:
        return '{"Message": "No user to be found."}', 404

    try:
        db_obj.delete()
        db.session.commit()
    except IntegrityError as e:
        return jsonify({'error': str(e.orig)}), 405
    else:
        return '{"Message": "User succesfully deleted."}', 204


# Funckia na vytvorenie uzivatela a pridania ho do databazi
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

    # Z tela poziadavky vytiahneme cislo a vlozime ho do databazy
    db_obj.phone = req_data['phone']
    # Z tela poziadavky vytiahneme heslo, zahashujeme ho a vlozime ho do databazy
    db_obj.password = generate_password_hash(req_data['password'])
    # Z tela poziadavky vytiahneme meno a vlozime ho do databazy
    db_obj.user_name = req_data['user_name']
    db_obj.time_account = 0
    try:
        # Pridame zmeny do databazy
        db.session.add(db_obj)
        # Ulozime zmeny v databaze
        db.session.commit()
        db.session.refresh(db_obj)

    except IntegrityError as e:
        return jsonify({'error': str(e.orig)}), 405

    return api_single_user_get(db_obj.id)


# Funckia ktora zmeni zadanemu pouzivatelovy heslo
@app.route('/api/v1/user/<user_id>/set-password', methods=['PUT'])
def api_single_user_set_password(user_id):

    db_query = db.session.query(User)
    db_obj = db_query.get(user_id)
    if not db_obj:
        return '{"Message": "No user to be found."}', 404

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

    return '{"Message": "User password succesfully changed."}', 204


# Funkcia na prihlasenie uzivatela
@app.route('/api/v1/user/login', methods=['POST'])
def api_single_user_login():
    if request.method == 'POST':
        req_data = None
        if request.content_type == 'application/json':
            req_data = request.json
        elif request.content_type == 'application/x-www-form-urlencoded':
            req_data = request.form
        # Podmienka ktora kontroluje ci mame v tele poziadavky telefonne cislo a heslo
        if not req_data['phone'] and not req_data['password']:
            return '{"Message": "Phone number and password not defined"}', 400
        phone = req_data['phone']
        password = req_data['password']

    else:
        return '{"Message": "Method not allowed."}', 400

    db_query = db.session.query(User)
    try:
        db_obj = db_query.filter_by(phone=phone).one()
    except NoResultFound:
        return '{"Message": "Phone number doesnt exist."}', 404

    if not check_password_hash(db_obj.password, password):
        return '{"Message": "Password not correct."}', 401

    identity = phone
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)

    response = jsonify({'login': True, 'phone': phone, 'id': db_obj.id, 'access_token': access_token})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response, 201


# Funkcia na odhlasenie pouzivatela
@app.route('/api/v1/user/logout', methods=['POST'])
# Metoda vyzauje JWT-token
@jwt_required(optional=True)
def api_single_user_logout():
    # get_jwt_identity je funckia ktora zo zadaneho tokenu vytiahne identitu
    identity = get_jwt_identity()
    db_query = db.session.query(User)
    try:
        db_obj = db_query.filter_by(phone=identity).one()
    except NoResultFound:
        return '{"Message": "No result found."}', 400

    response = jsonify({'logout': True, "msg": "see ya again"})
    unset_jwt_cookies(response)
    return response, 201


# Funkcia na vypisanie profilu uzivatela
@app.route('/api/v1/user/profile', methods=['GET'])
@jwt_required()
def api_single_user_profile():
    phone = get_jwt_identity()

    db_query = db.session.query(User)
    try:
        obj = db_query.filter_by(phone=phone).one()
    except NoResultFound:
        return '{"Message": "No result found."}', 404

    response_obj = [dict(
        id=obj.id,
        phone=obj.phone,
        user_name=obj.user_name,
        time_account=obj.time_account,
    )]

    response = jsonify(response_obj)
    return response, 200


# Funckia na refresnutie tokenu
@app.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    # Get_jwt_identity je funckia ktora vrati identitu JWT-tokenu. Ak nenajde ziadnu vrati None.
    current_user = get_jwt_identity()
    # Create_access_token je funkcia ktora vytvara JWT-token. V nasom pripade len aktualizuje konkretnemu pouzivatelovy jeho aktualny token. Da sa tam nastavit aj expiracia.
    access_token = create_access_token(identity=current_user)

    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200
