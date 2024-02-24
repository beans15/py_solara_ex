from reacton import component
from solara.alias import rv as v
from solara.components.input import use_change
from typing import Callable
import solara


@component
def InputTextarea(
    label: str,
    value: str | solara.Reactive[str] = "",
    on_value: Callable[[str], None] | None = None,
    disabled: bool = False,
    continuous_update: bool = False,
    rows: float | str = 5,
    update_events: list[str] = ["blur", "keyup.enter"],
    error: bool | str = False,
    message: str | None = None,
    classes: list[str] = [],
    style: str | dict[str, str] | None = None,
):
    reactive_value = solara.use_reactive(value, on_value)
    del value, on_value
    style_flat = solara.util._flatten_style(style)
    classes_flat = solara.util._combine_classes(classes)

    def set_value_str(value):
        reactive_value.value = str(value)

    def on_v_model(value):
        if continuous_update:
            set_value_str(value)

    messages: list[str] = []
    if error and isinstance(error, str):
        messages.append(error)
    elif message:
        messages.append(message)

    textarea_field = v.Textarea(
        v_model=reactive_value.value,
        on_v_model=on_v_model,
        label=label,
        disabled=disabled,
        rows=rows,
        error=bool(error),
        messages=messages,
        class_=classes_flat,
        style_=style_flat,
    )

    use_change(
        textarea_field,
        set_value_str,
        (not continuous_update),
        update_events,
    )
