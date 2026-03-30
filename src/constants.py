from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INSTANCE_ROOT = ROOT / "instances"
INSTANCE_FJSSPW_PATH = INSTANCE_ROOT / "Example_Instances_FJSSP-WF"
INSTANCE_DATA_ROOT = INSTANCE_ROOT / "InstanceData"
INSTANCE_DATA_FJSSPW_PATH = INSTANCE_DATA_ROOT / "FJSSP-W"
INSTANCE_DATA_SELECTED_PATH = INSTANCE_ROOT / \
    "SelectedInstanceData" / "selected_instances_data.csv"
