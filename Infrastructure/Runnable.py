from importlib import reload as rl
import sys, subprocess

def createFile(pyCode):
    f = open("temp.py", "w+")
    f.write(pyCode)
    f.close()

    return executer()

def executer():

    try:
        cmdCommand = "python temp.py"  # specify your cmd command
        process = subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error is None:
            print(output)
            return output
        else:
            return error
    except (ModuleNotFoundError, SyntaxError, UnboundLocalError) as err:
            return err






        



