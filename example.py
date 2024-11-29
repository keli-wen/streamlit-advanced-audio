import os

import numpy as np
import streamlit as st

from streamlit_advanced_audio import WaveSurferOptions, audix

st.title("Advanced Audio Player Demo (audix vs st.audio)")

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

# Display feature comparison
st.header("Feature Comparison")
st.markdown("""
| Feature | audix | st.audio |
|---------|-------|-----------|
| Waveform Visualization | ✅ | ❌ |
| Custom Time Range | ✅ | ❌ |
| Playback Status | ✅ | ❌ |
| Custom Appearance | ✅ | ❌ |
| Multiple Format Support | ✅ | ✅ |
| URL Support | ✅ | ✅ |
| File Upload | ✅ | ✅ |
""")

# Add some helpful documentation
st.header("Documentation")
with st.expander("Show WaveSurfer Options Documentation"):
    st.code("""
# Available WaveSurfer Options:
options = WaveSurferOptions(
    wave_color="rgb(200, 200, 200)",    # Waveform color
    progress_color="rgb(100, 100, 100)", # Progress color
    height=60,                           # Height in pixels
    bar_width=3,                         # Width of bars
    bar_gap=1,                           # Gap between bars
    bar_radius=2,                        # Bar corner radius
    bar_height=1.0,                      # Vertical scaling
    cursor_color="#333",                 # Playback cursor color
    cursor_width=2,                      # Cursor width
    hide_scrollbar=False,                # Hide scrollbar
    normalize=True                       # Normalize waveform
)
    """)
