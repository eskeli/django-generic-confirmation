import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from generic_confirmation.fields import PickledObjectField


class ConfirmationManager(models.Manager):
    def confirm(self, token):
        try:
            action = self.get(token=token)
        except self.model.DoesNotExist:
            return False
            
        if not action.is_expired():
            return action.resume_form_save()
        
        return False


class DeferredAction(models.Model):
    token = models.CharField(max_length=40)
    valid_until = models.DateTimeField(null=True)
    confirmed = models.BooleanField(default=False)
    
    form_class = models.CharField(max_length=255)
    form_input = PickledObjectField(editable=False)
    
    content_type = models.ForeignKey(ContentType, null=True)
    object_pk = models.TextField(null=True)
    instance_object = generic.GenericForeignKey('content_type', 'object_pk')
    
    objects = ConfirmationManager()
    
    def resume_form_save(self):
        form_class_name = self.form_class
        dot_index = form_class_name.rindex('.')
        module = form_class_name[:dot_index]
        klass = form_class_name[dot_index+1:] 
        form_module = __import__(module, {}, {}, [''])
        form_class = getattr(form_module, klass)
        
        if self.instance_object is None:
            form = form_class(self.form_input)
        else:
            form = form_class(self.form_input, instance=self.instance_object)
        
        if not form.is_valid():
            raise Exception("the defered form was not cleaned properly before saving")
    
        obj = form.save_original()
        obj.save()
        return obj
    
    
    def is_expired(self):
        if self.valid_until is None:
            return False
        now = datetime.datetime.now()
        return self.valid_until - now <= datetime.timedelta(days=5) #FIXME: hardcoded
    is_expired.boolean = True

    

        
        