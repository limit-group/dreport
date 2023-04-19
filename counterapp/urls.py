from django.urls import path
from .views import (
    add_reciept,
    add_req_or_issue,
    reciepts,
    req_and_issues,
    dashboard,
    reports,
    generate_pdf,
    login,
    reciept_detail,
    req_and_issues_detail,
)

urlpatterns = [
    path("", dashboard, name="Dashboard"),
    path("add-reciept/", add_reciept, name="Add Reciept"),
    path("add-req-or-issue/", add_req_or_issue, name="Add Requisition/Issue"),
    path("receipts/", reciepts, name="Reciepts"),
    path("receipts/<int:voucher_no>/", reciept_detail, name="Reciept Detail"),
    path("req-and-issues/", req_and_issues, name="Requisitions And Issues"),
    path(
        "req-and-issues/<int:voucher_no>/", req_and_issues_detail, name="Issue Detail"
    ),
    path("reports/", reports, name="Reports"),
    path("generate-pdf/", generate_pdf, name="Generate PDF"),
    path("login/", login, name="Login"),
]
