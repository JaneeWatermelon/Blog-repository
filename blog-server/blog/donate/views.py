import uuid
import json

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotification

from common.views import TitleMixin
from donate.forms import DonateForm
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings


class DonateView(TitleMixin, CreateView):
    template_name = 'donate/donate.html'
    title = 'Donate Page'
    form_class = DonateForm
    success_url = reverse_lazy('all_news')

    def post(self, request, *args, **kwargs):
        print('in post donate')
        super(DonateView, self).post(request, *args, **kwargs)
        Configuration.account_id = 437547
        Configuration.secret_key = 'test_10xHP8xjuHzVzzxh_3_cAOj0CWoqkEuA04bMzVT1DXY'
        payment = Payment.create({
            "amount": {
                "value": f"{self.object.price}.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": f"{settings.DOMAIN_NAME}/donate/result"
            },
            "capture": True,
            "description": f"Заказ №{self.object.id}"
        }, uuid.uuid4())
        self.request.session['payment_id'] = payment['id']
        return HttpResponseRedirect(payment['confirmation']['confirmation_url'])

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.instance.price < 50:
            form.instance.price = 50

        return super().form_valid(form)

class DonateResultView(TitleMixin, TemplateView):
    title = 'Donate Result Page'
    template_name = 'donate/donate_result.html'

    def get_context_data(self, **kwargs):
        print('in get_context_data')
        payment_id = self.request.session.get('payment_id')
        # del self.request.session['payment_id']
        print(payment_id)
        payment = Payment.find_one(payment_id)
        context = super(DonateResultView, self).get_context_data(**kwargs)
        context['status'] = payment['status']
        return context
@csrf_exempt
def my_webhook_handler(request):
    print('in webhook')
    event_json = json.loads(request.body)
    notification_object = WebhookNotification(event_json)
    payment_id = notification_object.object.status
    # request.session.setdefault('status', payment_id)
    # request.session['status'] = payment_id
    return HttpResponse(status=200)



