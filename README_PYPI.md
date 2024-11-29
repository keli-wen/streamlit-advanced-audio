# Streamlit Advanced Audio - EN

## Features

While the original `audio` component in Streamlit provides basic audio playback functionality, it lacks advanced features such as style customization and current playback time tracking.

The `audix` component (`audix` means `audio` + `extra`), built with `react`, `wavesurfer.js`, and `ant design`, offers the following features:

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

Pull requests for further improvements are welcome!

## Acknowledgments

This project builds upon several excellent open-source solutions:

- [Streamlit](https://streamlit.io/) for their amazing platform
- [Gradio](https://www.gradio.app/) for inspiration in ML application development
- [Streamlit Component Template](https://github.com/streamlit/component-template) for the component development framework
- [wavesurfer.js](https://wavesurfer-js.org/) for audio waveform visualization
- [wavesurfer Region Plugin](https://wavesurfer.xyz/plugins/regions) for region selection and trimming
- [Ant Design](https://ant.design/) for UI components and dark mode support

# Streamlit Advanced Audio - CN

## 功能与特性

原始 streamlit 中的 `audio` 组件提供了基本的音频播放功能，但是缺乏一些高级的特性，比如缺乏样式定制，无法获取当前播放的时间等。

`audix` 组件基于 `react`，`wavesurfer.js` 和 `ant design` 开发，提供了如下的功能：

- [x] 基本完全兼容了原始 `streamlit.audio` 组件的 API。
- [x] 支持获取当前播放的时间，用于快捷的实现音频切分裁剪等功能。
  - 当前播放时间（`currentTime`）
  - 选中区域信息（`selectedRegion`）
- [x] 使用了更现代的样式，支持黑暗模式也支持高度自定义样式（颜色大小等）。
  - 波形颜色
  - 进度条颜色
  - 波形高度
  - 条形宽度和间距
  - 光标样式
- [x] 支持了音频区间的设定，可以快速获取音频的区间起始时间。
  
目前可能存在的不足之处：

- [ ] 对于 url 的处理比较粗糙，会先下载到本地再播放。
- [ ] 裁剪功能仅停留在实验阶段，需要在 python 端基于返回值进行裁剪。

## 安装与使用

从本地安装：

```bash
git clone https://github.com/keli-wen/streamlit-advanced-audio
cd streamlit-advanced-audio
pip install -e .
```

从 PyPI 安装：

```bash
pip install streamlit-advanced-audio
```

## 基础使用示例

1. 基本播放功能：

```python
from streamlit_advanced_audio import audix

# 播放本地文件
audix("path/to/your/audio/file.wav")

# 播放URL音频
audix("https://example.com/audio.mp3")

# 播放NumPy数组
import numpy as np
sample_rate = 44100
audio_array = np.sin(2 * np.pi * 440 * np.linspace(0, 1, sample_rate))
audix(audio_array, sample_rate=sample_rate)
```

2. 自定义波形样式：

```python
from streamlit_advanced_audio import audix, WaveSurferOptions

options = WaveSurferOptions(
    wave_color="#2B88D9",      # 波形颜色
    progress_color="#b91d47",  # 进度条颜色
    height=100,               # 波形高度
    bar_width=2,             # 条形宽度
    bar_gap=1                # 条形间距
)

result = audix(
    "audio.wav",
    wavesurfer_options=options
)

# 获取播放状态
if result:
    current_time = result["currentTime"]
    selected_region = result["selectedRegion"]
    st.write(f"当前播放时间: {current_time}秒")
    if selected_region:
        st.write(f"选中区域: {selected_region['start']} - {selected_region['end']}秒")
```

3. 设置播放区间和循环：

```python
audix(
    "audio.wav",
    start_time="1s",     # 支持多种时间格式
    end_time="5s",
    loop=True,           # 循环播放
    autoplay=False       # 自动播放
)
```

## 进一步开发

本代码基于 [Streamlit Component Templates](https://github.com/streamlit/component-template) 开发。

具体可以参考关键的章节 [Quickstart](https://github.com/streamlit/component-template?tab=readme-ov-file#quickstart)。

如果你有进一步的优化建议，欢迎提交 PR。

## 感谢

本项目的使用基于许多优秀的开源方案，在此特别感谢：

- [Streamlit](https://streamlit.io/) 提供了如此伟大的产品。
- [Gradio](https://www.gradio.app/) 同样提供了优秀的 ML 应用开发体验。
- [Streamlit Component Template](https://github.com/streamlit/component-template) 快捷的组件开发模板。
- [wavesurfer.js](https://wavesurfer-js.org/) 用于音频波形图的绘制。
- [wavesurfer Region Plugin](https://wavesurfer.xyz/plugins/regions) 用于区间绘制和裁剪。
- [Ant Design](https://ant.design/) 用于 UI 组件和黑暗模式。
