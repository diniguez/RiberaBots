# MERiA
Metodologías Educativas basadas en Robótica, Inteligencia Artificial y Big Data

## First steps in Linux
# create and work into the virtual environment
python3 -m venv .venv   (or python3.10)
source .venv/bin/activate
# restart user session (close and open WSL terminal)
cd $folderOfTheRobot
source .venv/bin/activate

## First steps in Windows
# create and work into the virtual environment
python3 -m venv .venv   (or python3.10)
.\.venv\Scripts\activate.bat
# restart user session (close and open WSL terminal)
cd $folderOfTheRobot
.\.venv\Scripts\activate.bat

# launch code
python3 .\$code.py$