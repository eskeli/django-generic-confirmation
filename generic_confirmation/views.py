from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from generic_confirmation.forms import ConfirmationForm



def confirm_by_form(request, template_name='confirm.html', 
                    success_template_name='confirmed.html', 
                    success_url=None, success_message=None,
                    form_class=ConfirmationForm):
    """
    If ``success_url`` is not None a redirect to ``success_url`` will
    be issued, once the entered confirmation code was confirmed successfully.
    Optionally, of ``success_message`` is not None, it will be set via
    Django's message system.
    
    If ``success_url`` is None the template ``success_template_name`` will
    be rendered once the confirmation is complete. The ``success_message``
    will then be added to the template context instead of the message_set.
    
    """
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            if success_url is None:
                return render_to_response(success_template_name, 
                    {'success_message': success_message}, 
                    context_instance=RequestContext(request))
            else:
                if success_message is not None:
                    messages.add_message(request, messages.SUCCESS, success_message)
                return HttpResponseRedirect(success_url)
    else:
        form = form_class()
    return render_to_response(template_name, {'form': form}, 
                              context_instance=RequestContext(request))



def confirm_by_get(request, token, template_name='confirm.html', 
                   success_template_name="confirmed.html", 
                   success_url=None, success_message=None,
                   expired_template_name="confirm_expired.html",
                   expired_message=None,
                   form_class=ConfirmationForm):
    form = form_class({'token': token})
    if form.is_valid():
        try:
            form_save = form.save()
        except:
            form_save = False
        if form_save:
            if success_url is None:
                return render_to_response(success_template_name, 
                        {'success_message': success_message}, 
                        context_instance=RequestContext(request))
            else:
                if success_message is not None:
                    messages.add_message(request, messages.SUCCESS, success_message)
                return HttpResponseRedirect(success_url)
        else:
            return render_to_response(expired_template_name, 
                        {'expired_message': expired_message}, 
                        context_instance=RequestContext(request))
    else:
        return render_to_response(template_name, {}, 
                                  context_instance=RequestContext(request))
    
    
    
    
    
