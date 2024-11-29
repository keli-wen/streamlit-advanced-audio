# Streamlit Advanced Audio

![image](./assets/demo.gif)

[README_CN.md](./README_CN.md)

## Features

While the original `audio` component in Streamlit provides basic audio playback functionality, it lacks advanced features such as style customization and current playback time tracking.

The `audix` component, built with `react`, `wavesurfer.js`, and `ant design`, offers the following features:

> [!NOTE]
> `audix` means `audio` + `extra`

- [x] Full compatibility with the original `streamlit.audio` component API
- [x] Real-time playback information tracking for audio editing and trimming
  - Current playback time (`currentTime`)
  - Selected region information (`selectedRegion`)
- [x] Modern styling with dark mode support and extensive customization options
  - Waveform color
  - Progress bar color
  - Waveform height
  - Bar width and spacing
  - Cursor styling
- [x] Audio region selection support for quick interval selection and timing

Current limitations:

- [ ] Basic URL handling (downloads to local before playback)
- [ ] Experimental trimming feature (requires Python-side processing based on return values)

## More DEMOs

![image](./assets/image.png)

![image](./assets/image-region.png)

## Installation

Local installation:

```bash
git clone https://github.com/keli-wen/streamlit-advanced-audio
cd streamlit-advanced-audio
pip install -e .
```

PyPI installation:

```bash
pip install streamlit-advanced-audio
```

## Basic Usage

1. Basic playback:

```python
from streamlit_advanced_audio import audix

# Play local file
audix("path/to/your/audio/file.wav")

# Play from URL
audix("https://example.com/audio.mp3")

# Play NumPy array
import numpy as np
sample_rate = 44100
audio_array = np.sin(2 * np.pi * 440 * np.linspace(0, 1, sample_rate))
audix(audio_array, sample_rate=sample_rate)
```

2. Custom waveform styling:

```python
from streamlit_advanced_audio import audix, WaveSurferOptions

options = WaveSurferOptions(
    wave_color="#2B88D9",      # Waveform color
    progress_color="#b91d47",  # Progress bar color
    height=100,               # Waveform height
    bar_width=2,             # Bar width
    bar_gap=1                # Gap between bars
)

result = audix(
    "audio.wav",
    wavesurfer_options=options
)

# Get playback status
if result:
    current_time = result["currentTime"]
    selected_region = result["selectedRegion"]
    st.write(f"Current Time: {current_time}s")
    if selected_region:
        st.write(f"Selected Region: {selected_region['start']} - {selected_region['end']}s")
```

3. Set playback interval and looping:

```python
audix(
    "audio.wav",
    start_time="1s",     # Supports various time formats
    end_time="5s",
    loop=True,           # Enable looping
    autoplay=False       # Auto-play setting
)
```

## Development

This project is based on the [Streamlit Component Templates](https://github.com/streamlit/component-template).

For development details, please refer to the [Quickstart](https://github.com/streamlit/component-template?tab=readme-ov-file#quickstart) section.

> [!IMPORTANT]
> You can use the following command to build and **lint** the project:
> 
> ```bash
> cd streamlit-advanced-audio/frontend
> npm install
> npm run build
> cd ../../
> bash lint.sh # **For** py and tsx code lint.
> ```
>

Pull requests for further improvements are welcome!

## Acknowledgments

This project builds upon several excellent open-source solutions:

- [Streamlit](https://streamlit.io/) for their amazing platform
- [Gradio](https://www.gradio.app/) for inspiration in ML application development
- [Streamlit Component Template](https://github.com/streamlit/component-template) for the component development framework
- [wavesurfer.js](https://wavesurfer-js.org/) for audio waveform visualization
- [wavesurfer Region Plugin](https://wavesurfer.xyz/plugins/regions) for region selection and trimming
- [Ant Design](https://ant.design/) for UI components and dark mode support
