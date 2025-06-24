import base64
import io
import os
from dataclasses import asdict, dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd
import requests
import soundfile as sf
import streamlit as st
import streamlit.components.v1 as components
from streamlit import url_util

MediaData = Union[str, bytes, io.BytesIO, np.ndarray, io.FileIO]


@dataclass
class WaveSurferOptions:
    """WaveSurfer visualization options.

    All parameters are optional and will use WaveSurfer's defaults if not specified.

    Attributes:
        wave_color (str): The color of the waveform.
            (e.g., "#999", "rgb(200, 200, 200)")
        progress_color (str): The color of the progress mask.
            (e.g., "#555", "rgb(100, 100, 100)")
        height (Union[int, str]): The height of the waveform in pixels,
            or "auto" to fill container.
        bar_width (int): Width of the bars in pixels when using bar visualization.
        bar_gap (int): Gap between bars in pixels.
        bar_radius (int): Rounded borders radius for bars.
        bar_height (float): Vertical scaling factor for the waveform.
        cursor_color (str): The color of the playback cursor.
            (e.g., "#333", "rgb(50, 50, 50)")
        cursor_width (int): Width of the playback cursor in pixels.
        hide_scrollbar (bool): Whether to hide the horizontal scrollbar.
        normalize (bool): Stretch the waveform to the full height.
    """

    wave_color: str = "rgb(200, 200, 200)"
    progress_color: str = "rgb(100, 100, 100)"
    height: Union[int, str] = 60
    bar_width: int = 3
    bar_gap: int = 1
    bar_radius: int = 2
    bar_height: float = 1.0
    cursor_color: str = "#333"
    cursor_width: int = 2
    hide_scrollbar: bool = False
    normalize: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert options to a dictionary, excluding None values and converting to camelCase."""
        name_mapping = {
            "wave_color": "waveColor",
            "progress_color": "progressColor",
            "bar_width": "barWidth",
            "bar_gap": "barGap",
            "bar_radius": "barRadius",
            "bar_height": "barHeight",
            "cursor_color": "cursorColor",
            "cursor_width": "cursorWidth",
            "hide_scrollbar": "hideScrollbar",
            "normalize": "normalize",
        }

        return {
            name_mapping.get(key, key): value
            for key, value in asdict(self).items()
            if value is not None
        }


@dataclass
class RegionColorOptions:
    """Region color options.

    Attributes:
        interactive_region_color (str): The color of the interactive region.
            **interactive** means the region add by button.
        start_to_end_mask_region_color (str): The color of the start to end
            mask region.
    """

    interactive_region_color: str = "rgba(160, 211, 251, 0.4)"
    start_to_end_mask_region_color: str = "rgba(160, 211, 251, 0.4)"

    def to_dict(self) -> Dict[str, Any]:
        """Convert options to a dictionary."""
        return asdict(self)


@dataclass
class CustomizedRegion:
    """Customized region.

    Attributes:
        start (float): The start time of the region.
        end (float): The end time of the region.
        color (str): The color of the region.
    """

    start: float
    end: float
    color: str = "rgba(160, 211, 251, 0.4)"

    def to_dict(self) -> Dict[str, Any]:
        """Convert options to a dictionary."""
        return asdict(self)


# Create a _RELEASE constant. We'll set this to False while we're developing
# and True when we're ready to package and distribute our component.
_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "audix",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("audix", path=build_dir)


# Cache the conversion function to improve performance.
# For same audio data, the conversion function
# will not be called multiple times.
@st.cache_data
def _convert_to_base64(audio_data: Optional[MediaData], sample_rate: Optional[int] = None) -> Optional[str]:
    """Convert different types of audio data to base64 string.

    Parameters:
    ----------
    audio_data : Optional[MediaData]
        Audio data, can be:
        - File path (str or pathlib.Path)
        - URL (str)
        - Raw audio data (bytes, BytesIO)
        - Numpy array (numpy.ndarray)
        - File object
    sample_rate : Optional[int]
        Sample rate when data is a numpy array. Defaults to 16000 if not provided.

    Returns:
    -------
    Optional[str]
        Base64 encoded audio data string or None if conversion fails.

    Raises:
    ------
    ValueError
        If audio data is None.
    """
    if audio_data is None:
        raise ValueError("Audio data cannot be None")

    if isinstance(audio_data, (str, Path)):
        # If it's a file path.
        audio_data = str(audio_data)
        if os.path.exists(audio_data):
            with open(audio_data, "rb") as f:
                audio_bytes = f.read()
                audio_base64 = base64.b64encode(audio_bytes).decode()
                ext = os.path.splitext(audio_data)[1].lower()
                mime_type = {
                    ".wav": "audio/wav",
                    ".mp3": "audio/mpeg",
                    ".ogg": "audio/ogg",
                }.get(ext, "audio/wav")
                return f"data:{mime_type};base64,{audio_base64}"
        elif url_util.is_url(
            audio_data, allowed_schemas=("http", "https", "data")
        ):
            # Try to download the audio from the URL.
            response = requests.get(audio_data)
            if response.status_code == 200:
                audio_bytes = response.content
                audio_base64 = base64.b64encode(audio_bytes).decode()
                return f"data:audio/wav;base64,{audio_base64}"
            else:
                # Fail a error.
                st.error(f"Failed to download audio from URL: {audio_data}")

        # If the audio already is a base64 string, return it as is.
        return audio_data

    elif isinstance(audio_data, np.ndarray):
        # If it's a numpy array, convert it to WAV format.
        buffer = io.BytesIO()
        # Use provided sample_rate or default to 16000
        sr = sample_rate if sample_rate is not None else 16000
        sf.write(buffer, audio_data, samplerate=sr, format="WAV")
        buffer.seek(0)
        audio_base64 = base64.b64encode(buffer.read()).decode()
        return f"data:audio/wav;base64,{audio_base64}"

    elif isinstance(audio_data, (bytes, bytearray)):
        # If it's a bytes or bytearray object.
        audio_base64 = base64.b64encode(audio_data).decode()
        return f"data:audio/wav;base64,{audio_base64}"

    elif isinstance(audio_data, io.BytesIO):
        # If it's a BytesIO object.
        audio_data.seek(0)
        audio_base64 = base64.b64encode(audio_data.read()).decode()
        return f"data:audio/wav;base64,{audio_base64}"

    elif isinstance(audio_data, (io.RawIOBase, io.BufferedReader)):
        # If it's a file object.
        audio_base64 = base64.b64encode(audio_data.read()).decode()
        # Try to get the MIME type from the file name.
        if hasattr(audio_data, "name"):
            ext = os.path.splitext(audio_data.name)[1].lower()
            mime_type = {
                ".wav": "audio/wav",
                ".mp3": "audio/mpeg",
                ".ogg": "audio/ogg",
            }.get(ext, "audio/wav")
        else:
            mime_type = "audio/wav"
        return f"data:{mime_type};base64,{audio_base64}"

    else:
        st.error(f"Unsupported audio data type: {type(audio_data)}")
        return None


# Parse the time parameters.
def _parse_time(
    time_value: Optional[Union[int, float, str, timedelta]],
) -> Optional[float]:
    """Parse the time parameters.

    Parameters:
    ----------
    time_value : Optional[Union[int, float, str, timedelta]]
        Time value, can be:
        - Number of seconds (int, float)
        - Time string (e.g., "2 minute", "20s")
        - timedelta object

    Returns:
    -------
    Optional[float]
        Time value in seconds or None if the input is None.
    """
    if time_value is None:
        return None
    if isinstance(time_value, (int, float)):
        return float(time_value)
    if isinstance(time_value, str):
        return float(pd.Timedelta(time_value).total_seconds())
    if isinstance(time_value, timedelta):
        return float(time_value.total_seconds())


def audix(
    data: Optional[MediaData],
    format: str = "audio/wav",
    start_time: Union[int, float, timedelta, str, None] = 0,
    sample_rate: Optional[int] = None,
    end_time: Union[int, float, timedelta, str, None] = None,
    loop: bool = False,
    autoplay: bool = False,
    mask_start_to_end: bool = False,
    wavesurfer_options: WaveSurferOptions = WaveSurferOptions(),
    region_color_options: RegionColorOptions = RegionColorOptions(),
    customized_regions: List[CustomizedRegion] = [],
    key: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Advanced audio player component. `audix` means `audio` + `extra`.

    Parameters:
    ----------
    data : Union[str, bytes, BytesIO, numpy.ndarray, file]
        Audio data, can be:
        - File path (str)
        - URL (str)
        - Raw audio data (bytes, BytesIO)
        - Numpy array (numpy.ndarray)
        - File object
    format : str
        The mime type for the audio file. Defaults to `"audio/wav"`.
        See https://tools.ietf.org/html/rfc4281 for more info.
    start_time : Union[int, float, timedelta, str, None]
        Start time of the audio, supports:
        - Number of seconds (int, float)
        - Time string (e.g., "2 minute", "20s")
        - timedelta object
    sample_rate : Optional[int]
        Sample rate when data is a numpy array.
    end_time : Union[int, float, timedelta, str, None]
        End time of the audio, format same as start_time.
    loop : bool
        Whether to loop the audio.
    autoplay : bool
        Whether to autoplay the audio.
    mask_start_to_end : bool
        Whether to mask (add a region) the audio between
            `start_time` and `end_time`.
    wavesurfer_options : WaveSurferOptions
        WaveSurfer options to customize the waveform style.
    region_color_options : RegionColorOptions
        Region color options to customize the region style.
    customized_regions : List[CustomizedRegion]
        Customized regions to add to the waveform.
    key : Optional[str]
        Streamlit component instance key

    Returns:
    -------
    dict or None
        Dictionary containing playback status information:
        {
            "currentTime": float,
            "selectedRegion": Optional[dict[str, float]]
            "isPlaying": bool,
        }

    Raises:
    ------
    ValueError
        If start time is greater than or equal to end time.

    Examples:
    --------
    >>> result = audix(data="path/to/audio.mp3", loop=True, autoplay=True)
    >>> print(result)
    { "currentTime": 10.0, "selectedRegion": {"start": 10.0, "end": 20.0}, "isPlaying": True }
    """
    start_seconds = _parse_time(start_time) or 0
    end_seconds = _parse_time(end_time)

    if end_seconds is not None and start_seconds >= end_seconds:
        raise ValueError(
            "Start time cannot be greater than or equal to end time"
        )

    try:
        # Convert the audio data to base64, passing sample_rate parameter
        audio_url = _convert_to_base64(data, sample_rate)

        # Pass the configuration to the frontend component.
        component_value = _component_func(
            audio_url=audio_url,
            format=format,
            start_time=start_seconds,
            end_time=end_seconds,
            loop=loop,
            autoplay=autoplay,
            sample_rate=sample_rate,
            mask_start_to_end=mask_start_to_end,
            wavesurfer_options=wavesurfer_options.to_dict(),
            region_color_options=region_color_options.to_dict(),
            customized_regions=[
                region.to_dict() for region in customized_regions
            ],
            key=key,
        )

        return component_value

    except Exception as e:
        st.error(f"Error processing audio data: {str(e)}")
        return None
