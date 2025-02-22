import os

# toDo config

# System paths
voskModelPath = 'C:/work/AI/vosk-model-small-ru-0.22'
zapretPath = 'C:/Users/nobid/Downloads/Discord_zapret_with_voice_update_2/UltimateFix.bat'

# File names
outputFile = 'output.md'

# process paths
zapretProcess = 'C:/Users/nobid/Downloads/Discord_zapret_with_voice_update_2/bin'
backupPath = 'backups'


# Assistant settings
wakeWord = ["джарвис"]
baitWords = ["вис"]
waitTime = 7
wrightLog = False

# Command lists
commands = {
  "muteCommands" : ["тихо", "хватит", "стоп", "молчи", "-stop", "-стоп"],
  "voiceCommands" : ["-mute"],
  "clearCommands" : ["-cli", "-cls"],
  "saveCommands" : ["-save"],
  "restartZapretCommands" : ["-zapret", "-yt", "-ds"],
  "setSpeedCommands" : ["-speed","-x","-X"],
  "upSpeedCommands" : ["давай быстрее", "говори быстрее"],
  "downSpeedCommands" : ["давай помедленней", "слишком быстро", "говори медленнее"],
  "clearContextCommands" : ["-forget", "-fg", "забудь всё", "очисти контекст"]
}

# File codes
codes = ['  !', '    !', '\t!']
stopFind = ['------------','*Loading...*']

# Sound settings
soundStart = '' # 'sounds/rocket.wav'

# Audio settings
AUDIO_FREQUENCY = 53040

# Context memory settings
MAX_CONTEXT_LENGTH = 5  # Maximum number of message pairs to remember
CONTEXT_FILE = "context_memory.json"
