import ligotools.utils as ul
import numpy as np
from pathlib import Path
import os


def test_whiten():
    dt = 1.0 / 4096
    t = np.linspace(0, 1, 4096)
    strain = np.sin(2 * np.pi * 50 * t)
    interp_psd = lambda f: np.ones_like(f)

    whitened = ul.whiten(strain, interp_psd, dt)

    assert isinstance(whitened, np.ndarray), "Output is not a numpy array"
    assert whitened.shape == strain.shape, "Output shape differs from input"
    assert np.isfinite(whitened).all(), "Whitened output contains NaN or Inf"
    assert not np.allclose(whitened, 0), "Whitened output is entirely zero"


def test_write_wavfile():
    fs = 4096
    filename = Path("audio/test_output.wav")
    filename.parent.mkdir(exist_ok=True)
    if filename.exists():  
        os.remove(filename)

    data = np.random.randn(fs)
    ul.write_wavfile(filename, fs, data)

    assert filename.exists(), "WAV file was not created"
    os.remove(filename)