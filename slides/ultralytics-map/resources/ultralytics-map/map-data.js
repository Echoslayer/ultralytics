const atlas = {
  "nodes": [
    {
      "path": "",
      "parent": "",
      "role": "專案總覽",
      "level": "會操作",
      "inherited": false,
      "files": [
        "README.md",
        "AGENTS.md",
        "CONTRIBUTING.md",
        "pyproject.toml"
      ],
      "deeper": true
    },
    {
      "path": ".github",
      "parent": "",
      "role": "貢獻檢查與自動化",
      "level": "會操作",
      "inherited": false,
      "files": [
        ".github/dependabot.yml"
      ],
      "deeper": true
    },
    {
      "path": ".github/ISSUE_TEMPLATE",
      "parent": ".github",
      "role": "貢獻檢查與自動化",
      "level": "會操作",
      "inherited": true,
      "files": [
        ".github/ISSUE_TEMPLATE/bug-report.yml",
        ".github/ISSUE_TEMPLATE/config.yml",
        ".github/ISSUE_TEMPLATE/feature-request.yml",
        ".github/ISSUE_TEMPLATE/question.yml"
      ],
      "deeper": false
    },
    {
      "path": ".github/actions",
      "parent": ".github",
      "role": "貢獻檢查與自動化",
      "level": "會操作",
      "inherited": true,
      "files": [],
      "deeper": true
    },
    {
      "path": ".github/scripts",
      "parent": ".github",
      "role": "貢獻檢查與自動化",
      "level": "會操作",
      "inherited": true,
      "files": [
        ".github/scripts/create-export-env.py",
        ".github/scripts/fuzz.py"
      ],
      "deeper": false
    },
    {
      "path": ".github/workflows",
      "parent": ".github",
      "role": "貢獻檢查與自動化",
      "level": "會操作",
      "inherited": true,
      "files": [
        ".github/workflows/ci.yml",
        ".github/workflows/cla.yml",
        ".github/workflows/conda-check-prs.yml",
        ".github/workflows/docker.yml",
        ".github/workflows/docs.yml",
        ".github/workflows/format.yml"
      ],
      "deeper": false
    },
    {
      "path": "docker",
      "parent": "",
      "role": "容器與部署環境",
      "level": "按需追",
      "inherited": false,
      "files": [],
      "deeper": false
    },
    {
      "path": "docs",
      "parent": "",
      "role": "使用指南與 API 參考",
      "level": "會操作",
      "inherited": false,
      "files": [
        "docs/AGENTS.md",
        "docs/CLAUDE.md",
        "docs/README.md",
        "docs/build_docs.py",
        "docs/build_reference.py",
        "docs/coming_soon_template.md"
      ],
      "deeper": true
    },
    {
      "path": "docs/en",
      "parent": "docs",
      "role": "使用指南與 API 參考",
      "level": "會操作",
      "inherited": true,
      "files": [
        "docs/en/index.md",
        "docs/en/quickstart.md"
      ],
      "deeper": true
    },
    {
      "path": "docs/macros",
      "parent": "docs",
      "role": "使用指南與 API 參考",
      "level": "會操作",
      "inherited": true,
      "files": [
        "docs/macros/augmentation-args.md",
        "docs/macros/export-args.md",
        "docs/macros/export-table.md",
        "docs/macros/platform-data-regions.md",
        "docs/macros/platform-gpu-table.md",
        "docs/macros/platform-inference-parameters.md"
      ],
      "deeper": false
    },
    {
      "path": "examples",
      "parent": "",
      "role": "平台整合範例",
      "level": "按需追",
      "inherited": false,
      "files": [
        "examples/README.md"
      ],
      "deeper": true
    },
    {
      "path": "examples/RTDETR-ONNXRuntime-Python",
      "parent": "examples",
      "role": "平台整合範例",
      "level": "按需追",
      "inherited": true,
      "files": [
        "examples/RTDETR-ONNXRuntime-Python/README.md",
        "examples/RTDETR-ONNXRuntime-Python/main.py"
      ],
      "deeper": false
    },
    {
      "path": "examples/YOLO-Axelera-Python",
      "parent": "examples",
      "role": "平台整合範例",
      "level": "按需追",
      "inherited": true,
      "files": [
        "examples/YOLO-Axelera-Python/README.md",
        "examples/YOLO-Axelera-Python/yolo11-seg.py",
        "examples/YOLO-Axelera-Python/yolo26-pose-tracker.py"
      ],
      "deeper": false
    },
    {
      "path": "examples/YOLO-Interactive-Tracking-UI",
      "parent": "examples",
      "role": "平台整合範例",
      "level": "按需追",
      "inherited": true,
      "files": [
        "examples/YOLO-Interactive-Tracking-UI/README.md",
        "examples/YOLO-Interactive-Tracking-UI/interactive_tracker.py"
      ],
      "deeper": false
    },
    {
      "path": "examples/YOLO-Series-ONNXRuntime-Rust",
      "parent": "examples",
      "role": "平台整合範例",
      "level": "按需追",
      "inherited": true,
      "files": [
        "examples/YOLO-Series-ONNXRuntime-Rust/Cargo.toml",
        "examples/YOLO-Series-ONNXRuntime-Rust/README.md"
      ],
      "deeper": true
    },
    {
      "path": "examples/YOLOv8-Action-Recognition",
      "parent": "examples",
      "role": "平台整合範例",
      "level": "按需追",
      "inherited": true,
      "files": [
        "examples/YOLOv8-Action-Recognition/README.md",
        "examples/YOLOv8-Action-Recognition/action_recognition.py"
      ],
      "deeper": false
    },
    {
      "path": "examples/YOLOv8-ONNXRuntime",
      "parent": "examples",
      "role": "平台整合範例",
      "level": "按需追",
      "inherited": true,
      "files": [
        "examples/YOLOv8-ONNXRuntime/README.md",
        "examples/YOLOv8-ONNXRuntime/main.py"
      ],
      "deeper": false
    },
    {
      "path": "examples/YOLOv8-ONNXRuntime-Rust",
      "parent": "examples",
      "role": "平台整合範例",
      "level": "按需追",
      "inherited": true,
      "files": [
        "examples/YOLOv8-ONNXRuntime-Rust/Cargo.toml",
        "examples/YOLOv8-ONNXRuntime-Rust/README.md"
      ],
      "deeper": true
    },
    {
      "path": "examples/YOLOv8-OpenCV-ONNX-Python",
      "parent": "examples",
      "role": "平台整合範例",
      "level": "按需追",
      "inherited": true,
      "files": [
        "examples/YOLOv8-OpenCV-ONNX-Python/README.md",
        "examples/YOLOv8-OpenCV-ONNX-Python/main.py"
      ],
      "deeper": false
    },
    {
      "path": "examples/YOLOv8-Region-Counter",
      "parent": "examples",
      "role": "平台整合範例",
      "level": "按需追",
      "inherited": true,
      "files": [
        "examples/YOLOv8-Region-Counter/README.md",
        "examples/YOLOv8-Region-Counter/yolov8_region_counter.py"
      ],
      "deeper": false
    },
    {
      "path": "examples/YOLOv8-SAHI-Inference-Video",
      "parent": "examples",
      "role": "平台整合範例",
      "level": "按需追",
      "inherited": true,
      "files": [
        "examples/YOLOv8-SAHI-Inference-Video/README.md",
        "examples/YOLOv8-SAHI-Inference-Video/yolov8_sahi.py"
      ],
      "deeper": false
    },
    {
      "path": "examples/YOLOv8-Segmentation-ONNXRuntime-Python",
      "parent": "examples",
      "role": "平台整合範例",
      "level": "按需追",
      "inherited": true,
      "files": [
        "examples/YOLOv8-Segmentation-ONNXRuntime-Python/README.md",
        "examples/YOLOv8-Segmentation-ONNXRuntime-Python/main.py"
      ],
      "deeper": false
    },
    {
      "path": "examples/cpp",
      "parent": "examples",
      "role": "平台整合範例",
      "level": "按需追",
      "inherited": true,
      "files": [
        "examples/cpp/README.md"
      ],
      "deeper": true
    },
    {
      "path": "research",
      "parent": "",
      "role": "本地貢獻研究",
      "level": "會操作",
      "inherited": false,
      "files": [],
      "deeper": true
    },
    {
      "path": "research/contributing",
      "parent": "research",
      "role": "本地貢獻研究",
      "level": "會操作",
      "inherited": true,
      "files": [
        "research/contributing/README.md",
        "research/contributing/mkdocs-run.py",
        "research/contributing/mkdocs.yml"
      ],
      "deeper": true
    },
    {
      "path": "tests",
      "parent": "",
      "role": "行為驗證與測試設定",
      "level": "深入讀",
      "inherited": false,
      "files": [
        "tests/__init__.py",
        "tests/cache_test_assets.py",
        "tests/conftest.py",
        "tests/test_cli.py",
        "tests/test_cuda.py",
        "tests/test_engine.py"
      ],
      "deeper": false
    },
    {
      "path": "ultralytics",
      "parent": "",
      "role": "Python 套件與命令列功能",
      "level": "深入讀",
      "inherited": false,
      "files": [
        "ultralytics/__init__.py"
      ],
      "deeper": true
    },
    {
      "path": "ultralytics/assets",
      "parent": "ultralytics",
      "role": "內建示例圖片",
      "level": "會操作",
      "inherited": false,
      "files": [],
      "deeper": false
    },
    {
      "path": "ultralytics/cfg",
      "parent": "ultralytics",
      "role": "參數與任務設定",
      "level": "深入讀",
      "inherited": false,
      "files": [
        "ultralytics/cfg/__init__.py",
        "ultralytics/cfg/default.yaml"
      ],
      "deeper": true
    },
    {
      "path": "ultralytics/cfg/datasets",
      "parent": "ultralytics/cfg",
      "role": "參數與任務設定",
      "level": "深入讀",
      "inherited": true,
      "files": [
        "ultralytics/cfg/datasets/Argoverse.yaml",
        "ultralytics/cfg/datasets/DOTAv1.5.yaml",
        "ultralytics/cfg/datasets/DOTAv1.yaml",
        "ultralytics/cfg/datasets/GlobalWheat2020.yaml",
        "ultralytics/cfg/datasets/HomeObjects-3K.yaml",
        "ultralytics/cfg/datasets/ImageNet.yaml"
      ],
      "deeper": false
    },
    {
      "path": "ultralytics/cfg/models",
      "parent": "ultralytics/cfg",
      "role": "參數與任務設定",
      "level": "深入讀",
      "inherited": true,
      "files": [
        "ultralytics/cfg/models/README.md"
      ],
      "deeper": true
    },
    {
      "path": "ultralytics/cfg/trackers",
      "parent": "ultralytics/cfg",
      "role": "參數與任務設定",
      "level": "深入讀",
      "inherited": true,
      "files": [
        "ultralytics/cfg/trackers/botsort.yaml",
        "ultralytics/cfg/trackers/bytetrack.yaml",
        "ultralytics/cfg/trackers/deepocsort.yaml",
        "ultralytics/cfg/trackers/fasttrack.yaml",
        "ultralytics/cfg/trackers/ocsort.yaml",
        "ultralytics/cfg/trackers/tracktrack.yaml"
      ],
      "deeper": false
    },
    {
      "path": "ultralytics/data",
      "parent": "ultralytics",
      "role": "載入、標註與增強",
      "level": "深入讀",
      "inherited": false,
      "files": [
        "ultralytics/data/__init__.py",
        "ultralytics/data/annotator.py",
        "ultralytics/data/augment.py",
        "ultralytics/data/base.py",
        "ultralytics/data/build.py",
        "ultralytics/data/converter.py"
      ],
      "deeper": true
    },
    {
      "path": "ultralytics/data/scripts",
      "parent": "ultralytics/data",
      "role": "載入、標註與增強",
      "level": "深入讀",
      "inherited": true,
      "files": [],
      "deeper": false
    },
    {
      "path": "ultralytics/engine",
      "parent": "ultralytics",
      "role": "任務共用流程",
      "level": "深入讀",
      "inherited": false,
      "files": [
        "ultralytics/engine/model.py",
        "ultralytics/engine/predictor.py",
        "ultralytics/engine/results.py",
        "ultralytics/engine/trainer.py",
        "ultralytics/engine/validator.py",
        "ultralytics/engine/exporter.py"
      ],
      "deeper": false
    },
    {
      "path": "ultralytics/models",
      "parent": "ultralytics",
      "role": "模型與任務特定行為",
      "level": "深入讀",
      "inherited": false,
      "files": [
        "ultralytics/models/__init__.py",
        "ultralytics/models/llm.py"
      ],
      "deeper": true
    },
    {
      "path": "ultralytics/models/fastsam",
      "parent": "ultralytics/models",
      "role": "模型與任務特定行為",
      "level": "深入讀",
      "inherited": true,
      "files": [
        "ultralytics/models/fastsam/__init__.py",
        "ultralytics/models/fastsam/model.py",
        "ultralytics/models/fastsam/predict.py",
        "ultralytics/models/fastsam/utils.py",
        "ultralytics/models/fastsam/val.py"
      ],
      "deeper": false
    },
    {
      "path": "ultralytics/models/nas",
      "parent": "ultralytics/models",
      "role": "模型與任務特定行為",
      "level": "深入讀",
      "inherited": true,
      "files": [
        "ultralytics/models/nas/__init__.py",
        "ultralytics/models/nas/model.py",
        "ultralytics/models/nas/predict.py",
        "ultralytics/models/nas/val.py"
      ],
      "deeper": false
    },
    {
      "path": "ultralytics/models/rtdetr",
      "parent": "ultralytics/models",
      "role": "模型與任務特定行為",
      "level": "深入讀",
      "inherited": true,
      "files": [
        "ultralytics/models/rtdetr/__init__.py",
        "ultralytics/models/rtdetr/model.py",
        "ultralytics/models/rtdetr/predict.py",
        "ultralytics/models/rtdetr/train.py",
        "ultralytics/models/rtdetr/val.py"
      ],
      "deeper": false
    },
    {
      "path": "ultralytics/models/sam",
      "parent": "ultralytics/models",
      "role": "模型與任務特定行為",
      "level": "深入讀",
      "inherited": true,
      "files": [
        "ultralytics/models/sam/__init__.py",
        "ultralytics/models/sam/amg.py",
        "ultralytics/models/sam/build.py",
        "ultralytics/models/sam/build_sam3.py",
        "ultralytics/models/sam/model.py",
        "ultralytics/models/sam/predict.py"
      ],
      "deeper": true
    },
    {
      "path": "ultralytics/models/utils",
      "parent": "ultralytics/models",
      "role": "模型與任務特定行為",
      "level": "深入讀",
      "inherited": true,
      "files": [
        "ultralytics/models/utils/__init__.py",
        "ultralytics/models/utils/loss.py",
        "ultralytics/models/utils/ops.py"
      ],
      "deeper": false
    },
    {
      "path": "ultralytics/models/yolo",
      "parent": "ultralytics/models",
      "role": "模型與任務特定行為",
      "level": "深入讀",
      "inherited": true,
      "files": [
        "ultralytics/models/yolo/__init__.py",
        "ultralytics/models/yolo/model.py"
      ],
      "deeper": true
    },
    {
      "path": "ultralytics/nn",
      "parent": "ultralytics",
      "role": "網路組裝與執行後端",
      "level": "按需追",
      "inherited": false,
      "files": [
        "ultralytics/nn/__init__.py",
        "ultralytics/nn/autobackend.py",
        "ultralytics/nn/distill_model.py",
        "ultralytics/nn/tasks.py",
        "ultralytics/nn/text_model.py"
      ],
      "deeper": true
    },
    {
      "path": "ultralytics/nn/backends",
      "parent": "ultralytics/nn",
      "role": "網路組裝與執行後端",
      "level": "按需追",
      "inherited": true,
      "files": [
        "ultralytics/nn/backends/__init__.py",
        "ultralytics/nn/backends/ascend.py",
        "ultralytics/nn/backends/axelera.py",
        "ultralytics/nn/backends/base.py",
        "ultralytics/nn/backends/coreai.py",
        "ultralytics/nn/backends/coreml.py"
      ],
      "deeper": false
    },
    {
      "path": "ultralytics/nn/modules",
      "parent": "ultralytics/nn",
      "role": "網路組裝與執行後端",
      "level": "按需追",
      "inherited": true,
      "files": [
        "ultralytics/nn/modules/__init__.py",
        "ultralytics/nn/modules/activation.py",
        "ultralytics/nn/modules/block.py",
        "ultralytics/nn/modules/conv.py",
        "ultralytics/nn/modules/head.py",
        "ultralytics/nn/modules/transformer.py"
      ],
      "deeper": false
    },
    {
      "path": "ultralytics/optim",
      "parent": "ultralytics",
      "role": "最佳化器",
      "level": "按需追",
      "inherited": false,
      "files": [
        "ultralytics/optim/__init__.py",
        "ultralytics/optim/muon.py"
      ],
      "deeper": false
    },
    {
      "path": "ultralytics/solutions",
      "parent": "ultralytics",
      "role": "計數與場景應用",
      "level": "按需追",
      "inherited": false,
      "files": [
        "ultralytics/solutions/__init__.py",
        "ultralytics/solutions/ai_gym.py",
        "ultralytics/solutions/analytics.py",
        "ultralytics/solutions/config.py",
        "ultralytics/solutions/distance_calculation.py",
        "ultralytics/solutions/heatmap.py"
      ],
      "deeper": true
    },
    {
      "path": "ultralytics/solutions/templates",
      "parent": "ultralytics/solutions",
      "role": "計數與場景應用",
      "level": "按需追",
      "inherited": true,
      "files": [],
      "deeper": false
    },
    {
      "path": "ultralytics/trackers",
      "parent": "ultralytics",
      "role": "跨影格追蹤",
      "level": "按需追",
      "inherited": false,
      "files": [
        "ultralytics/trackers/README.md",
        "ultralytics/trackers/__init__.py",
        "ultralytics/trackers/basetrack.py",
        "ultralytics/trackers/bot_sort.py",
        "ultralytics/trackers/byte_tracker.py",
        "ultralytics/trackers/deep_oc_sort.py"
      ],
      "deeper": true
    },
    {
      "path": "ultralytics/trackers/utils",
      "parent": "ultralytics/trackers",
      "role": "跨影格追蹤",
      "level": "按需追",
      "inherited": true,
      "files": [
        "ultralytics/trackers/utils/__init__.py",
        "ultralytics/trackers/utils/gmc.py",
        "ultralytics/trackers/utils/kalman_filter.py",
        "ultralytics/trackers/utils/matching.py",
        "ultralytics/trackers/utils/reid.py",
        "ultralytics/trackers/utils/stracks.py"
      ],
      "deeper": false
    },
    {
      "path": "ultralytics/utils",
      "parent": "ultralytics",
      "role": "損失、指標與共用工具",
      "level": "按需追",
      "inherited": false,
      "files": [
        "ultralytics/utils/__init__.py",
        "ultralytics/utils/autobatch.py",
        "ultralytics/utils/autodevice.py",
        "ultralytics/utils/benchmarks.py",
        "ultralytics/utils/checks.py",
        "ultralytics/utils/cpu.py"
      ],
      "deeper": true
    },
    {
      "path": "ultralytics/utils/callbacks",
      "parent": "ultralytics/utils",
      "role": "損失、指標與共用工具",
      "level": "按需追",
      "inherited": true,
      "files": [
        "ultralytics/utils/callbacks/__init__.py",
        "ultralytics/utils/callbacks/base.py",
        "ultralytics/utils/callbacks/clearml.py",
        "ultralytics/utils/callbacks/comet.py",
        "ultralytics/utils/callbacks/dvc.py",
        "ultralytics/utils/callbacks/mlflow.py"
      ],
      "deeper": false
    },
    {
      "path": "ultralytics/utils/export",
      "parent": "ultralytics/utils",
      "role": "損失、指標與共用工具",
      "level": "按需追",
      "inherited": true,
      "files": [
        "ultralytics/utils/export/__init__.py",
        "ultralytics/utils/export/ascend.py",
        "ultralytics/utils/export/axelera.py",
        "ultralytics/utils/export/coreai.py",
        "ultralytics/utils/export/coreml.py",
        "ultralytics/utils/export/deepx.py"
      ],
      "deeper": false
    }
  ]
};
