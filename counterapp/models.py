from django.db import models


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


class RequisitionAndIssue(models.Model):
    voucher_no = models.IntegerField()
    order_no = models.CharField(max_length=255, null=True)
    invoice_no = models.CharField(max_length=255, null=True)
    issuing_officer = models.CharField(max_length=255, null=True)
    issuing_officer_designation = models.CharField(max_length=255, null=True)
    requisitioning_officer = models.CharField(max_length=255, null=True)
    requisitioning_officer_designation = models.CharField(max_length=255, null=True)
    receiving_officer = models.CharField(max_length=255, null=True)
    receiving_officer_designation = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_req_and_issues():
        return RequisitionAndIssue.objects.all()

    def get_issues_by_voucher_no(voucher_no):
        issue = RequisitionAndIssue.objects.filter(voucher_no=voucher_no).first()
        return issue.req_and_issue_items.all()


class RequisitionAndIssueItem(models.Model):
    receipt = models.ForeignKey(
        RequisitionAndIssue,
        on_delete=models.CASCADE,
        related_name="req_and_issue_items",
    )
    code_no = models.CharField(max_length=255)
    description = models.TextField()
    units = models.CharField(max_length=255)
    quantity_required = models.IntegerField()
    quantity_issued = models.IntegerField()
    value = models.CharField(max_length=255)
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def get_req_and_issue_items():
        return RequisitionAndIssueItem.objects.all()


class ReceiptItem(models.Model):
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name="receipt_items",
    )
    code_no = models.IntegerField()
    description = models.TextField()
    units = models.CharField(max_length=255)
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
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_user_by_email(email):
        return User.objects.filter(email=email).first()
