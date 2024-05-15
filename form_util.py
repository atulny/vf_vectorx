from abc import ABC, abstractmethod
from datetime import datetime, time
from typing import Any, Generic, Literal, TypeVar

import streamlit as st
from streamlit.elements.widgets.time_widgets import DateValue, DateWidgetReturn
from streamlit.runtime.uploaded_file_manager import UploadedFile
#from streamlit_tags import st_tags
#keywords = st_tags(‘Enter Keyword:’, ‘Press enter to add more’, [‘One’, ‘Two’, ‘Three’])



_T = TypeVar("_T")

_DEFAULT_NOT_SET = object()


class WidgetBuilder(ABC, Generic[_T]):
    default = _DEFAULT_NOT_SET

    @abstractmethod
    def build(self) -> _T:
        ...


# Widget builders for Streamlit input widgets
# Note "st.button and st.download_button cannot be added to a form."
# Ref: https://docs.streamlit.io/library/api-reference/control-flow/st.form


class Checkbox(WidgetBuilder[bool]):
    #label, value=False, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False,
    # label_visibility="visible"
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: bool = False

    def build(self) -> bool:
        kwargs = self.kwargs | {"value": self.default}
        return st.checkbox(*self.args, **kwargs)


class Toggle(WidgetBuilder[bool]):
    # label, value=False, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False,
    # label_visibility="visible"
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: bool = False

    def build(self) -> bool:
        kwargs = self.kwargs | {"value": self.default}
        return st.toggle(*self.args, **kwargs)


class Radio(WidgetBuilder[Any | None]):
    #label, options, index=0, format_func=special_internal_function, key=None, help=None, on_change=None, args=None,
    # kwargs=None, *, disabled=False, horizontal=False, captions=None, label_visibility="visible
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: int | None = 0

    def build(self) -> Any | None:
        kwargs = self.kwargs | {"index": self.default}
        return st.radio(*self.args, **kwargs)


class Selectbox(WidgetBuilder[Any | None]):
    #label, options, index = 0, format_func = special_internal_function, key = None, help = None, on_change = None,
    #args = None, kwargs = None, *, placeholder = "Choose an option", disabled = False, label_visibility = "visible
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: int | None = 0

    def build(self) -> Any | None:
        kwargs = self.kwargs | {"index": self.default}
        return st.selectbox(*self.args, **kwargs)


class Multiselect(WidgetBuilder[list[Any]]):
    #label, options, default=None, format_func=special_internal_function, key=None, help=None, on_change=None,
    # args=None, kwargs=None, *, max_selections=None, placeholder="Choose an option", disabled=False,
    # label_visibility="visible"
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: Any | None = None

    def build(self) -> list[Any]:
        kwargs = self.kwargs | {"default": self.default}
        return st.multiselect(*self.args, **kwargs)


class Slider(WidgetBuilder[Any]):
    #label, min_value = None, max_value = None, value = None, step = None, format = None, key = None, help = None,
    #   on_change = None, args = None, kwargs = None, *, disabled = False, label_visibility = "visible"
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: Any | None = None

    def build(self) -> Any:
        kwargs = self.kwargs | {"value": self.default}
        return st.slider(*self.args, **kwargs)


class SelectSlider(WidgetBuilder[Any | tuple[Any]]):
  #label, options=(), value=None, format_func=special_internal_function, key=None, help=None, on_change=None,
  # args=None, kwargs=None, *, disabled=False, label_visibility="visible"
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default = None

    def build(self) -> Any | tuple[Any]:
        kwargs = self.kwargs | {"value": self.default}
        return st.select_slider(*self.args, **kwargs)


class TextInput(WidgetBuilder[str | None]):
    #label, value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None,
    # args=None, kwargs=None, *, placeholder=None, disabled=False, label_visibility="visible"
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: str = ""

    def build(self) -> str | None:
        kwargs = self.kwargs | {"value": self.default}
        return st.text_input(*self.args, **kwargs)  # type: ignore[no-any-return]


class NumberInput(WidgetBuilder[int | float | None]):
    #label, min_value=None, max_value=None, value="min", step=None, format=None, key=None, help=None, on_change=None,
    # args=None, kwargs=None, *, placeholder=None, disabled=False, label_visibility="visible"
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: int | float | Literal["min"] = "min"

    def build(self) -> int | float | None:
        kwargs = self.kwargs | {"value": self.default}
        return st.number_input(*self.args, **kwargs)  # type: ignore[no-any-return]


class TextArea(WidgetBuilder[str | None]):
    #label, value="", height=None, max_chars=None, key=None, help=None, on_change=None, args=None, kwargs=None, *,
    # placeholder=None, disabled=False, label_visibility="visible"
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: str = ""

    def build(self) -> str | None:
        kwargs = self.kwargs | {"value": self.default}
        return st.text_area(*self.args, **kwargs)  # type: ignore[no-any-return]


class DateInput(WidgetBuilder[DateWidgetReturn]):
    #label, value="default_value_today", min_value=None, max_value=None, key=None, help=None, on_change=None,
    # args=None, kwargs=None, *, format="YYYY/MM/DD", disabled=False, label_visibility="visible"
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: DateValue | Literal["today"] = "today"

    def build(self) -> DateWidgetReturn:
        kwargs = self.kwargs | {"value": self.default}
        return st.date_input(*self.args, **kwargs)


class TimeInput(WidgetBuilder[time | None]):
    #label, value="now", key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False,
    # label_visibility="visible", step=0:15:00
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: time | datetime | Literal["now"] = "now"

    def build(self) -> time | None:
        kwargs = self.kwargs | {"value": self.default}
        return st.time_input(*self.args, **kwargs)  # type: ignore[no-any-return]


class FileUploader(WidgetBuilder[Any]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def build(self) -> Any:
        return st.file_uploader(*self.args, **self.kwargs)


class CameraInput(WidgetBuilder[UploadedFile | None]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def build(self) -> UploadedFile | None:
        return st.camera_input(*self.args, **self.kwargs)


class ColorPicker(WidgetBuilder[str]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: str | None = None

    def build(self) -> str:
        kwargs = self.kwargs | {"value": self.default}
        return st.color_picker(*self.args, **kwargs)


def manager():
    with st.expander("Example"):
        user_input = st.text_input("Enter a key")
        add_button = st.button("Add", key='add_button')
        if add_button:
            if len(user_input) > 0:
                st.session_state['my_lst'] += [user_input]
                st.write( st.session_state['my_lst'] )
            else:
                st.warning("Enter text")


def render_fields(fields, data,form_key ):
    for f in fields:
        name = f.get("name")
        st.text_input(label=f.get("label", name).capitalize(), key=f'{form_key}_{name}', value=data.get(name, ""))