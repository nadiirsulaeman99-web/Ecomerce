from django import forms
from .models import Order, OrderPay
from cart.cart import Cart
from django.core.exceptions import ValidationError

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields= ['frist_name', 'last_name', 'email', 'address', 'postal_code', 'city']




class OrderPayForm(forms.ModelForm):
    class Meta:
        model = OrderPay
        fields= ['pay_phone', 'amount']
        widgets = {
            # Tan ayaa ka dhigaysa mid aan Template-ka ka muuqan laakiin xogta xambaarsan
            'amount': forms.HiddenInput(), 
        }

    def __init__(self, *args, **kwargs):
        cart = kwargs.pop('cart',None)
        super().__init__(*args, **kwargs)

        self.cart = cart
        if self.cart:
            total = self.cart.get_total_price()
            self.fields['amount'].initial = total

            # Haddii form-ku xog wado (POST), halkan ku qasab:
            if self.is_bound and 'amount' not in self.data:
                self.data = self.data.copy() # Ka dhig mid la beddeli karo
                self.data['amount'] = total
            # self.fields['amount'].initial = self.cart.get_total_price() 

    def clean_pay_phone(self):
        pay_phone = self.cleaned_data.get('pay_phone')
        if not pay_phone.isdigit():
            raise ValidationError('Fadlan number oo kaliya qor.')
        
        if len(pay_phone) != 9:
            raise ValidationError("Fadlan '9' number qor adigo kabilabaya [61,62,68]. ")
        
        valid_prafixes = ('61','62','68')
        if not any(pay_phone.startswith(prefix) for prefix in valid_prafixes):
            raise ValidationError('Fadalan kubilaaw number: 61 ama 62 ama 68')
        return pay_phone
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not self.cart:
            return amount

        if amount <= 0:
            raise ValidationError("Fadalan Lama ogola '0' iyo waxi kayar ee hagalin.")
        
        total_price = self.cart.get_total_price()
        if float(amount) != float(total_price):
            raise ValidationError("Fadalan dir isugayn'ta qimaha lagaa rabo.")

        return amount
        
        
        


    
        
    