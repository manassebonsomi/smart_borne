from flask import Blueprint, jsonify
from controllers.dashboard_controller import DashboardController
from flask_jwt_extended import jwt_required

dashboard_routes = Blueprint("dashboard_routes", __name__)


@dashboard_routes.route("/dashboard/statistics", methods=["GET"])
@jwt_required()
def statistics():
    return jsonify({
        "success": True,
        "data": DashboardController.statistics()
    }), 200


@dashboard_routes.route(
    "/dashboard/recommendations",
    methods=["GET"]
)
@jwt_required()
def recommendations():
    return jsonify({
        "success": True,
        "data": DashboardController.recommendations()
    })


@dashboard_routes.route(
    "/dashboard/errors",
    methods=["GET"]
)
@jwt_required()
def errors():
    return jsonify({
        "success": True,
        "data": DashboardController.errors()
    })


@dashboard_routes.route(
    "/dashboard/audit",
    methods=["GET"]
)
@jwt_required()
def audit():
    return jsonify({

        "success": True,
        "data": DashboardController.audit_logs()
    })


@dashboard_routes.route(
    "/dashboard/campaigns",
    methods=["GET"]
)
@jwt_required()
def campaigns():
    return jsonify({
        "success": True,
        "data": DashboardController.campaigns()
    })


@dashboard_routes.route(
    "/dashboard/questions",
    methods=["GET"]
)
@jwt_required()
def questions():
    return jsonify({
        "success": True,
        "data": DashboardController.questions()
    })