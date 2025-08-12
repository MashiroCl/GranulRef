# GranulRef

Tool to transform repository commit history into different granularities and detect refactorings.

## Coarse-grained Refactoring & Ephemeral Refactoring

**Coarse-grained Refactoring (CGR):** A refactoring whose code changes are recorded across multiple commits, rather than confined in a single commit. 

**Ephemeral Refactoring (EPR):** A refactoring whose code changes are recorded within a single commit and where modifications in adjacent commits would disrupt their integrity. 

## Refactoring Detection

Refactoring detection tool used is [RefactoringMiner3.0.4](https://github.com/tsantalis/RefactoringMiner)

## Usage
TODO


## Publications
The following articles include the details of CGR.

Lei Chen, Shinpei Hayashi. [Impact of Change Granularity in Refactoring Detection](https://dl.acm.org/doi/10.1145/3524610.3528386). In Proceedings of the 30th IEEE/ACM International Conference on Program Comprehension (ICPC 2022), Early Research Achievements (ERA) Track, pp. 565-569. Online, may, 2022

📖 [Read on arXiv](https://arxiv.org/abs/2204.11276)

```
@inproceedings{
  title={Impact of change granularity in refactoring detection},
  author={Chen, Lei and Hayashi, Shinpei},
  booktitle={Proceedings of the 30th IEEE/ACM International Conference on Program Comprehension},
  pages={565--569},
  year={2022}
}

```