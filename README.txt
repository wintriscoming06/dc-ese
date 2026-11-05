DISTRIBUTED COMPUTING ESE - VS CODE PYTHON PACK
================================================

CONTENTS
- 10 fully commented Python programs
- 9 matching CSV sample datasets (one CSV per experiment)
- This README

HOW TO RUN IN VS CODE (UBUNTU OR WINDOWS)
1. Extract this ZIP.
2. Open the extracted folder in VS Code: File > Open Folder.
3. Open Terminal > New Terminal.
4. Confirm Python is installed:
       python3 --version
   On Windows, use:
       py --version
5. Run the required experiment, for example:
       python3 02_bully.py
   On Windows:
       py 02_bully.py

IMPORTANT
- Keep each Python file and its CSV in the same folder.
- CSV names in the programs must match the filenames here. If your exam slip gives a different suffix, edit the filename inside open("...csv").
- No third-party Python packages are required. The programs use Python standard-library modules.
- Experiment 9 Ring follows the supplied code PDF's highest-priority rule. If your slip says highest node ID, use max(token) as noted in the code.
- Experiment 10 is a ThreadPoolExecutor-based Scatter-Gather simulation. It is not actual MPI/mpi4py.
- Berkeley filters faulty nodes marked TRUE to follow the question-slip requirement.
