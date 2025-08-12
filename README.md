# GranulRef

Tool to transform repository commit history into different granularities and detect refactorings.

## Coarse-grained Refactoring & Ephemeral Refactoring

**Coarse-grained Refactoring (CGR):** A refactoring whose code changes are recorded across multiple commits, rather than confined in a single commit. 

**Ephemeral Refactoring (EPR):** A refactoring whose code changes are recorded within a single commit and where modifications in adjacent commits would disrupt their integrity. 

## Refactoring Detection

Refactoring detection tool used is [RefactoringMiner3.0.4](https://github.com/tsantalis/RefactoringMiner)

## Usage
TODO