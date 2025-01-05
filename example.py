import os

import numpy as np
import pandas as pd
import streamlit as st

from streamlit_advanced_audio import (
    CustomizedRegion,
    RegionColorOptions,
    WaveSurferOptions,
    audix,
)

st.title("Advanced Audio Player Demo (audix vs st.audio)")

# Display feature comparison
st.header("Feature Comparison")

st.dataframe(
    pd.DataFrame(
        {
            "Feature": [
                "Waveform Visualization",
                "Custom Time Range",
                "Playback Status",
                "Custom Appearance",
                "Multiple Format Support",
                "URL Support",
                "File Upload",
            ],
            "audix": ["✅", "✅", "✅", "✅", "✅", "✅", "✅"],
            "st.audio": ["❌", "❌", "❌", "❌", "✅", "✅", "✅"],
        }
    ),
    use_container_width=True,
    hide_index=True,
)

# 1. Local File Playback.
st.header("1. Local File Playback")
# Replace with your audio file path.
local_file = "path/to/your/audio.wav"
if os.path.exists(local_file):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("audix player")
        # Custom wavesurfer options
        options = WaveSurferOptions(
            wave_color="#2B88D9",
            progress_color="#b91d47",
            height=100,
            bar_width=2,
            bar_gap=1,
        )
        result1 = audix(
            data=local_file,
            start_time="1s",
            end_time="5s",
            loop=True,
            autoplay=False,
            wavesurfer_options=options,
        )
        if result1:
            st.write("Playback Info:", result1)

    with col2:
        st.subheader("st.audio player")
        st.audio(local_file)
else:
    st.info(f"File {local_file} does not exist.")

# 2. Numpy Array Playback (Synthesized Audio).
st.header("2. Synthesized Audio (Numpy Array)")
st.markdown("""
This example generates a simple audio signal - a combination of two sine waves
to demonstrate how to work with numpy arrays.
""")
st.markdown(
    "When you play/pause/drag the `audix` player, the current time will be :red[updated]."
)

# Generate a complex tone (440Hz + 880Hz).s
sample_rate = 44100
duration = 3  # seconds
t = np.linspace(0, duration, int(sample_rate * duration))

# Create a more complex sound with multiple frequencies and amplitude modulation
base_freq = 440
frequencies = [
    base_freq,
    base_freq * 2,
    base_freq * 3,
    base_freq * 5,
]  # Fundamental and harmonics
amplitudes = [0.5, 0.3, 0.2, 0.1]  # Decreasing amplitudes for harmonics

# Add amplitude modulation
mod_freq = 3  # 3 Hz modulation
envelope = 0.5 * (1 + np.sin(2 * np.pi * mod_freq * t))

# Combine all frequencies with amplitude modulation
audio_array = np.zeros_like(t)
for freq, amp in zip(frequencies, amplitudes):
    audio_array += amp * np.sin(2 * np.pi * freq * t)

# Apply the envelope and add some frequency modulation
audio_array *= envelope
audio_array += 0.2 * np.sin(
    2 * np.pi * (base_freq + 50 * np.sin(2 * np.pi * 2 * t)) * t
)

# Normalize to prevent clipping
audio_array = 0.7 * audio_array / np.max(np.abs(audio_array))

col3, col4 = st.columns(2)
with col3:
    st.subheader("audix player")
    result2 = audix(
        data=audio_array,
        sample_rate=sample_rate,
        wavesurfer_options=WaveSurferOptions(wave_color="#00b894", height=80),
    )
    with st.expander("Customized configuration"):
        st.code("""
options = WaveSurferOptions(
    wave_color="#00b894",
    height=80
)
        """)
    if result2:
        st.write("Playback Info:", result2)

with col4:
    st.subheader("st.audio player")
    st.audio(audio_array, sample_rate=sample_rate)

# 3. File Upload
st.header("3. File Upload Support")
uploaded_file = st.file_uploader(
    "Upload an audio file",
    type=["wav", "mp3", "ogg"],
    help="Supports WAV, MP3, and OGG formats",
)

if uploaded_file is not None:
    col5, col6 = st.columns(2)
    with col5:
        st.subheader("audix player")
        result3 = audix(
            uploaded_file,
            wavesurfer_options=WaveSurferOptions(
                wave_color="#e17055", cursor_color="#d63031"
            ),
        )
        if result3:
            st.write("Playback Info:", result3)

    with col6:
        st.subheader("st.audio player")
        st.audio(uploaded_file)

# 4. URL Audio
st.header("4. URL Audio Playback")
url = "https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav"
st.markdown(f"Source URL: `{url}`")

col7, col8 = st.columns(2)
with col7:
    st.subheader("audix player")
    result4 = audix(
        url,
        wavesurfer_options=WaveSurferOptions(
            wave_color="#6c5ce7", progress_color="#a29bfe", height=60
        ),
    )
    with st.expander("Customized configuration"):
        st.code("""
options = WaveSurferOptions(
    wave_color="#6c5ce7",
    progress_color="#a29bfe",
    height=60
)
        """)
    if result4:
        st.write("Playback Info:", result4)

with col8:
    st.subheader("st.audio player")
    st.audio(url)

# 5. Region customization
st.header("5. Region customization")
result5 = audix(
    audio_array,
    start_time=0.5,
    end_time=5.5,
    mask_start_to_end=True,
    wavesurfer_options=WaveSurferOptions(wave_color="#d17d5d", height=60),
    region_color_options=RegionColorOptions(
        start_to_end_mask_region_color="rgba(160, 211, 251, 0.3)",
    ),
    customized_regions=[
        CustomizedRegion(start=6, end=6.5, color="#00b89466"),
        CustomizedRegion(start=7, end=8, color="rgba(255, 255, 255, 0.6)"),
    ],
)

if result5:
    st.write("Playback Info:", result5)

st.code("""
result5 = audix(
    audio_array,
    start_time=0.5,
    end_time=5.5,
    mask_start_to_end=True,
    wavesurfer_options=WaveSurferOptions(
        wave_color="#d17d5d",
        height=60,
    ),
    region_color_options=RegionColorOptions(
        start_to_end_mask_region_color="rgba(160, 211, 251, 0.3)",
    ),
    customized_regions=[
        CustomizedRegion(start=6, end=6.5, color="#00b89466"),
        CustomizedRegion(start=7, end=8, color="rgba(255, 255, 255, 0.6)"),
    ],
)
""")


# Add some helpful documentation
st.header("Documentation")
with st.expander("Show WaveSurfer Options Documentation"):
    st.code("""
@dataclass
class WaveSurferOptions:
    \"\"\"WaveSurfer visualization options.

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
    \"\"\"

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
    """)


with st.expander("Show Region Color Options Documentation"):
    st.code("""
@dataclass
class RegionColorOptions:
    \"\"\"Region color options.

    Attributes:
        interactive_region_color (str): The color of the interactive region.
            **interactive** means the region add by button.
        start_to_end_mask_region_color (str): The color of the start to end
            mask region.
    \"\"\"

    interactive_region_color: str = "rgba(160, 211, 251, 0.4)"
    start_to_end_mask_region_color: str = "rgba(160, 211, 251, 0.4)"

    """)

with st.expander("Show Customized Region Documentation"):
    st.code("""
@dataclass
class CustomizedRegion:
    \"\"\"Customized region.

    Attributes:
        start (float): The start time of the region.
        end (float): The end time of the region.
        color (str): The color of the region.
    \"\"\"

    start: float
    end: float
    color: str = "rgba(160, 211, 251, 0.4)"
    """)
