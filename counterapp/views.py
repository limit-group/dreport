import json
from io import BytesIO
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core import serializers
from reportlab.lib.pagesizes import A4, landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm, inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, SimpleDocTemplate, TableStyle

from .models import (
    Receipt,
    ReceiptItem,
    RequisitionAndIssue,
    RequisitionAndIssueItem,
    User,
)


def login(request):
    context = {}
    if request.method == "GET":
        return render(request, "counterapp/auth/login.html", context)

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.get_user_by_email(email)
        if not user:
            context["msg"] = "user doesn't exist"
            return render(request, "counterapp/auth/login.html", context)

        if user and check_password(password, user.password):
            request.session["user_id"] = user.id
            return redirect("dashboard/")

        else:
            context["msg"] = "wrong password provided!"
            return render(request, "counterapp/auth/login.html", context)


def add_reciept(request):
    context = {}
    if request.method == "GET":
        return render(request, "counterapp/add_receipt.html", context)

    if request.method == "POST":
        items = request.POST["items"]
        if items is None:
            context["msg"] = "Add entries to the reciepts"
            return render(request, "counterapp/add_receipt.html", context)
        try:
            receipt = Receipt.objects.create(voucher_no=request.POST["voucher_no"])
            for item in json.loads(items):
                reciept_item = ReceiptItem(
                    code_no=item["code_no"],
                    description=item["description"],
                    quantity=item["quantity"],
                    units=item["units"],
                    value=item["value"],
                    remarks=item["remarks"],
                    receipt=receipt,
                )
                reciept_item.save()
        except:
            context["msg"] = "Error saving reciept!"
            return render(request, "counterapp/add_receipt.html", context)

        receipts = ReceiptItem.objects.all()
        context["receipts"] = receipts
        return render(request, "counterapp/receipts.html", context)


def add_req_or_issue(request):
    context = {}
    if request.method == "GET":
        return render(request, "counterapp/add_req_or_issue.html", context)

    if request.method == "POST":
        items = request.POST["items"]
        if items is None:
            context["msg"] = "Add entries of requisition or issues"
            return render(request, "counterapp/add_req_or_issue.html", context)
        try:
            receipt = RequisitionAndIssue.objects.create(
                voucher_no=request.POST["voucher_no"]
            )
            for item in json.loads(items):
                req_item = RequisitionAndIssueItem(
                    code_no=item["code_no"],
                    description=item["description"],
                    units=item["units"],
                    quantity_required=item["quantity_required"],
                    quantity_issued=item["quantity_issued"],
                    value=item["value"],
                    remarks=item["remarks"],
                    receipt=receipt,
                )
                req_item.save()
        except:
            context["msg"] = "Error adding requisition or issues"
            return render(request, "counterapp/add_req_or_issue.html", context)

        req_and_issues = RequisitionAndIssueItem.get_req_and_issue_items()
        context["req_and_issues"] = req_and_issues
        return render(request, "counterapp/req_and_issues.html", context)


def reciepts(request):
    context = {}
    receipts = ReceiptItem.get_receipt_items()
    context["receipts"] = receipts

    return render(request, "counterapp/receipts.html", context)


def reciept_detail(request, voucher_no):
    context = {}
    receipts = Receipt.get_reciepts_by_voucher_no(voucher_no)
    context["receipts"] = receipts
    return render(request, "counterapp/receipts.html", context)


def req_and_issues(request):
    context = {}
    req_and_issues = RequisitionAndIssueItem.get_req_and_issue_items()
    context["req_and_issues"] = req_and_issues

    return render(request, "counterapp/req_and_issues.html", context)


def req_and_issues_detail(request, voucher_no):
    context = {}
    req_and_issues = RequisitionAndIssue.get_issues_by_voucher_no(voucher_no)
    context["req_and_issues"] = req_and_issues

    return render(request, "counterapp/req_and_issues.html", context)


def dashboard(request):
    context = {}
    issues = RequisitionAndIssueItem.get_req_and_issue_items().values()
    recs = ReceiptItem.get_receipt_items().values()
    recp_count = 0
    recp_value = 0
    for r in list(recs):
        recp_count += r["quantity"]
        recp_value += r["quantity"] * int(r["value"])

    issues_count = 0
    issue_value = 0
    for i in list(issues):
        issues_count += i["quantity_issued"]
        issue_value += i["quantity_issued"] * int(r["value"])

    context["issues_count"] = issues_count
    context["issues_value"] = issue_value
    context["rec_count"] = recp_count
    context["rec_value"] = recp_value
    return render(request, "counterapp/dashboard.html", context)


def reports(request):
    context = {}
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    context["months"] = months
    if request.method == "GET":
        reciepts = Receipt.get_reciepts()
        req_and_issues = RequisitionAndIssue.get_req_and_issues()
        context["receipts"] = reciepts
        context["req_and_issues"] = req_and_issues
        return render(request, "counterapp/reports.html", context)


def generate_pdf(request):
    res = HttpResponse(content_type="application/pdf")
    d = datetime.today().strftime("%Y-%m-%d")
    res["Content-Dispostion"] = f"inline; filename='{d}.pdf'"

    buffer = BytesIO()
    p = SimpleDocTemplate(buffer, pagesize=A4, title=f"Report on {d}")

    data = list(ReceiptItem.objects.all().values())

    # Convert JSON string to a list of dictionaries
    # data = json.loads(data)

    # Extract the values from each dictionary and append them to a list
    table_data = []
    for item in data:
        table_data.append(list(item.values()))

    # Create the table
    c_width = [0.4 * inch, 1.5 * inch, 1 * inch, 1 * inch, 1 * inch]
    t = Table(table_data, rowHeights=20, repeatRows=1, colWidths=c_width)

    # Add table styles
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 14),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
        ]
    )
    t.setStyle(table_style)

    # Add the table to the PDF
    elements = []
    elements.append(t)

    p.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    res.write(pdf)

    return res
