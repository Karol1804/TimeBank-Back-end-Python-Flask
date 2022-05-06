import datetime
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from timebank.models.serviceregister_model import Serviceregister
from timebank import app, db
from timebank.libs.response_helpers import record_sort_params_handler, get_all_db_objects, is_number, ValidationError, \
    user_exists, service_exists, is_rating
from timebank.models.services_model import Service
from timebank.models.users_model import User


@app.route('/api/v1/serviceregister', methods=['GET'])
def api_get_all_service_register():
    sort_field, sort_dir, valid = record_sort_params_handler(request.args, Serviceregister)
    app.logger.error(f"{request.remote_addr}, Request in get all Serviceregister failed, "
                     f"check your request and try again")
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
                end_time=obj.end_time,
                rating=obj.rating
            ))
        app.logger.info(f"{request.remote_addr}, All serviceregister have been loaded successfully.")
        return jsonify(response_obj), 200
    else:
        app.logger.warning(f"{request.remote_addr}, No serviceregister has been found.")
        return '', 404


@app.route('/api/v1/serviceregister/<serviceregister_id>', methods=['GET'])
def api_single_registerservice_get(serviceregister_id):
    db_query = db.session.query(Serviceregister)
    obj = db_query.get(serviceregister_id)

    if not obj:
        app.logger.warning(f"{request.remote_addr}, Selected serviceregister: {serviceregister_id} doesn't exist.")
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
        end_time=obj.end_time,
        rating=obj.rating
    )]

    response = jsonify(response_obj)
    app.logger.info(f"{request.remote_addr}, Selected serviceregister:"
                    f" {serviceregister_id} has been loaded successfully.")
    return response, 200


@app.route('/api/v1/serviceregister/<serviceregister_id>', methods=['PUT'])
@jwt_required(optional=True)
def api_single_serviceregister_put(serviceregister_id):
    if get_jwt_identity() is None:
        return '', 401
    db_query = db.session.query(Serviceregister)
    db_obj = db_query.get(serviceregister_id)

    if not db_obj:
        app.logger.warning(f"{request.remote_addr}, Selected serviceregister: "
                           f"{serviceregister_id} does not exist.")
        return '', 404
    old_obj = [db_obj.service_id, db_obj.consumer_id, db_obj.hours,
               db_obj.service_status.name, db_obj.end_time, db_obj.rating]
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
            app.logger.error(f"{request.remote_addr}, Validation error: "
                             f"Updating serviceregister failed, service id is not a number.")
            return jsonify({'error': str(e)}), 400

        db_obj.service_id = int(req_data['service_id'])

    if 'customer_id' in req_data:
        try:
            is_number(req_data['customer_id'])
            user_exists(req_data['customer_id'])
        except ValidationError as e:
            app.logger.error(f"{request.remote_addr}, Validation error: "
                             f"Updating serviceregister failed, customer id is not a number.")
            return jsonify({'error': str(e)}), 400

        db_obj.service_id = int(req_data['customer_id'])

    try:
        db.session.commit()
        db.session.refresh(db_obj)
    except IntegrityError as e:
        app.logger.error(f"{request.remote_addr}, Integrity error: There has been problem "
                         f"with updating serviceregister in the database. Recheck your request and try again.")
        return jsonify({'error': str(e.orig)}), 405
    app.logger.info(f"{request.remote_addr}, User: {serviceregister_id} "
                    f"has been updated by requestor: {get_jwt_identity()}\n"
                    f"  Service ID has been changed from {old_obj[0]} to {db_obj.service_id},\n"
                    f"  Customer ID has been changed from {old_obj[1]} to {db_obj.consumer_id},\n"
                    f"  Hours has been changed from {old_obj[2]} to {db_obj.hours},\n"
                    f"  Service status has been changed from \"{old_obj[3]}\" to \"{db_obj.service_status.name}\",\n"
                    f"  End time has been changed from {old_obj[4]} to {db_obj.end_time},\n"
                    f"  Rating has been changed from {old_obj[5]} to {db_obj.rating}.")
    return '', 204


@app.route('/api/v1/serviceregister/<serviceregister_id>', methods=['DELETE'])
@jwt_required(optional=True)
def api_single_registerservice_delete(serviceregister_id):
    if get_jwt_identity() is None:
        return '', 401
    db_query = db.session.query(Serviceregister)
    db_test = db_query.get(serviceregister_id)
    db_obj = db_query.filter_by(id=serviceregister_id)

    if not db_test:
        app.logger.warning(f"{request.remote_addr}, Selected serviceregister: {serviceregister_id} does not exist.")
        return {'Bad Request': f'Service {serviceregister_id} not found'}, 400

    try:
        db_obj.delete()
        db.session.commit()
    except IntegrityError as e:
        app.logger.error(f"{request.remote_addr}, Integrity error: "
                         f"There has been problem with deleting serviceregister from the database. "
                         f"Recheck your request and try again.")
        return jsonify({'error': str(e.orig)}), 405
    else:
        app.logger.info(f"{request.remote_addr}, Selected serviceregister: {serviceregister_id} "
                        f"has been deleted successfully by requestor: {get_jwt_identity()}.")
        return jsonify({'Message': 'Serviceregister has been successfully deleted'}), 204


@app.route('/api/v1/serviceregister-create', methods=['POST'])
@jwt_required(optional=True)
def api_single_serviceregister_create():
    if get_jwt_identity() is None:
        return '', 401
    db_obj = Serviceregister()

    req_data = None
    if request.content_type == 'application/json':
        req_data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        req_data = request.form

    db_query2 = db.session.query(User)
    obj2 = db_query2.filter_by(phone=get_jwt_identity()).one()

    try:
        is_number(req_data['service_id'])
        service_exists(req_data['service_id'])
    except ValidationError as e:
        app.logger.error(f"{request.remote_addr}, Validation error: "
                         f"Creating serviceregister failed, check service id in your request and try again.")
        return jsonify({'error': str(e)}), 400
    db_obj.service_id = req_data['service_id']
    db_query3 = db.session.query(Service)
    db_obj2 = db_query3.get(db_obj.service_id)
    if db_obj2.user_id == obj2.id:
        app.logger.warning(f"{request.remote_addr}, Can't create a service register with same service id and user id")
        return jsonify({'error': 'User and consumer are the same'}), 400

    db_obj.consumer_id = obj2.id
    db_obj.service_status = "inprogress"

    try:
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
    except IntegrityError as e:
        app.logger.error(f"{request.remote_addr}, Integrity error: "
                         f"There has been problem with creating new serviceregister into database. "
                         f"Recheck your request and try again.")
        return jsonify({'error': str(e.orig)}), 405
    app.logger.info(f"{request.remote_addr}, Service has been created successfully, "
                    f"New service has following parameters:\n"
                    f"  Id: {db_obj.id},\n"
                    f"  Service ID: {db_obj.service_id},\n"
                    f"  Consumer ID: {db_obj.consumer_id},\n"
                    f"  Hours: {db_obj.hours},\n"
                    f"  Service status: {db_obj.service_status.name}.")
    return api_single_registerservice_get(db_obj.id)


@app.route('/api/v1/serviceregister/<serviceregister_id>/<hours>/', methods=['PUT'])
@app.route('/api/v1/serviceregister/<serviceregister_id>/<hours>/<rating>', methods=['PUT'])
@jwt_required(optional=True)
def api_single_serviceregister_finish_rating(serviceregister_id, hours, rating=None):
    if get_jwt_identity() is None:
        return '', 401
    try:
        is_number(serviceregister_id)
    except ValidationError as e:
        app.logger.warning(f"{request.remote_addr}, Finishing of serviceregister failed, "
                           f"check serviceregister number and try again.")
        return jsonify({'error': str(e)}), 400
    try:
        is_number(hours)
    except ValidationError as e:
        app.logger.warning(f"{request.remote_addr}, Finishing of serviceregister failed, "
                           f"check hours number and try again.")
        return jsonify({'error': str(e)}), 400
    if rating:
        try:
            is_number(rating)
        except ValidationError as e:
            app.logger.warning(f"{request.remote_addr}, Finishing of serviceregister failed, "
                               f"check rating number and if it is in range and try again.")
            return jsonify({'error': str(e)}), 400
        try:
            is_rating(rating)
        except ValidationError as e:
            app.logger.warning(f"{request.remote_addr}, Finishing of serviceregister failed, "
                               f"check rating number and if it is in range and try again.")
            return jsonify({'error': str(e)}), 400

    db_query = db.session.query(Serviceregister)
    db_obj = db_query.get(serviceregister_id)

    if not db_obj:
        app.logger.warning(f"{request.remote_addr}, Serviceregister in finishing does not exist.")
        return jsonify({'error': "Serviceregister doesn\'t exist"}), 404

    # db_query2 = service related to selected serv.reg.
    db_query2 = db.session.query(Service)
    db_obj2 = db_query2.get(db_obj.service_id)
    if db_obj.service_status.name == "ended":
        app.logger.warning(f"{request.remote_addr}, Can not finish serviceregister, "
                           f"serviceregister has been already finished.")
        return jsonify({'error': "Serviceregister has been already finished"}), 400

    db_obj.service_status = "ended"
    db_obj.end_time = datetime.datetime.now()
    db_obj.hours = hours
    db_obj.rating = rating
    db_obj2.User.time_account += int(hours)
    db_obj2.avg_rating = db.session.query(func.avg(
        Serviceregister.rating)).filter(Serviceregister.service_id == db_obj.service_id,
                                        Serviceregister.rating is not None).scalar_subquery()

    try:
        db.session.commit()
        db.session.refresh(db_obj)
    except IntegrityError as e:
        app.logger.error(f"{request.remote_addr}, Integrity error: "
                         f"There has been problem with finishing serviceregister in database. "
                         f"Recheck your request and try again.")
        return jsonify({'error': str(e.orig)}), 405
    app.logger.info(f"{request.remote_addr}, Finishing serviceregister: {serviceregister_id} has been completed "
                    f"successfully by requestor: {get_jwt_identity()}.")
    return jsonify({'Message': 'Serviceregister successfully finished'}), 200
