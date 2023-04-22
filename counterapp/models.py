from django.db import models
from django.contrib.auth.hashers import make_password


class Item(models.Model):
    name = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    description = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def create_item(name):
        return Item.objects.create(name=name)

    def get_all_items():
        return Item.objects.all()

    def get_item_by_id(id):
        return Item.objects.filter(id=id).first()

    def delete_item(id):
        item = Item.get_item_by_id(id)
        item.delete()
        return


class Receipt(models.Model):
    voucher_no = models.IntegerField()
    order_no = models.CharField(max_length=255, null=True)
    invoice_no = models.CharField(max_length=255, null=True)
    issuing_officer = models.CharField(max_length=255, null=True)
    issuing_officer_designation = models.CharField(max_length=255, null=True)
    receiving_officer = models.CharField(max_length=255, null=True)
    receiving_officer_designation = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def get_reciepts():
        return Receipt.objects.all()

    def get_reciepts_by_voucher_no(voucher_no):
        rec = Receipt.objects.filter(voucher_no=voucher_no).first()
        return rec.receipt_items.all()


class Requisition(models.Model):
    voucher_no = models.IntegerField()
    order_no = models.CharField(max_length=255, null=True)
    invoice_no = models.CharField(max_length=255, null=True)
    requisitioning_officer = models.CharField(max_length=255, null=True)
    requisitioning_officer_designation = models.CharField(max_length=255, null=True)
    approved = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_requisitions():
        return Requisition.objects.all()

    def get_requisition_by_id(id):
        return Requisition.objects.filter(id=id).first()

    def get_requisitions_by_voucher_no(voucher_no):
        issue = Requisition.objects.filter(voucher_no=voucher_no).first()
        return issue.requisition_items.all()


class Issue(models.Model):
    voucher_no = models.IntegerField()
    order_no = models.CharField(max_length=255, null=True)
    invoice_no = models.CharField(max_length=255, null=True)
    issuing_officer = models.CharField(max_length=255, null=True)
    issuing_officer_designation = models.CharField(max_length=255, null=True)
    approved = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=255, null=True)
    receiving_officer = models.CharField(max_length=255, null=True)
    receiving_officer_designation = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_issues():
        return Issue.objects.all()

    def get_issues_by_voucher_no(voucher_no):
        issue = Issue.objects.filter(voucher_no=voucher_no).first()
        return issue.issue_items.all()


class RequisitionItem(models.Model):
    requisition = models.ForeignKey(
        Requisition,
        on_delete=models.CASCADE,
        related_name="requisition_items",
    )
    code_no = models.CharField(max_length=255)
    description = models.TextField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity_required = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def get_requisition_items():
        return RequisitionItem.objects.all()


class IssueItem(models.Model):
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="issue_items",
    )
    code_no = models.CharField(max_length=255)
    description = models.TextField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity_issued = models.IntegerField()
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def get_issue_items():
        return IssueItem.objects.all()


class ReceiptItem(models.Model):
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name="receipt_items",
    )
    code_no = models.IntegerField()
    description = models.TextField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    value = models.CharField(max_length=255)
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def get_receipt_items():
        return ReceiptItem.objects.all()


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(
        max_length=255,
        choices=(
            ("admin", "Admin"),
            ("user", "User"),
            ("issuing", "IssuingOfficer"),
            ("recieving", "RecievingOfficer"),
            ("requisitioning", "RequisitioningOfficer"),
        ),
        null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_user_by_email(email):
        return User.objects.filter(email=email).first()

    def get_all_users():
        return User.objects.all()

    def create_user(email, username, role, password):
        return User.objects.create(
            name=username, email=email, role=role, password=make_password(password)
        )

    def get_user_by_id(id):
        return User.objects.filter(id=id).first()

    def update_user(user, username, email, password, role):
        user.name = username
        user.email = email
        if password:
            user.password = make_password(password)

        user.role = role

        user.save()
        return

    def delete_user(id):
        user = User.get_user_by_id(id)
        user.delete()
        return
