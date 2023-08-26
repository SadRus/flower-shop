from django import forms

from phonenumber_field.formfields import PhoneNumberField

from shop.models import Timeslot, Consultation


class OrderForm(forms.Form):
	error_css_class = 'error'

	name = forms.CharField(
		label='',
		required=True,
		max_length=250,
		min_length=2,
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Введите Имя',
				'class': 'order__form_input',
			}
		)
	)
	phone = PhoneNumberField(
		label='',
		widget=forms.TextInput(
			attrs={
				'placeholder': '+7 (999) 000 00 00',
				'class': 'order__form_input',
			}
		)
	)
	phone.error_messages['invalid'] = 'Номер телефона введен неверно! Исправьте, пожалуйста'

	address = forms.CharField(
		label='',
		required=True,
		max_length=255,
		min_length=2,
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Адрес доставки',
				'class': 'order__form_input',
			}
		)
	)
	timeslot = forms.ModelChoiceField(
		widget=forms.RadioSelect(
			attrs={
				'class': 'order__form_radio',
			}
		),
		queryset=Timeslot.objects.all(),
	)


class ConsultationForm(forms.ModelForm):
	class Meta:
		model = Consultation
		fields = ['name', 'phone']
		labels = {
			'name': '',
			'phone': '',
		}
		widgets = {
			'name': forms.TextInput(
				attrs={
					'placeholder': 'Введите имя',
					'class': 'order__form_input',
				}
			),
			'phone': forms.TextInput(
				attrs={
					'placeholder': '+7 (999) 000 00 00',
					'class': 'order__form_input',
				}
			),
		}