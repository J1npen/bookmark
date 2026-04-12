import uuid
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from alipay import AliPay

from .models import PaymentOrder

PAYMENT_AMOUNT = Decimal('5.00')
ALIPAY_SANDBOX_GATEWAY = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do'
ALIPAY_GATEWAY = 'https://openapi.alipay.com/gateway.do'


def _get_alipay():
    cfg = settings.ALIPAY_CONFIG
    app_private_key = (
        '-----BEGIN RSA PRIVATE KEY-----\n'
        + cfg['app_private_key']
        + '\n-----END RSA PRIVATE KEY-----'
    )
    alipay_public_key = (
        '-----BEGIN PUBLIC KEY-----\n'
        + cfg['alipay_public_key']
        + '\n-----END PUBLIC KEY-----'
    )
    return AliPay(
        appid=cfg['appid'],
        app_notify_url=None,
        app_private_key_string=app_private_key,
        alipay_public_key_string=alipay_public_key,
        sign_type='RSA2',
        debug=cfg['sandbox'],
    )


def _gateway():
    return ALIPAY_SANDBOX_GATEWAY if settings.ALIPAY_CONFIG['sandbox'] else ALIPAY_GATEWAY


# ── 注册信息页（展示付款说明）──────────────────────────────────────────────────

def register_info(request):
    if request.user.is_authenticated:
        return redirect('/')

    pending = request.session.get('pending_out_trade_no')
    if pending:
        try:
            order = PaymentOrder.objects.get(out_trade_no=pending)
            if order.status == 'paid':
                return render(request, 'payment/return.html', {
                    'out_trade_no': pending,
                    'paid': True,
                })
            elif order.status == 'registered':
                del request.session['pending_out_trade_no']
                pending = None
            # status='pending'：notify 未到，继续展示说明页并给提示
        except PaymentOrder.DoesNotExist:
            del request.session['pending_out_trade_no']
            pending = None

    return render(request, 'payment/register.html', {
        'amount': PAYMENT_AMOUNT,
        'has_pending_order': pending is not None,
    })


# ── 创建订单并跳转支付宝 ──────────────────────────────────────────────────────

def create_order(request):
    if request.method != 'POST':
        return redirect('payment:register_info')
    if request.user.is_authenticated:
        return redirect('/')

    out_trade_no = uuid.uuid4().hex
    PaymentOrder.objects.create(out_trade_no=out_trade_no, amount=PAYMENT_AMOUNT)
    request.session['pending_out_trade_no'] = out_trade_no

    alipay = _get_alipay()
    return_url = request.build_absolute_uri('/payment/return/')
    notify_url = request.build_absolute_uri('/payment/notify/')

    order_string = alipay.client_api(
        'alipay.trade.page.pay',
        biz_content={
            'out_trade_no': out_trade_no,
            'total_amount': str(PAYMENT_AMOUNT),
            'subject': '书签收藏服务注册费',
            'product_code': 'FAST_INSTANT_TRADE_PAY',
        },
        return_url=return_url,
        notify_url=notify_url,
    )

    return redirect(f'{_gateway()}?{order_string}')


# ── 支付宝同步回调（用户支付后跳回）──────────────────────────────────────────

def payment_return(request):
    params = {k: v for k, v in request.GET.items()}
    sign = params.pop('sign', None)

    alipay = _get_alipay()
    verified = alipay.verify(params, sign)

    if not verified:
        return render(request, 'payment/return.html', {
            'error': '支付验证签名失败，请重试或联系管理员。',
        })

    out_trade_no = params.get('out_trade_no', '')
    trade_no = params.get('trade_no', '')

    try:
        order = PaymentOrder.objects.get(out_trade_no=out_trade_no)
    except PaymentOrder.DoesNotExist:
        return render(request, 'payment/return.html', {'error': '订单不存在。'})

    if order.status == 'registered':
        return render(request, 'payment/return.html', {
            'error': '此订单已完成注册，请直接登录。',
        })

    if order.status == 'pending':
        order.status = 'paid'
        order.trade_no = trade_no
        order.paid_at = timezone.now()
        order.save()

    return render(request, 'payment/return.html', {
        'out_trade_no': out_trade_no,
        'paid': True,
    })


# ── 支付宝异步通知 ────────────────────────────────────────────────────────────

@csrf_exempt
def payment_notify(request):
    if request.method != 'POST':
        return HttpResponse('fail')

    params = {k: v for k, v in request.POST.items()}
    sign = params.pop('sign', None)

    alipay = _get_alipay()
    if not alipay.verify(params, sign):
        return HttpResponse('fail')

    if params.get('trade_status') in ('TRADE_SUCCESS', 'TRADE_FINISHED'):
        out_trade_no = params.get('out_trade_no', '')
        trade_no = params.get('trade_no', '')
        PaymentOrder.objects.filter(
            out_trade_no=out_trade_no, status='pending'
        ).update(
            status='paid',
            trade_no=trade_no,
            paid_at=timezone.now(),
        )

    return HttpResponse('success')


# ── 提交注册表单 ──────────────────────────────────────────────────────────────

def do_register(request):
    if request.method != 'POST':
        return redirect('payment:register_info')

    out_trade_no = request.POST.get('out_trade_no', '').strip()
    username = request.POST.get('username', '').strip()
    password1 = request.POST.get('password1', '')
    password2 = request.POST.get('password2', '')

    def show_form_error(msg):
        return render(request, 'payment/return.html', {
            'out_trade_no': out_trade_no,
            'paid': True,
            'reg_error': msg,
            'prev_username': username,
        })

    try:
        order = PaymentOrder.objects.get(out_trade_no=out_trade_no, status='paid')
    except PaymentOrder.DoesNotExist:
        return render(request, 'payment/return.html', {
            'error': '支付订单无效或已使用，请重新支付。',
        })

    if not username:
        return show_form_error('用户名不能为空。')
    if len(username) < 3:
        return show_form_error('用户名至少需要 3 个字符。')
    if User.objects.filter(username=username).exists():
        return show_form_error('该用户名已被注册，请换一个。')
    if len(password1) < 6:
        return show_form_error('密码至少需要 6 位。')
    if password1 != password2:
        return show_form_error('两次输入的密码不一致。')

    user = User.objects.create_user(username=username, password=password1)
    order.status = 'registered'
    order.save()

    request.session.pop('pending_out_trade_no', None)
    login(request, user)
    return redirect('/')
