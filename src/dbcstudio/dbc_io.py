from __future__ import annotations

from pathlib import Path
from typing import Union

from .model import DbcDocument, MessageModel, SignalModel


def load_dbc(path: str) -> DbcDocument:
    import cantools

    db = cantools.database.load_file(path)
    messages: list[MessageModel] = []

    for message in db.messages:
        msg = MessageModel(
            frame_id=message.frame_id,
            name=message.name,
            length=message.length,
            senders=list(message.senders),
            signals=[],
        )
        for signal in message.signals:
            converted = SignalModel(
                name=signal.name,
                start=signal.start,
                length=signal.length,
                byte_order=signal.byte_order,
                is_signed=signal.is_signed,
                scale=float(signal.scale),
                offset=float(signal.offset),
                minimum=float(signal.minimum) if signal.minimum is not None else None,
                maximum=float(signal.maximum) if signal.maximum is not None else None,
                unit=signal.unit or "",
                receivers=list(signal.receivers),
            )
            msg.signals.append(converted)
        messages.append(msg)

    return DbcDocument(path=path, version=db.version, messages=messages)


def save_dbc(doc: DbcDocument, path: str) -> None:
    lines: list[str] = []
    lines.append('VERSION "{}"'.format(doc.version or ""))
    lines.append("")
    lines.append("NS_ :")
    lines.extend([
        "\tNS_DESC_",
        "\tCM_",
        "\tBA_DEF_",
        "\tBA_",
        "\tVAL_",
        "\tCAT_DEF_",
        "\tCAT_",
        "\tFILTER",
        "\tBA_DEF_DEF_",
        "\tEV_DATA_",
        "\tENVVAR_DATA_",
        "\tSGTYPE_",
        "\tSGTYPE_VAL_",
        "\tBA_DEF_SGTYPE_",
        "\tBA_SGTYPE_",
        "\tSIG_TYPE_REF_",
        "\tVAL_TABLE_",
        "\tSIG_GROUP_",
        "\tSIG_VALTYPE_",
        "\tSIGTYPE_VALTYPE_",
        "\tBO_TX_BU_",
        "\tBA_DEF_REL_",
        "\tBA_REL_",
        "\tBA_DEF_DEF_REL_",
        "\tBU_SG_REL_",
        "\tBU_EV_REL_",
        "\tBU_BO_REL_",
        "\tSG_MUL_VAL_",
    ])
    lines.append("")
    lines.append("BS_:")
    lines.append("")

    node_set = {sender for message in doc.messages for sender in message.senders if sender}
    for message in doc.messages:
        for signal in message.signals:
            node_set.update(receiver for receiver in signal.receivers if receiver)
    node_text = " ".join(sorted(node_set)) if node_set else "Vector__XXX"
    lines.append(f"BU_: {node_text}")
    lines.append("")

    for message in doc.messages:
        sender = message.senders[0] if message.senders else "Vector__XXX"
        lines.append(f"BO_ {message.frame_id} {message.name}: {message.length} {sender}")
        for signal in message.signals:
            endian = "1" if signal.byte_order == "little_endian" else "0"
            sign = "-" if signal.is_signed else "+"
            minimum = signal.minimum if signal.minimum is not None else 0
            maximum = signal.maximum if signal.maximum is not None else 0
            receivers = ",".join(signal.receivers) if signal.receivers else "Vector__XXX"
            lines.append(
                " SG_ {name} : {start}|{length}@{endian}{sign} ({scale},{offset}) "
                "[{minimum}|{maximum}] \"{unit}\" {receivers}".format(
                    name=signal.name,
                    start=signal.start,
                    length=signal.length,
                    endian=endian,
                    sign=sign,
                    scale=_fmt(signal.scale),
                    offset=_fmt(signal.offset),
                    minimum=_fmt(minimum),
                    maximum=_fmt(maximum),
                    unit=signal.unit,
                    receivers=receivers,
                )
            )
        lines.append("")

    Path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _fmt(value: Union[float, int]) -> str:
    text = f"{value:.12g}"
    return text
