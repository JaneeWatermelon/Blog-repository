import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from yookassa import Configuration, Payment

from common.views import TitleMixin
from donate.forms import DonateForm

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
        print(self.object)
        print(self.object.price)
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
        return HttpResponseRedirect(payment['confirmation']['confirmation_url'])

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.instance.price < 50:
            form.instance.price = 50

        return super().form_valid(form)

class DonateResultView(TitleMixin, TemplateView):
    title = 'Donate Result Page'
    template_name = 'donate/donate_result.html'

    # def get_context_data(self, **kwargs):
    #     payment_id = self.request.args[0]
    #     payment = Payment.find_one(payment_id)
    #     context = super(DonateResultView, self).get_context_data(**kwargs)
    #     context['status'] = payment['status']
    #     return context




