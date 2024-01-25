from django.template.defaultfilters import register


@register.filter(name='dictslice')
def dictslice(dict_object, keys):
    selected = [elem.strip() for elem in keys.split(',')]
    return {k: dict_object[k] for k in selected if dict_object.get(k) is not None}