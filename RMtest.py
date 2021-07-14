from RefactoringMiner import RefactoringMiner

path=RMPath="/Users/leichen/ResearchAssistant/RefactoringMiner_commandline/RefactoringMiner-2.1.0/bin/RefactoringMiner"
rm=RefactoringMiner(path)
rm.detect(repository="/Users/leichen/ResearchAssistant/InteractiveRebase/data/RTEoutput2",output=".",commitID="139244cda9bdc747562c7c8b219478673a096139")