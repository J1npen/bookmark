from django.db import models


class PaymentOrder(models.Model):
    """
    支付订单表。managed=False，需手动在 MySQL 中建表：

    CREATE TABLE payment_orders (
        id          BIGINT AUTO_INCREMENT PRIMARY KEY,
        out_trade_no VARCHAR(64)    NOT NULL UNIQUE,
        trade_no    VARCHAR(64)    NULL DEFAULT NULL,
        amount      DECIMAL(10,2)  NOT NULL DEFAULT 5.00,
        status      VARCHAR(20)    NOT NULL DEFAULT 'pending',
        created_at  DATETIME(6)    NOT NULL,
        paid_at     DATETIME(6)    NULL DEFAULT NULL
    );

    status 取值：pending / paid / registered
    """
    out_trade_no = models.CharField(max_length=64, unique=True)
    trade_no = models.CharField(max_length=64, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default='5.00')
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'payment_orders'

    def __str__(self):
        return f"{self.out_trade_no} [{self.status}]"
