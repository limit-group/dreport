import json
import re
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
    Requisition,
    RequisitionItem,
    User,
    ReceiptItem,
    Issue,
    IssueItem,
    Item,
)


def dashboard(request):
    context = {}
    issue_count = Issue.objects.count()
    receipt_count = Receipt.objects.count()
    requisition_count = Requisition.objects.count()
    item_count = Item.objects.count()
    user_count = User.objects.count()

    context["issue_count"] = issue_count
    context["receipt_count"] = receipt_count
    context["requisition_count"] = requisition_count
    context["item_count"] = item_count
    context["user_count"] = user_count
    return render(request, "counterapp/dashboard.html", context)


def items(request):
    context = {}
    if request.method == "GET":
        items = Item.get_all_items()
        context["items"] = items
        return render(request, "counterapp/items.html", context)


def add_item(request):
    context = {}
    if request.method == "GET":
        return render(request, "counterapp/add_item.html", context)

    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        try:
            Item.create_item(name)
        except:
            context["msg"] = "failed to create an item"
            return render(request, "counterapp/add_item.html", context)

        items = Item.get_all_items()
        context["items"] = items
        return render(request, "counterapp/items.html", context)


def item_detail(request, item_id):
    context = {}

    try:
        item = Item.get_item_by_id(item_id)
    except Item.DoesNotExist:
        context["msg"] = "Item not found!"
        return render(request, "counterapp/items.html", context)

    if request.method == "GET":
        context["item"] = item
        return render(request, "counterapp/edit_item.html", context)

    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        count = request.POST["count"]
        try:
            Item.update_item(item, name, description, count)
        except:
            context["msg"] = "Error updating item!"
            return render(request, "counterapp/items.html", context)

        return render(request, "counterapp/items.html", context)


def delete_item(request, item_id):
    context = {}
    if request.method == "POST":
        try:
            Item.delete_item(item_id)
        except:
            context["msg"] = "failed to delete item"
            return render(request, "counterapp/items.html", context)

        Item.get_all_items()
        context["items"] = items
        return render(request, "counterapp/items.html", context)


def users(request):
    context = {}
    if request.session["user_role"] != "Admin" and not None:
        return render(request, "counterapp/dashboard.html", context)

    if request.method == "GET":
        users = User.get_all_users()
        context["users"] = users
        return render(request, "counterapp/auth/users.html", context)


def add_user(request):
    context = {}
    if request.session["user_role"] != "Admin" and request.session is not None:
        return render(request, "counterapp/dashboard.html", context)

    if request.method == "GET":
        return render(request, "counterapp/auth/signup.html", context)

    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]
        role = request.POST["role"]
        # role = "Admin"

        if password != confirm_password:
            context["msg"] = "Passwords must match."
            return render(request, "counterapp/auth/signup.html", context)

        user = User.get_user_by_email(email)
        if user:
            context["msg"] = "This user is already registered"
            return render(request, "counterapp/auth/signup.html", context)
        try:
            User.create_user(email, username, role, password)
        except:
            context["msg"] = "Error creating a new user"
            return render(request, "counterapp/auth/signup.html", context)

        context["users"] = User.get_all_users()
        return render(request, "counterapp/auth/users.html", context)


def user_detail(request, user_id):
    context = {}
    if request.session["user_role"] != "Admin" and not None:
        return render(request, "counterapp/dashboard.html", context)

    try:
        user = User.get_user_by_id(user_id)
    except User.DoesNotExist:
        context["msg"] = "Error getting  user"
        return render(request, "counterapp/auth/users.html", context)

    if request.method == "GET":
        context["user"] = user
        return render(request, "counterapp/auth/edit_user.html", context)

    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]
        role = request.POST["role"]

        if password != confirm_password:
            context["msg"] = "Passwords must match."
            return render(request, "counterapp/auth/edit_user.html", context)

        try:
            User.update_user(user, username, email, password, role)
        except Exception as e:
            context["msg"] = "Error updating user"
            print(e)
            return render(request, "counterapp/auth/edit_user.html", context)

        context["users"] = User.get_all_users()
        return render(request, "counterapp/auth/users.html", context)


def delete_user(request, user_id):
    context = {}
    if request.method == "POST":
        users = User.get_all_users()
        context["users"] = users

        try:
            User.delete_user(user_id)
        except:
            context["msg"] = "failed to delete user"
            return render(request, "counterapp/auth/users.html", context)

        return render(request, "counterapp/auth/users.html", context)


def login(request):
    context = {}
    if request.method == "GET":
        if request.session is not None:
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
            request.session["username"] = user.name
            request.session["user_role"] = user.role
            return render(request, "counterapp/dashboard.html", context)

        else:
            context["msg"] = "wrong password provided!"
            return render(request, "counterapp/auth/login.html", context)


def logout(request):
    if request.session:
        del request.session["user_id"]
        del request.session["user_role"]
        del request.session["username"]
        return redirect("/login")


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


def add_reciept(request):
    context = {}
    if request.method == "GET":
        items = Item.get_all_items()
        context["items"] = items
        return render(request, "counterapp/add_receipt.html", context)

    if request.method == "POST":
        entries = request.POST["entries"]
        if entries is None:
            context["msg"] = "Add entries to the reciepts"
            return render(request, "counterapp/add_receipt.html", context)
        try:
            receipt = Receipt.objects.create(voucher_no=request.POST["voucher_no"])
            reciept_items = []
            for entry in json.loads(entries):
                item_id = (
                    int(re.match(r"\d+", entry["item"]).group())
                    if re.match(r"\d+", entry["item"])
                    else None
                )
                reciept_item = ReceiptItem(
                    code_no=entry["code_no"],
                    description=entry["description"],
                    quantity=entry["quantity"],
                    item_id=item_id,
                    remarks=entry["remarks"],
                    receipt=receipt,
                )
                reciept_items.append(reciept_item)

                item = Item.get_item_by_id(item_id)
                item.count += int(entry["quantity"])
                item.save()

            ReceiptItem.objects.bulk_create(reciept_items)

        except Exception as e:
            print(e)
            items = Item.get_all_items()
            context["items"] = items
            context["msg"] = "Error saving reciept!"
            return render(request, "counterapp/add_receipt.html", context)

        receipts = ReceiptItem.objects.all()
        context["receipts"] = receipts
        return render(request, "counterapp/receipts.html", context)


def issues(request):
    context = {}
    issues = IssueItem.get_issue_items()
    context["issues"] = issues

    return render(request, "counterapp/issues.html", context)


def issue_detail(request, voucher_no):
    context = {}
    issues = Issue.get_issues_by_voucher_no(voucher_no)
    context["issues"] = issues

    return render(request, "counterapp/issues.html", context)


def add_issue(request):
    context = {}
    if request.method == "GET":
        items = Item.get_all_items()
        context["items"] = items
        return render(request, "counterapp/add_issue.html", context)

    if request.method == "POST":
        entries = request.POST["entries"]
        if not entries:
            context["msg"] = "Add entries of issues"
            return render(request, "counterapp/add_issue.html", context)
        try:
            issue = Issue.objects.create(voucher_no=request.POST["voucher_no"])
            issue_items = []
            for entry in json.loads(entries):
                item_id = (
                    int(re.match(r"\d+", entry["item"]).group())
                    if re.match(r"\d+", entry["item"])
                    else None
                )
                issue_item = IssueItem(
                    code_no=entry["code_no"],
                    description=entry["description"],
                    item_id=item_id,
                    quantity_issued=entry["quantity_issued"],
                    issue=issue,
                )
                issue_items.append(issue_item)
                item = Item.get_item_by_id(item_id)
                if item.count > 0:
                    item.count -= entry["quantity_issued"]
                    item.save()

            IssueItem.objects.bulk_create(issue_items)
        except Exception as e:
            items = Item.get_all_items()
            context["items"] = items
            context["msg"] = "Error adding issue entry"
            return render(request, "counterapp/add_issue.html", context)

        issues = IssueItem.get_issue_items()
        context["issues"] = issues
        return render(request, "counterapp/issues.html", context)


def requisitions(request):
    context = {}
    requisitions = RequisitionItem.get_requisition_items()
    context["requisitions"] = requisitions

    return render(request, "counterapp/requisitions.html", context)


def requisition_detail(request, voucher_no):
    context = {}
    requisitions = Requisition.get_requisitions_by_voucher_no(voucher_no)
    context["requisitions"] = requisitions

    return render(request, "counterapp/requisitions.html", context)


def add_requisition(request):
    context = {}
    if request.method == "GET":
        items = Item.get_all_items()
        context["items"] = items
        return render(request, "counterapp/add_requisition.html", context)

    if request.method == "POST":
        entries = request.POST["entries"]
        if entries is None:
            context["msg"] = "Add entries of a requisition"
            return render(request, "counterapp/add_requisition.html", context)
        try:
            requisition = Requisition.objects.create(
                voucher_no=request.POST["voucher_no"]
            )
            requisition_items = []
            for entry in json.loads(entries):
                item_id = (
                    int(re.match(r"\d+", entry["item"]).group())
                    if re.match(r"\d+", entry["item"])
                    else None
                )
                req_item = RequisitionItem(
                    code_no=entry["code_no"],
                    description=entry["description"],
                    item_id=item_id,
                    quantity_required=entry["quantity_required"],
                    requisition=requisition,
                )
                requisition_items.append(req_item)
                item = Item.get_item_by_id(item_id)
                item.count += 1
                item.save()

            RequisitionItem.objects.bulk_create(requisition_items)

        except Exception as e:
            print(e)
            items = Item.get_all_items()
            context["items"] = items
            context["msg"] = "Error adding requisition entries"
            return render(request, "counterapp/add_requisition.html", context)

        requisitions = RequisitionItem.get_requisition_items()
        context["requisitions"] = requisitions
        return render(request, "counterapp/requisitions.html", context)


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
        issues = Issue.get_issues()
        requisitions = Requisition.get_requisitions()
        context["receipts"] = reciepts
        context["issues"] = issues
        context["requisitions"] = requisitions
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
