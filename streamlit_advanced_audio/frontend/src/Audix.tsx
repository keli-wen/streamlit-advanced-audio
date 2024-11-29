import {
  Button,
  Select,
  Slider,
  Typography,
  ConfigProvider,
  theme,
} from 'antd';
import {
  PlayCircleOutlined,
  PauseCircleOutlined,
  DownloadOutlined,
  SoundOutlined,
  ScissorOutlined,
  UndoOutlined,
  CheckOutlined,
  CloseOutlined,
} from '@ant-design/icons';
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from 'streamlit-component-lib';
import React, { ReactNode } from 'react';
import WaveSurfer from 'wavesurfer.js';
import RegionsPlugin from 'wavesurfer.js/dist/plugins/regions';

interface State {
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  playbackRate: number;
  selectedRegion: { start: number; end: number } | null;
  isFocused: boolean;
  showRegionControls: boolean;
  isRegionPlaying: boolean;
  hasModifications: boolean;
}

class AudioPlayer extends StreamlitComponentBase<State> {
  private isDarkMode = false;
  private wavesurfer: WaveSurfer | null = null;
  private regionsPlugin: RegionsPlugin | null = null;
  private containerRef = React.createRef<HTMLDivElement>();

  public state: State = {
    isPlaying: false,
    currentTime: 0,
    duration: 0,
    playbackRate: 1,
    selectedRegion: null,
    isFocused: false,
    showRegionControls: false,
    isRegionPlaying: false,
    hasModifications: false,
  };

  componentDidMount() {
    this.initWavesurfer();
  }

  componentWillUnmount() {
    if (this.wavesurfer) {
      this.wavesurfer.destroy();
    }
  }

  private initWavesurfer = () => {
    if (!this.containerRef.current) {
      console.error('Container ref is null');
      return;
    }

    // Get the container width.
    const containerWidth = this.containerRef.current.clientWidth;

    // Calculate the duration of the audio file before creating the WaveSurfer instance.
    const audio = new Audio(this.props.args.audio_url);
    audio.addEventListener('loadedmetadata', () => {
      const duration = audio.duration;

      // Calculate suitable minPxPerSec
      const targetWidth = containerWidth * 0.9;
      const calculatedMinPxPerSec = targetWidth / duration;
      const minPxPerSec = Math.max(Math.min(calculatedMinPxPerSec, 50), 1);

      // Merge default options with provided wavesurfer_options.
      const wavesurferOptions = {
        container: this.containerRef.current!,
        waveColor: 'rgb(200, 200, 200)',
        progressColor: 'rgb(100, 100, 100)',
        height: 60,
        minPxPerSec: minPxPerSec,
        barWidth: 3,
        barGap: 1,
        barRadius: 2,
        normalize: true,
        dragToSeek: true,
        interact: true,
        plugins: [RegionsPlugin.create()],
        cursorColor: '#333',
        cursorWidth: 2,
        hideScrollbar: false,
        autoplay: this.props.args.autoplay,
        fillParent: true,
        autoScroll: true,
        autoCenter: true,
        ...this.props.args.wavesurfer_options, // Merge provided options
      };

      this.wavesurfer = WaveSurfer.create(wavesurferOptions);

      // Register RegionsPlugin.
      this.regionsPlugin = this.wavesurfer.registerPlugin(
        RegionsPlugin.create()
      );

      this.wavesurfer.load(this.props.args.audio_url);

      this.wavesurfer.on('finish', () => {
        if (this.props.args.loop) {
          // If start time is set, play from start time.
          if (this.props.args.start_time > 0) {
            this.wavesurfer!.setTime(this.props.args.start_time);
          } else {
            // Otherwise, play from the beginning.
            this.wavesurfer!.setTime(0);
          }
          this.wavesurfer!.play();
        } else {
          this.setState({ isPlaying: false });
        }
      });

      this.wavesurfer.on('ready', () => {
        if (this.props.args.start_time > 0) {
          this.wavesurfer!.setTime(this.props.args.start_time);
        }

        if (this.props.args.end_time !== null) {
          this.wavesurfer!.on('audioprocess', () => {
            const currentTime = this.wavesurfer!.getCurrentTime();
            if (currentTime >= this.props.args.end_time!) {
              this.wavesurfer!.pause();
              if (this.props.args.loop) {
                this.wavesurfer!.setTime(this.props.args.start_time);
                this.wavesurfer!.play();
              }
            }
          });
        }

        this.setState({ duration: this.wavesurfer!.getDuration() });
      });

      // Handle the error event.
      this.wavesurfer.on('error', (err) => {
        console.error('WaveSurfer error:', err);
      });

      // Handle the audio processing event.
      this.wavesurfer.on('audioprocess', () => {
        this.setState({ currentTime: this.wavesurfer!.getCurrentTime() });
        if (this.state.selectedRegion) {
          const currentTime = this.wavesurfer!.getCurrentTime();
          if (
            currentTime < this.state.selectedRegion.start ||
            currentTime >= this.state.selectedRegion.end
          ) {
            this.wavesurfer!.setTime(this.state.selectedRegion.start);
          }

          // If arriving at the end of the region.
          if (currentTime >= this.state.selectedRegion.end) {
            if (this.props.args.loop) {
              // If loop is enabled, set the time to the start of the region.
              this.wavesurfer!.setTime(this.state.selectedRegion.start);
            } else {
              // Otherwise, pause the audio.
              this.wavesurfer!.pause();
              this.setState({ isPlaying: false });
            }
          }
        }
      });

      // Handle seeking (dragging the playhead) in the audio.
      this.wavesurfer.on('seeking', () => {
        this.setState({ currentTime: this.wavesurfer!.getCurrentTime() });
        Streamlit.setComponentValue({
          currentTime: this.wavesurfer!.getCurrentTime(),
          selectedRegion: this.state.selectedRegion,
        });
      });
    });
  };

  private handlePlayPause = () => {
    if (this.wavesurfer) {
      if (this.state.selectedRegion) {
        const currentTime = this.wavesurfer.getCurrentTime();
        // If region exists, play only within region.
        if (!this.state.isPlaying) {
          // Out of the region, set the time to the start of the region.
          if (
            currentTime < this.state.selectedRegion.start ||
            currentTime >= this.state.selectedRegion.end
          ) {
            this.wavesurfer.setTime(this.state.selectedRegion.start);
          }
          this.wavesurfer.play();
        } else {
          this.wavesurfer.pause();
        }
      } else {
        // Normal play/pause behavior.
        this.wavesurfer.playPause();
      }
      this.setState((prevState) => ({ isPlaying: !prevState.isPlaying }));
      Streamlit.setComponentValue({
        currentTime: this.wavesurfer!.getCurrentTime(),
        selectedRegion: this.state.selectedRegion,
      });
    }
  };

  private handleSpeedChange = (speed: number) => {
    if (this.wavesurfer) {
      this.wavesurfer.setPlaybackRate(speed);
      this.setState({ playbackRate: speed });
    }
  };

  private handleDownload = () => {
    const audioUrl = this.props.args.audio_url;
    const link = document.createElement('a');
    link.href = audioUrl;
    link.download = 'audio.mp3';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  private handleCreateRegion = () => {
    if (this.wavesurfer && this.regionsPlugin) {
      // Clear existing regions.
      this.regionsPlugin.clearRegions();

      const currentTime = this.wavesurfer.getCurrentTime();
      const duration = this.wavesurfer.getDuration();
      const minStart = this.props.args.start_time || 0;
      const maxEnd = this.props.args.end_time || duration;

      // Ensure initial position is within allowed range.
      const validStart = Math.max(currentTime, minStart);
      const regionEnd = Math.min(validStart + 0.2 * duration, maxEnd);

      const region = this.regionsPlugin.addRegion({
        start: validStart,
        end: regionEnd,
        color: 'rgba(160, 211, 251, 0.4)',
        drag: true,
        resize: true,
      });

      // Limit the drag and resize range.
      region.on('update', () => {
        let newStart = region.start;
        let newEnd = region.end;

        // Limit to valid range.
        if (newStart < minStart) newStart = minStart;
        if (newEnd > maxEnd) newEnd = maxEnd;

        // Only update if the values really need to be adjusted.
        if (newStart !== region.start || newEnd !== region.end) {
          region.setOptions({
            start: newStart,
            end: newEnd,
          });
        }

        this.setState({
          selectedRegion: {
            start: newStart,
            end: newEnd,
          },
        });
      });

      // Initial state update.
      this.setState({
        selectedRegion: {
          start: validStart,
          end: regionEnd,
        },
        showRegionControls: true,
      });
    }
  };

  private handleTrimAudio = () => {
    if (this.state.selectedRegion) {
      this.setState({ showRegionControls: false, hasModifications: true });
      // Send region data to Streamlit.
      Streamlit.setComponentValue({
        currentTime: this.wavesurfer!.getCurrentTime(),
        selectedRegion: this.state.selectedRegion,
      });
    }
  };

  private handleResetAudio = () => {
    if (this.wavesurfer) {
      this.regionsPlugin?.clearRegions();
      this.setState({
        selectedRegion: null,
        showRegionControls: false,
        hasModifications: false,
      });
      Streamlit.setComponentValue({
        currentTime: this.wavesurfer!.getCurrentTime(),
        selectedRegion: this.state.selectedRegion,
      });
    }
  };

  // The region controls are only shown when a region is selected.
  private renderRegionControls = () => {
    if (!this.state.showRegionControls) return null;

    return (
      <div className="flex space-x-2">
        <Button
          icon={<CheckOutlined />}
          type="primary"
          onClick={this.handleTrimAudio}
        />
        <Button
          icon={<CloseOutlined />}
          onClick={() => {
            this.regionsPlugin?.clearRegions();
            this.setState({
              selectedRegion: null,
              showRegionControls: false,
            });
          }}
        />
      </div>
    );
  };

  public render = (): ReactNode => {
    const { Option } = Select;
    const { Text } = Typography;
    this.isDarkMode = this.props.theme?.base === 'dark';

    return (
      // Support light and dark themes.
      <ConfigProvider
        theme={{
          algorithm: this.isDarkMode
            ? theme.darkAlgorithm
            : theme.defaultAlgorithm,
          token: {
            colorPrimary: '#3b82f6',
            borderRadius: 6,
          },
        }}
      >
        <div className="w-full space-y-5 p-4 rounded-lg">
          {/* Top controls */}
          <div className="flex justify-between items-center">
            {/* Left controls */}
            <div className="flex items-center space-x-4">
              <Select
                value={this.state.playbackRate}
                className="w-20"
                onChange={this.handleSpeedChange}
              >
                <Option value={0.5}>0.5x</Option>
                <Option value={0.75}>0.75x</Option>
                <Option value={1}>1x</Option>
                <Option value={1.5}>1.5x</Option>
                <Option value={2}>2x</Option>
                <Option value={3}>3x</Option>
              </Select>

              <div className="flex items-center space-x-2">
                <SoundOutlined />
                <Slider
                  className="w-16"
                  defaultValue={100}
                  onChange={(value) => {
                    if (this.wavesurfer) {
                      this.wavesurfer.setVolume(value / 100);
                    }
                  }}
                />
              </div>
            </div>

            {/* Right buttons */}
            <div className="flex space-x-3">
              <Button
                icon={<ScissorOutlined />}
                onClick={this.handleCreateRegion}
                disabled={this.state.showRegionControls}
              />
              <Button
                icon={<DownloadOutlined />}
                onClick={this.handleDownload}
              />
            </div>
          </div>

          {/* 波形图容器 */}
          <div
            ref={this.containerRef}
            className="cursor-pointer hover:opacity-90 transition-all duration-200"
          />

          {/* 底部控制栏 */}
          <div className="flex items-center space-x-4">
            <Button
              type="text"
              size="large"
              icon={
                this.state.isPlaying ? (
                  <PauseCircleOutlined />
                ) : (
                  <PlayCircleOutlined />
                )
              }
              onClick={this.handlePlayPause}
            />

            {/* Mono font for stable width. */}
            <div className="flex items-center space-x-1">
              <Text className="text-sm font-medium font-mono">
                {this.state.currentTime.toFixed(2)}
              </Text>
              <Text className="text-sm opacity-60">/</Text>
              <Text className="text-sm opacity-60 font-mono">
                {this.state.duration.toFixed(2)}
              </Text>
              <Text className="text-sm opacity-60">s</Text>
            </div>

            {/* Trim controls */}
            <div className="flex-1 flex justify-end space-x-2">
              {this.state.hasModifications && (
                <Button
                  onClick={this.handleResetAudio}
                  icon={<UndoOutlined />}
                />
              )}
              {this.renderRegionControls()}
            </div>
          </div>
        </div>
      </ConfigProvider>
    );
  };
}

export default withStreamlitConnection(AudioPlayer);
