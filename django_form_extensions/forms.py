# encoding:utf-8
'''
Created on 2014.08.10

@author: preture
'''
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms.fields import Field
from django.utils.translation import ugettext_lazy


class SimpleListField(Field):
    default_error_messages = {
        'invalid': ugettext_lazy('Enter a valid value.'),
    }
    
    def __init__(self, inner_field=None, inner_form=None, max_length=None, min_length=None, *args, **kwargs):
        self.inner_field = inner_field
        self.inner_form = inner_form
        self.max_length = max_length
        self.min_length = min_length
        super(SimpleListField, self).__init__(*args, **kwargs)
        
        if inner_field and not isinstance(inner_field, Field):
            raise ValueError(u'inner_field invalid')
        if inner_form and not issubclass(inner_form, Form):
            raise ValueError(u'inner_form invalid')
        if not inner_field and not inner_form:
            raise ValueError(u'inner_field or inner_form must has one')
        if min_length is not None:
            self.validators.append(validators.MinLengthValidator(min_length))
        if max_length is not None:
            self.validators.append(validators.MaxLengthValidator(max_length))
    
    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return None
        if type(value) is not list:
            raise ValidationError(self.error_messages['invalid'])
        new_value = []
        if self.inner_field:
            for one in value:
                new_value.append(self.inner_field.to_python(one))
        elif self.inner_form:
            for one in value:
                _form = self.inner_form(one)
                if not _form.is_valid():
                    raise ValidationError(self.error_messages['invalid'])
                new_value.append(_form.cleaned_data)
        return new_value

class FormListField(Field):
    default_error_messages = {
        'invalid': ugettext_lazy('Enter a valid value.'),
    }
    
    def __init__(self, inner_forms, max_length=None, min_length=None, *args, **kwargs):
        self.inner_forms = inner_forms  # (k,{'k1':v1,'k2':v2})
        self.max_length = max_length
        self.min_length = min_length
        super(FormListField, self).__init__(*args, **kwargs)
        
        if (type(inner_forms) is not tuple) or (len(inner_forms) is not 2) or (type(self.inner_forms[1]) is not dict):
            raise ValueError(u'inner_forms invalid')
        if min_length is not None:
            self.validators.append(validators.MinLengthValidator(min_length))
        if max_length is not None:
            self.validators.append(validators.MaxLengthValidator(max_length))
    
    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return None
        if type(value) is not list:
            raise ValidationError(self.error_messages['invalid'])
        new_value = []
        for one in value:
            if not one.has_key(self.inner_forms[0]) or not one[self.inner_forms[0]] in self.inner_forms[1].keys():
                raise ValidationError(self.error_messages['invalid'])
            inner_form = self.inner_forms[1][one[self.inner_forms[0]]]
            if not issubclass(inner_form, Form):
                raise ValidationError(self.error_messages['invalid'])
            _form = inner_form(one)
            if not _form.is_valid():
                raise ValidationError(self.error_messages['invalid'])
            new_value.append(_form.cleaned_data)
        return new_value
    
class SimpleFormField(Field):
    default_error_messages = {
        'invalid': ugettext_lazy('Enter a valid value.'),
    }
    
    def __init__(self, inner_form, *args, **kwargs):
        self.inner_form = inner_form
        super(SimpleFormField, self).__init__(*args, **kwargs)
        if not issubclass(self.inner_form, Form):
            raise ValidationError(self.error_messages['invalid'])
    
    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return None
        if type(value) is not dict:
            raise ValidationError(self.error_messages['invalid'])
        _form = self.inner_form(one)
        if not _form.is_valid():
            raise ValidationError(self.error_messages['invalid'])
        return _form.cleaned_data