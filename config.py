import os

# System paths
voskModelPath = 'C:/work/AI/vosk-model-small-ru-0.22'
zapretPath = 'C:/Users/nobid/Downloads/Discord_zapret_with_voice_update_2/UltimateFix.bat'

# File names
outputFile = 'output.txt'

# process paths
zapretProcess = 'C:/Users/nobid/Downloads/Discord_zapret_with_voice_update_2/bin'

# Assistant settings
wakeWord = ["джарвис"]
baitWords = ["вис"]
waitTime = 7
wrightLog = False

# Command lists
muteCommands = ["тихо", "хватит", "стоп", "молчи", "-stop", "-стоп"]
voiceCommands = ["-mute", "-mute\n"]
clearCommands = ["-cli", "-cls"]
saveCommands = ["-save"]
restartZapretCommands = ["-zapret", "-yt", "-ds"]

# File codes
codes = ['  !', '    !', '\t!']

# Sound settings
soundStart = '' # 'sounds/rocket.wav'

# Audio settings
AUDIO_FREQUENCY = 53040