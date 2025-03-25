# AI Home Assistant 🚀

Welcome to the **AI Home Assistant** project!  
This is a minimal yet powerful AI assistant designed for home use, built with neural network integration and customizable functionality.

---

## 🌟 Features

1. **Name Recognition**:  
   The assistant activates only when its name is called, ensuring a seamless and private experience.

2. **Neural Network Flexibility**:  
   Easily switch between different neural network models to tailor the assistant to your needs.

3. **Simple and Lightweight**:  
   A minimal implementation focused on core functionalities for maximum efficiency.

4. **Context Management**:  
   Ability to clear, create, restore, and switch communication contexts.

5. **Branch Handling**:  
   The assistant supports creating, selecting, and displaying different interaction branches.

6. **Speech and Text Recognition**:  
   Use of Vosk and Google Speech Recognizer for audio processing, as well as flexible handling of text commands.

7. **Integration with Text and Voice Commands**:  
   A full set of commands for controlling the assistant, available in both text and voice formats.

8. **Timer and Sound Management**:  
   Setting a timer, adjusting speech speed, and controlling sound playback.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- A microphone-enabled device

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NobidoNs/CustomAI.git
   cd CustomAI
   ```
2. Install dependencies:
   run dependencies.bat
   or
   pip install -r requirements.txt
   additionally for linux: sudo apt install ffmpeg
   additionally for mac install portaudio
3. Calibration:
   run ambient.bat
   or
   run ambient.py
   DO NOT make any SOUNDS for 5 seconds
4. Run Jarvis.bat or start.py file.
5. (optional) open output.md file for use text mode (--help).

## Example to use

say: "джарвис расскажи о себе"
or
text: info/examples

You can make jarvis swear when saying assigned words:
   1. open devolp_config.json 
   2. add words in "badWords"
example: "badWords": ["ну"],

To load in jarvis lot context

## 🛠️ How It Works

1. **Activation**:  
   The assistant listens for its name to start processing input.

2. **Speech Processing**:  
   Once activated, it uses **Google Speech Recognizer** to capture audio from the microphone and convert it into text.

3. **Request Handling**:  
   The transcribed text is sent to the selected neural network for further processing, enabling dynamic responses.

4. **Sound Playback**:
   Using gTTS(Google text to speech) and pygame mixer read request.

---

#### **List of Available Commands for Calling Scripts**

Scripts are defined in the `devolp_config.json` file under the `"scripts"` section. Each script has:

- **Name** — the key in the `"scripts"` object.
- **List of commands** — an array of strings that can be used to call the corresponding script.

Example from the `devolp_config.json` file:

```json
"scripts": {
    "Game": ["сценарий игра", "протокол игра", "игровой код", "игре быть"]
}
```

#### **Example of Usage**

. **Text Command:**
In the command line or via text input, send a command associated with the desired script. For example:

```
сценарий игра
```

After this, the `"Game"` script will be executed.

#### **How to Add a New Script**

To add a new custom script, follow these steps:

##### 1 **Define the new script in `devolp_config.json`:**

```json
"scripts": {
    "NewScript": ["command for the new script"]
}
```

##### 2 **Create NewScript.txt file in app/sysControl:**

paste your program paths in it.

Last simplest configuration: https://github.com/NobidoNs/CustomAI/commit/89e4294d76a01d9c8c6b4fd115cf91d5c99e1642

## 💡 Contribution

We welcome contributions to enhance the assistant's capabilities! Feel free to submit a pull request or open an issue.

## 📝 License

This project is licensed under the MIT License.
