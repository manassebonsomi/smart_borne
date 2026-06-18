from flask import Blueprint, jsonify
from controllers.dashboard_controller import DashboardController

dashboard_routes = Blueprint("dashboard_routes", __name__)


@dashboard_routes.route("/statistics", methods=["GET"])
def statistics():

    return jsonify({

        "success": True,
        "data":
        DashboardController
        .statistics()
    }), 200