#Wrapper to pass ruby the true working directory
import os
workingDirectory = os.path.dirname(os.path.realpath(__file__))
workingDirectory += '/'
command = 'ruby ' + workingDirectory + 'command.rb ' + workingDirectory
os.system(command)