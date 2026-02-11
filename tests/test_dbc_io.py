from pathlib import Path

from dbcstudio.dbc_io import save_dbc
from dbcstudio.model import DbcDocument, MessageModel, SignalModel


def test_save_dbc_writes_basic_structure(tmp_path: Path) -> None:
    doc = DbcDocument(
        version="1.0",
        messages=[
            MessageModel(
                frame_id=0x123,
                name="VehicleStatus",
                length=8,
                senders=["Gateway"],
                signals=[
                    SignalModel(
                        name="Speed",
                        start=0,
                        length=16,
                        byte_order="little_endian",
                        is_signed=False,
                        scale=0.1,
                        offset=0.0,
                        minimum=0.0,
                        maximum=250.0,
                        unit="km/h",
                        receivers=["Cluster"],
                    )
                ],
            )
        ],
    )

    out = tmp_path / "out.dbc"
    save_dbc(doc, str(out))

    content = out.read_text(encoding="utf-8")
    assert 'VERSION "1.0"' in content
    assert "BO_ 291 VehicleStatus: 8 Gateway" in content
    assert 'SG_ Speed : 0|16@1+ (0.1,0) [0|250] "km/h" Cluster' in content
