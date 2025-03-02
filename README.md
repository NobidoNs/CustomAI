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

---

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

## 🚀 Getting Started  

### Prerequisites  

- Python 3.8+  
- A microphone-enabled device  

### Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/NobidoNs/CustomAI.git
   cd CustomAI
2. Install dependencies:
   pip install -r requirements.txt
   for linux: sudo apt install ffmpeg
3. (Optional) Install vosk model:
   Install model from https://alphacephei.com/vosk/models 
4. Run main.py file.

Last simplest configuration: https://github.com/NobidoNs/CustomAI/commit/89e4294d76a01d9c8c6b4fd115cf91d5c99e1642

## 💡 Contribution
We welcome contributions to enhance the assistant's capabilities! Feel free to submit a pull request or open an issue.

## 📝 License
This project is licensed under the MIT License.
