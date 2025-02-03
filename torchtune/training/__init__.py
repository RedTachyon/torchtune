# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from torchtune.training._activation_offloading import (
    get_act_offloading_ctx_manager,
    NoOpManager,
    OffloadActivations,
)
from torchtune.training._compile import compile_loss, compile_model
from torchtune.training._distributed import (
    gather_cpu_state_dict,
    get_full_optimizer_state_dict,
    get_shard_conditions,
    get_world_size_and_rank,
    init_distributed,
    is_distributed,
    load_from_full_model_state_dict,
    load_from_full_optimizer_state_dict,
    prepare_mha_for_tp,
    set_torch_num_threads,
    shard_model,
    validate_no_params_on_meta_device, get_distributed_backend,
)
from torchtune.training._grad_scaler import scale_grads
from torchtune.training._profiler import (
    DEFAULT_PROFILE_DIR,
    DEFAULT_PROFILER_ACTIVITIES,
    DEFAULT_SCHEDULE,
    DEFAULT_TRACE_OPTS,
    DummyProfiler,
    PROFILER_KEY,
    setup_torch_profiler,
)
from torchtune.training.activations import apply_selective_activation_checkpointing
from torchtune.training.checkpointing import (
    ADAPTER_CONFIG,
    ADAPTER_KEY,
    Checkpointer,
    DistributedCheckpointer,
    EPOCHS_KEY,
    FormattedCheckpointFiles,
    FullModelHFCheckpointer,
    FullModelMetaCheckpointer,
    FullModelTorchTuneCheckpointer,
    MAX_STEPS_KEY,
    MODEL_KEY,
    ModelType,
    OPT_KEY,
    RNG_KEY,
    SEED_KEY,
    STEPS_KEY,
    TOTAL_EPOCHS_KEY,
    update_state_dict_for_classifier,
)
from torchtune.training.lr_schedulers import get_cosine_schedule_with_warmup, get_lr
from torchtune.training.memory import (
    cleanup_before_training,
    create_optim_in_bwd_wrapper,
    get_memory_stats,
    log_memory_stats,
    OptimizerInBackwardWrapper,
    register_optim_in_bwd_hooks,
    set_activation_checkpointing,
)
from torchtune.training.pooling import get_unmasked_sequence_lengths
from torchtune.training.precision import (
    get_dtype,
    set_default_dtype,
    validate_expected_param_dtype,
)
from torchtune.training.quantization import get_quantizer_mode
from torchtune.training.seed import set_seed

__all__ = [
    "get_act_offloading_ctx_manager",
    "prepare_mha_for_tp",
    "apply_selective_activation_checkpointing",
    "get_dtype",
    "set_default_dtype",
    "validate_expected_param_dtype",
    "FullModelHFCheckpointer",
    "FullModelMetaCheckpointer",
    "DistributedCheckpointer",
    "FullModelTorchTuneCheckpointer",
    "ModelType",
    "Checkpointer",
    "update_state_dict_for_classifier",
    "ADAPTER_CONFIG",
    "ADAPTER_KEY",
    "EPOCHS_KEY",
    "MAX_STEPS_KEY",
    "MODEL_KEY",
    "OPT_KEY",
    "RNG_KEY",
    "SEED_KEY",
    "STEPS_KEY",
    "TOTAL_EPOCHS_KEY",
    "get_quantizer_mode",
    "get_cosine_schedule_with_warmup",
    "get_lr",
    "cleanup_before_training",
    "create_optim_in_bwd_wrapper",
    "get_memory_stats",
    "log_memory_stats",
    "OptimizerInBackwardWrapper",
    "register_optim_in_bwd_hooks",
    "set_activation_checkpointing",
    "init_distributed",
    "is_distributed",
    "get_world_size_and_rank",
    "set_torch_num_threads",
    "shard_model",
    "get_shard_conditions",
    "validate_no_params_on_meta_device",
    "gather_cpu_state_dict",
    "get_full_optimizer_state_dict",
    "load_from_full_model_state_dict",
    "load_from_full_optimizer_state_dict",
    "set_seed",
    "get_unmasked_sequence_lengths",
    "DEFAULT_PROFILE_DIR",
    "DEFAULT_PROFILER_ACTIVITIES",
    "DEFAULT_SCHEDULE",
    "DEFAULT_TRACE_OPTS",
    "DummyProfiler",
    "PROFILER_KEY",
    "setup_torch_profiler",
    "compile_loss",
    "compile_model",
    "NoOpManager",
    "OffloadActivations",
    "FormattedCheckpointFiles",
    "scale_grads",
    "get_distributed_backend"
]
