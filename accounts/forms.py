from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from ppid import models 
from django.core.exceptions import ValidationError

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DataForm(ModelForm):
	class Meta:
		model = models.Data
		fields = '__all__'
		widgets = {
			'code': forms.TextInput(
				attrs = {
				'placeholder': 'Contoh DISHUB-001',
				'class':'form-control',
				'required':''
				}
			), 
			'responsible': forms.TextInput(
				attrs = {
				'placeholder': 'Penanggung Jawab Penerbitan',
				'class':'form-control',
				}
			), 
            'title': forms.TextInput(
				attrs = {
				'placeholder': 'Judul DIP',
				'class':'form-control',
				'required':''
				}
			), 
            'information': forms.Textarea(
				attrs = {
				'placeholder': 'Deskripsi',
				'class':'form-control',
				}
			), 
			'type_data': forms.Select(
				attrs = {
				'class':'form-control',
				'required':''
				}
			), 
            'file': forms.FileInput(
				attrs = {
				'class': 'form-control',
				'required':''
				}
			), 
            'date_a': forms.TextInput(
				attrs = {
				'type': 'date',
				'class':'form-control'
				}
			), 
            'date_b': forms.TextInput(
				attrs = {
				'type': 'date',
				'class':'form-control'
				}
			), 
		}

	def clean_code(self):
		code = self.cleaned_data.get('code')
		if (code == ""):
			raise forms.ValidationError('Kode Tidak Boleh Kosong')
		for instance in models.Data.objects.all():
			if instance.code == code:
				raise forms.ValidationError('Kode Sudah Pernah Digunakan')
		return code


class DataFormUpdate(ModelForm):
	class Meta:
		model = models.Data
		fields = '__all__'
		widgets = {
			'code': forms.TextInput(
				attrs = {
				'placeholder': 'Contoh DISHUB-001',
				'class':'form-control'
				}
			), 
			'responsible': forms.TextInput(
				attrs = {
				'placeholder': 'Penanggung Jawab Penerbitan',
				'class':'form-control'
				}
			), 
            'title': forms.TextInput(
				attrs = {
				'placeholder': 'Judul DIP',
				'class':'form-control'
				}
			), 
            'information': forms.Textarea(
				attrs = {
				'placeholder': 'Deskripsi',
				'class':'form-control'
				}
			), 
			'type_data': forms.Select(
				attrs = {
				'class':'form-control'
				}
			), 
            # 'file': forms.FileInput(
			# 	attrs = {
			# 	'class': 'form-control',
			# 	}
			# ), 
            'date_a': forms.TextInput(
				attrs = {
				'type': 'date',
				'class':'form-control'
				}
			), 
            'date_b': forms.TextInput(
				attrs = {
				'type': 'date',
				'class':'form-control'
				}
			), 
		}

class RequestForm(ModelForm):
    class Meta:
        model = models.Form_information
        fields = '__all__'
        widgets = {
			'name': forms.TextInput(
				attrs = {
				'placeholder': 'Nama Lengkap',
                'class' : 'form-control',
				'readonly' : ''
				}
			), 
            'address': forms.Textarea(
				attrs = {
				'class': 'form-control',
				'placeholder': 'Alamat',
				'readonly' : ''
				}
			), 
            'telp': forms.TextInput(
				attrs = {
				'placeholder': 'No Telp',
				'type': 'number',
                'class' : 'form-control',
				'readonly' : ''
				}
			), 
            'email': forms.TextInput(
				attrs = {
				'placeholder': 'Email',
                'class' : 'form-control',
				'readonly' : ''
				}
			), 
            'purpose': forms.Textarea(
				attrs = {
				'placeholder': 'Tujuan Penggunaan Informasi',
				'class' : 'form-control',
				'readonly' : ''
				}
			), 
             'detail': forms.Textarea(
				attrs = {
				'placeholder': 'Detail Informasi Yang Dibutuhkan',
				'class' : 'form-control',
				'readonly' : ''
				}
			), 
            'status': forms.Select(
				attrs = {
                'class':'form-control'
				}
			), 
            'dinas': forms.Select(
				attrs = {
				'readonly' : ''
				}
			), 
			'Information': forms.Textarea(
				attrs = {
				'class' : 'form-control'
				}
			), 
		}

class ProfileForm(ModelForm):
    class Meta:
        model = models.Dinas
        fields = '__all__'
        widgets = {
			'title': forms.TextInput(
				attrs = {
                'class' : 'form-control',
				}
			), 
			'shortness': forms.TextInput(
				attrs = {
                'class' : 'form-control',
				}
			), 
			'email': forms.TextInput(
				attrs = {
                'class' : 'form-control',
				}
			), 
			'telp': forms.TextInput(
				attrs = {
                'class' : 'form-control',
				}
			), 
			'website': forms.TextInput(
				attrs = {
                'class' : 'form-control',
				}
			), 
		}


		






