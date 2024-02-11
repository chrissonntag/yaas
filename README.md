## Installation

### Conda

**Short way**
```shell
conda env create -f conda-env.yml
poetry install
```

**Still short**
```shell
conda create -n yaas python=3.11
conda activate yaas
conda install poetry
peotry install
```

## Usage

```shell
python yaas.py config/agentchat_auto_feedback_from_code_execution.yaml
```
