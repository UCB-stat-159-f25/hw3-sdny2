from ligotools import readligo as rl
import json
from pathlib import Path

def test_loaddata():
    root = Path(__file__).resolve().parents[2]
    fnjson = root / "data" / "BBH_events_v3.json"
    with open(fnjson, "r") as f:
        events = json.load(f)
    event = events["GW150914"]
    fn_H1 = root / "data" / event["fn_H1"]

    strain, time, chan_dict = rl.loaddata(str(fn_H1), "H1")

    # Actual Validation
    assert len(strain) == len(time), "The lengths of strain and time do not match."
    assert isinstance(chan_dict, dict), "chan_dict is not a dictionary."
    assert "DATA" in chan_dict, "'DATA' channel is missing in channel_dict."


def test_dq_channel_to_seglist():
    root = Path(__file__).resolve().parents[2]
    fnjson = root / "data" / "BBH_events_v3.json"
    with open(fnjson, "r") as f:
        events = json.load(f)
    event = events["GW150914"]

    fn_L1 = root / "data" / event["fn_L1"]
    strain, time, chan_dict = rl.loaddata(str(fn_L1), "L1")
    seglist = rl.dq_channel_to_seglist(chan_dict["BURST_CAT3"])

    # Verify that valid segments exist
    assert len(seglist) > 0, "No segments returned from dq_channel_to_seglist."

    # Check that all elements are slice objects
    assert all(isinstance(s, slice) for s in seglist), "Returned segments are not slice objects"

    # Inspect the first segment
    first_seg = seglist[0]
    seg_strain = strain[first_seg]
    seg_time = time[first_seg]

    # Check segment size and time range roughly match event window
    assert 130000 < len(seg_strain) < 132000, "Unexpected segment length"
    assert 1126259446.0 <= seg_time[0] <= 1126259447.0, "Segment start time off"
    assert 1126259477.9 <= seg_time[-1] <= 1126259478.0, "Segment end time off"

