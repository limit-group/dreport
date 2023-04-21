from django.urls import path
from .views import (
    add_reciept,
    add_issue,
    add_requisition,
    reciepts,
    requisitions,
    dashboard,
    reports,
    generate_pdf,
    login,
    reciept_detail,
    requisition_detail,
    add_user,
    users,
    issues,
    issue_detail,
    add_item,
    items
)

urlpatterns = [
    path("", dashboard, name="Dashboard"),
    path("add-reciept/", add_reciept, name="Add Reciept"),
    path("add-requistion/", add_requisition, name="Add Requisition"),
    path("add-issue/", add_issue, name="Add Issue"),
    path("add-item/", add_item, name="Add Item"),
    path("items/", items, name="Items"),
    path("issues/", issues, name="Issues"),
    path("issues/<int:voucher_no>/", issue_detail, name="Issue Detail"),
    path("receipts/", reciepts, name="Reciepts"),
    path("receipts/<int:voucher_no>/", reciept_detail, name="Reciept Detail"),
    path("requisitions/", requisitions, name="Requisitions"),
    path("requisitions/<int:voucher_no>/", requisition_detail, name="Issue Detail"),
    path("reports/", reports, name="Reports"),
    path("generate-pdf/", generate_pdf, name="Generate PDF"),
    path("login/", login, name="Login"),
    path("users/", users, name="Users"),
    path("users/add-user/", add_user, name="Add User"),
]
