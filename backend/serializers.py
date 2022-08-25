from typing import Any, OrderedDict, Union

from django.db.models import QuerySet
from rest_framework import serializers


class SlugRelatedOptionalField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        if data:

            queryset = self.get_queryset().filter(**{self.slug_field: data})  # type: ignore
            if queryset.exists():
                return queryset.first()
        return data


class SlugRelatedGetOrCreateField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        if data:
            queryset = self.get_queryset()
            try:
                return queryset.get_or_create(**{self.slug_field: data})[  # type: ignore
                    0
                ]

            except (TypeError, ValueError):
                self.fail("invalid")
        return data


def convert_var_to_obj(variable, model, key) -> Any:
    if isinstance(variable, model):
        return variable
    elif not variable:
        return None
    elif isinstance(variable, str):
        params = {key: variable}
        obj, _ = model.objects.get_or_create(**params)
    elif isinstance(variable, (dict, OrderedDict)):
        obj, _ = model.objects.get_or_create(**variable)
    elif isinstance(variable, list):
        new_list = []
        for i, value in enumerate(variable):
            new_list.append(convert_var_to_obj(value, model, key))
        filtered_new_list = [i for i in new_list if i is not None]
        if len(filtered_new_list) > 0:
            return filtered_new_list
        return None

    else:
        raise TypeError("unsupported type")
