from flask import Blueprint, jsonify
from controllers.dashboard_controller import DashboardController

dashboard_routes = Blueprint("dashboard_routes", __name__)


@dashboard_routes.route("/dashboard/statistics", methods=["GET"])
def statistics():
    return jsonify({
        "success": True,
        "data": DashboardController.statistics()
    }), 200


@dashboard_routes.route(
    "/dashboard/recommendations",
    methods=["GET"]
)
def recommendations():
    return jsonify({
        "success": True,
        "data": DashboardController.recommendations()
    })


@dashboard_routes.route(
    "/dashboard/errors",
    methods=["GET"]
)
def errors():
    return jsonify({
        "success": True,
        "data": DashboardController.errors()
    })


@dashboard_routes.route(
    "/dashboard/audit",
    methods=["GET"]
)
def audit():
    return jsonify({

        "success": True,
        "data": DashboardController.audit_logs()
    })


@dashboard_routes.route(
    "/dashboard/campaigns",
    methods=["GET"]
)
def campaigns():
    return jsonify({
        "success": True,
        "data": DashboardController.campaigns()
    })


@dashboard_routes.route(
    "/dashboard/questions",
    methods=["GET"]
)
def questions():
    return jsonify({
        "success": True,
        "data": DashboardController.questions()
    })