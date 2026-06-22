from flask import Blueprint
from flask import jsonify
from controllers.report_controller import ReportController

report_bp = Blueprint("report",__name__)


@report_bp.route("/reports/pdf", methods=["GET"])
def export_pdf():
    return jsonify(ReportController.export_pdf())


@report_bp.route("/reports/excel", methods=["GET"])
def export_excel():
    return jsonify(ReportController.export_excel())