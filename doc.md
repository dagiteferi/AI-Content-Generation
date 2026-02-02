# AI Content Generation System Documentation

This document outlines the structure, capabilities, and usage of the AI Content Generation system, based on an exploration of its codebase.

## 1. Package Structure

The core application logic resides within the `src/ai_content/` directory, organized into several key modules:

*   **`cli/`**: Contains the command-line interface (CLI) for user interaction, allowing users to trigger content generation and manage jobs.
*   **`config/`**: Manages application settings and configurations, including provider API keys and other environment-dependent variables.
*   **`core/`**: Provides foundational components, base classes, and common utilities such as provider registration, job tracking, and result handling.
*   **`integrations/`**: Handles connections and interactions with external services, potentially for content archiving or publishing (e.g., `archive.py`, `media.py`, `youtube.py`).
*   **`pipelines/`**: Defines structured, end-to-end workflows for different types of content generation (e.g., music, video). These pipelines orchestrate the use of various providers, presets, and utilities.
*   **`presets/`**: Stores predefined templates and settings for various content types (music styles, video styles), simplifying content generation with common configurations.
*   **`providers/`**: Contains implementations for integrating with different AI content generation services. Each service typically has its own subdirectory.
*   **`utils/`**: Offers general-purpose utility functions, such as file handling, lyrics parsing, and retry mechanisms.

### Provider Organization

Providers are organized into subdirectories within `src/ai_content/providers/`, with each subdirectory representing a specific AI service. This modular structure facilitates easy integration, management, and extension of different AI content generation backends.

Current provider subdirectories include:
*   `aimlapi/`
*   `google/`
*   `kling/`

### Purpose of the `pipelines/` Directory

The `pipelines/` directory is crucial for defining and orchestrating the end-to-end workflows for generating AI content. It contains specialized pipeline classes (e.g., `music.py`, `video.py`) that outline the sequence of operations, leveraging various providers, presets, and utilities to produce the desired output. `base.py` likely provides a common interface or abstract class for these pipelines, ensuring consistency across different content generation workflows.

## 2. Provider Capabilities

The system integrates with several AI providers, each offering distinct capabilities for music and video generation.

### Music Providers Available

*   **Google Lyria (`lyria`)**:
    *   **Primary Use**: Instrumental music generation.
    *   **Workflow Focus**: Excellent for "performance-first" workflows, where the AI generates instrumental tracks first, allowing for subsequent lyric integration.
    *   **Vocals/Lyrics Support**: Primarily for instrumental tracks; does not explicitly support vocals/lyrics generation.

*   **AIMLAPI MiniMax (`minimax`)**:
    *   **Primary Use**: Music generation with strong capabilities for vocals and lyrics.
    *   **Workflow Focus**: Recommended for "lyrics-first" workflows, where structured lyrics are provided to guide music generation.
    *   **Additional Features**: Supports "reference-based" generation, allowing style transfer from a reference audio input.
    *   **Vocals/Lyrics Support**: Explicitly supports and is recommended for vocal/lyrics integration.

### Video Providers Available

*   **Google Veo (`veo`)**:
    *   **Primary Use**: General video generation.
    *   **Capabilities**: Supports both text-to-video (generating video from a text prompt) and image-to-video (animating a video from a keyframe image).
    *   **Default**: This is the default video provider in the system.

*   **Kling AI (`kling`)**:
    *   **Primary Use**: High-quality video generation.
    *   **Capabilities**: Supports both text-to-video and image-to-video generation.
    *   **Features**: Noted for "Highest quality video generation" and uses the "v2.1-master model." Generation times are typically 5-14 minutes.

### Which supports image-to-video?

Both **Google Veo (`veo`)** and **Kling AI (`kling`)** providers support image-to-video generation.

### Which provider supports vocals/lyrics?

**AIMLAPI MiniMax (`minimax`)** is the primary provider that explicitly supports and is recommended for vocals/lyrics integration in music generation.

## 3. Preset System

The system utilizes a preset system to simplify content generation by providing pre-configured styles and settings for music and video.

### Available Music Presets (with BPM and Mood)

| Preset Name     | BPM | Mood        |
| :-------------- | :-: | :---------- |
| `jazz`          | 95  | nostalgic   |
| `blues`         | 72  | soulful     |
| `ethiopian-jazz`| 85  | mystical    |
| `cinematic`     | 100 | epic        |
| `electronic`    | 128 | euphoric    |
| `ambient`       | 60  | peaceful    |
| `lofi`          | 85  | relaxed     |
| `rnb`           | 90  | sultry      |
| `salsa`         | 180 | fiery       |
| `bachata`       | 130 | romantic    |
| `kizomba`       | 95  | sensual     |

### Available Video Presets (with Aspect Ratios)

| Preset Name | Aspect Ratio |
| :---------- | :----------- |
| `nature`    | "16:9"       |
| `urban`     | "21:9"       |
| `space`     | "16:9"       |
| `abstract`  | "1:1"        |
| `ocean`     | "16:9"       |
| `fantasy`   | "21:9"       |
| `portrait`  | "9:16"       |

### How to Add a New Preset

To add a new preset (for either music or video), follow these steps:

1.  **Define a new `dataclass` instance**:
    *   For music, create a new instance of `MusicPreset` in `src/ai_content/presets/music.py`.
    *   For video, create a new instance of `VideoPreset` in `src/ai_content/presets/video.py`.
    *   Populate the instance with the required attributes (`name`, `prompt`, `bpm`/`aspect_ratio`, `mood`/`duration`, `tags`/`style_keywords`).

2.  **Add to the `_PRESETS` dictionary**:
    *   Include the newly created preset instance in the `MUSIC_PRESETS` dictionary (for music) or `VIDEO_PRESETS` dictionary (for video) within the same file. This action registers the preset with the system, making it available for use.

## 4. CLI Commands

The command-line interface provides various commands for interacting with the AI content generation system.

### Available Commands

*   **`music`**: Generates music content using AI providers.
*   **`video`**: Generates video content using AI providers.
*   **`list-providers`**: Displays a list of all registered music, video, and image providers.
*   **`list-presets`**: Shows all available music and video presets, including their key characteristics (BPM/mood for music, aspect ratio for video).
*   **`music-status [GENERATION_ID]`**: Checks the generation status of a specific music job (primarily for MiniMax) and allows optional downloading of completed audio.
*   **`jobs`**: Lists all tracked content generation jobs, with options to filter by status or provider.
*   **`jobs-stats`**: Provides a summary of job statistics, including total jobs, jobs by status, by provider, and by content type.
*   **`jobs-sync`**: Synchronizes the status of pending jobs with the respective AI provider APIs, optionally downloading completed files.

### Global Options

These options can be used with any command:

*   **`--verbose` or `-v`**: Enables debug logging for more detailed output.
*   **`--config` or `-c`**: Specifies a custom configuration file path to override default settings.

### `music` Command Options

*   **`--prompt` or `-p` (required)**: A text prompt describing the desired music style or content.
*   **`--provider` (default: `lyria`)**: Specifies the AI provider to use for music generation. Available options include `lyria` and `minimax`.
*   **`--style` or `-s`**: Applies a predefined music preset by name (e.g., `jazz`, `cinematic`). If used, it overrides the `--prompt` and `--bpm` options with preset values.
*   **`--duration` or `-d` (default: `30`)**: Sets the desired duration of the generated music in seconds.
*   **`--bpm` (default: `120`)**: Sets the beats per minute for the generated music.
*   **`--lyrics` or `-l`**: Provides a path to a text file containing lyrics to be used in music generation (best with `minimax`).
*   **`--reference-url` or `-r`**: A URL to a reference audio file for style transfer (primarily supported by `minimax`).
*   **`--output` or `-o`**: Specifies the file path where the generated music should be saved.
*   **`--force` or `-f`**: Forces the generation process even if a duplicate job (with the same parameters) is detected.

### `video` Command Options

*   **`--prompt` or `-p` (required)**: A text prompt describing the desired video scene or content.
*   **`--provider` (default: `veo`)**: Specifies the AI provider to use for video generation. Available options include `veo` and `kling`.
*   **`--style` or `-s`**: Applies a predefined video preset by name (e.g., `nature`, `urban`). If used, it overrides the `--prompt` and `--aspect` options with preset values.
*   **`--aspect` or `-a` (default: `16:9`)**: Sets the aspect ratio for the generated video.
*   **`--duration` or `-d` (default: `5`)**: Sets the desired duration of the generated video in seconds.
*   **`--image` or `-i`**: Provides a path to an image file to be used as the first frame for image-to-video generation. (Note: The current implementation requires an image URL, implying local files need to be uploaded first).
*   **`--output` or `-o`**: Specifies the file path where the generated video should be saved.
