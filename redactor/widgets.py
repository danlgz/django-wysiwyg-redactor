from django.forms import widgets
from django.utils.safestring import mark_safe
from django.urls import reverse
import json
from django.conf import settings


GLOBAL_OPTIONS = getattr(settings, 'REDACTOR_OPTIONS', {})

INIT_JS = """<script type="text/javascript">
document.addEventListener('DOMContentLoaded', function() {
  jQuery(document).ready(function(){
    jQuery("#%s").redactor(%s);
  });
});

</script>
"""


class RedactorEditor(widgets.Textarea):

    class Media:
        js = (
            # 'redactor/jquery-1.7.min.js',
            'redactor/redactor.js',
        )
        css = {
            'all': (
                'redactor/css/redactor.css',
                'redactor/css/django_admin.css',
            )
        }

    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', None)
        self.custom_options = kwargs.pop('redactor_options', {})

        widget_attrs = {'class': 'redactor-box'}
        widget_attrs.update(kwargs.get('attrs', {}))
        kwargs['attrs'] = widget_attrs
        super(RedactorEditor, self).__init__(*args, **kwargs)

    def get_options(self):
        options = GLOBAL_OPTIONS.copy()
        options.update(self.custom_options)
        options['class'] = 'redactor-box'
        upload_to = self.upload_to
        options.update({
            'imageUpload': reverse('redactor_upload_image', kwargs={'upload_to': upload_to}),
            'fileUpload': reverse('redactor_upload_file', kwargs={'upload_to': upload_to})
        })

        return json.dumps(options)

    def render(self, name, value, attrs=None, renderer=None):
        html = super(RedactorEditor, self).render(name, value, attrs)
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id')
        html += INIT_JS % (id_, self.get_options())
        return mark_safe(html)


# For backward compatibility
JQueryEditor = RedactorEditor
