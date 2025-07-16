from typing import Any, TypeAlias

JSON: TypeAlias = dict[str, Any]


class Model:
    def __init__(self, payload: JSON):
        self.payload = payload


class Field:
    def __init__(self, path: str):
        self.path = path

    def _get_value(self, payload: JSON) -> Any:
        keys = self.path.split('.')
        data = payload
        for key in keys:
            try:
                data = data[key]
            except (TypeError, KeyError):
                return None
        return data

    def __get__(self, obj: Model, owner: type) -> Any:
        if obj is None:
            return None
        return self._get_value(obj.payload)

    def _set_value(self, payload: JSON, value: Any) -> None:
        keys = self.path.split('.')
        data = payload
        for key in keys[:-1]:
            try:
                data = data[key]
            except (TypeError, KeyError):
                data[key] = {}
                data = data[key]
        data[keys[-1]] = value

    def __set__(self, obj: Model, value: Any) -> None:
        if obj is None:
            return
        self._set_value(obj.payload, value)
