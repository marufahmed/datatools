########################################################################################

docker run --gpus=1 --rm -p 8000:8000 -p 8001:8001 -p 8002:8002 -v /home/ocr/ocr/ocr_triton_onnx/models:/models --name triton-server nvcr.io/nvidia/tritonserver:22.12-py3 tritonserver --model-repository=/models --exit-on-error=false

```
| ocr_word_lp      | 1       | UNAVAILABLE: Internal: onnx runtime error 1: /workspace/onnxruntime/onnxruntime/core/providers/cuda/cuda_call.cc:124 std::conditional_t<THRW, void, onnxruntime::common::Status> onnxruntime::CudaCall(ERRTYPE, const char*, const char*, ERRTYPE, const char*) [with ERRTYPE = cudaError; bool THRW = true; std::conditional_t<THRW, void, onnxruntime::common::Status> = void] /workspace/onnxruntime/onnxruntime/core/providers/cuda/cuda_call.cc:117 std::conditional_t<THRW,  |
|                  |         | void, onnxruntime::common::Status> onnxruntime::CudaCall(ERRTYPE, const char*, const char*, ERRTYPE, const char*) [with ERRTYPE = cudaError; bool THRW = true; std::conditional_t<THRW, void, onnxruntime::common::Status> = void] CUDA failure 900: operation not permitted when stream is capturing ; GPU=0 ; hostname=67521ae79fdc ; expr=cudaDeviceSynchronize();                                                                                                              |
|                  |         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ocr_word_tw      | 1       | UNAVAILABLE: Internal: onnx runtime error 1: /workspace/onnxruntime/onnxruntime/core/providers/cuda/cuda_call.cc:124 std::conditional_t<THRW, void, onnxruntime::common::Status> onnxruntime::CudaCall(ERRTYPE, const char*, const char*, ERRTYPE, const char*) [with ERRTYPE = cudaError; bool THRW = true; std::conditional_t<THRW, void, onnxruntime::common::Status> = void] /workspace/onnxruntime/onnxruntime/core/providers/cuda/cuda_call.cc:117 std::conditional_t<THRW,  |
|                  |         | void, onnxruntime::common::Status> onnxruntime::CudaCall(ERRTYPE, const char*, const char*, ERRTYPE, const char*) [with ERRTYPE = cudaError; bool THRW = true; std::conditional_t<THRW, void, onnxruntime::common::Status> = void] CUDA failure 900: operation not permitted when stream is capturing ; GPU=0 ; hostname=67521ae79fdc ; expr=cudaDeviceSynchronize();
```

########################################################################################

docker run --gpus=all --rm -p 8000:8000 -p 8001:8001 -p 8002:8002 -v /home/ocr/ocr/ocr_triton_onnx/models:/models --name triton-server nvcr.io/nvidia/tritonserver:22.12-py3 tritonserver --model-repository=/models --exit-on-error=false

```
| ocr_word_hwr     | 1       | UNAVAILABLE: Internal: onnx runtime error 1: /workspace/onnxruntime/onnxruntime/core/providers/cuda/cuda_call.cc:124 std::conditional_t<THRW, void, onnxruntime::common::Status> onnxruntime::CudaCall(ERRTYPE, const char*, const char*, ERRTYPE, const char*) [with ERRTYPE = cudaError; bool THRW = true; std::conditional_t<THRW, void, onnxruntime::common::Status> = void] /workspace/onnxruntime/onnxruntime/core/providers/cuda/cuda_call.cc:117 std::conditional_t<THRW,  |
|                  |         | void, onnxruntime::common::Status> onnxruntime::CudaCall(ERRTYPE, const char*, const char*, ERRTYPE, const char*) [with ERRTYPE = cudaError; bool THRW = true; std::conditional_t<THRW, void, onnxruntime::common::Status> = void] CUDA failure 900: operation not permitted when stream is capturing ; GPU=0 ; hostname=d9710c11b7de ; expr=cudaDeviceSynchronize();                                                                                                              |
|                  |         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ocr_word_lp      | 1       | UNAVAILABLE: Internal: onnx runtime error 1: /workspace/onnxruntime/onnxruntime/core/providers/cuda/cuda_call.cc:124 std::conditional_t<THRW, void, onnxruntime::common::Status> onnxruntime::CudaCall(ERRTYPE, const char*, const char*, ERRTYPE, const char*) [with ERRTYPE = cudaError; bool THRW = true; std::conditional_t<THRW, void, onnxruntime::common::Status> = void] /workspace/onnxruntime/onnxruntime/core/providers/cuda/cuda_call.cc:117 std::conditional_t<THRW,  |
|                  |         | void, onnxruntime::common::Status> onnxruntime::CudaCall(ERRTYPE, const char*, const char*, ERRTYPE, const char*) [with ERRTYPE = cudaError; bool THRW = true; std::conditional_t<THRW, void, onnxruntime::common::Status> = void] CUDA failure 900: operation not permitted when stream is capturing ; GPU=0 ; hostname=d9710c11b7de ; expr=cudaDeviceSynchronize();
```

########################################################################################

docker run --gpus=1 --rm -p 8000:8000 -p 8001:8001 -p 8002:8002 -v /home/ocr/ocr/ocr_triton_onnx/models:/models --name triton-server nvcr.io/nvidia/tritonserver:23.12-py3 tritonserver --model-repository=/models --exit-on-error=false

```
| ocr_character    | 1       | UNAVAILABLE:
| ocr_news_detect  | 1       | UNAVAILABLE:
| ocr_seg_east_hwr | 1       | UNAVAILABLE:
| ocr_seg_east_tw  | 1       | UNAVAILABLE:
| ocr_word_hwr     | 1       | UNAVAILABLE:
| ocr_word_lp      | 1       | UNAVAILABLE:
| ocr_word_tw      | 1       | UNAVAILABLE:
```

########################################################################################
docker run --gpus=all --rm -p 8000:8000 -p 8001:8001 -p 8002:8002 -v /home/ocr/ocr/ocr_triton_onnx/models:/models --name triton-server nvcr.io/nvidia/tritonserver:23.12-py3 tritonserver --model-repository=/models --exit-on-error=false

```
| ocr_character    | 1       | UNAVAILABLE:
| ocr_news_detect  | 1       | UNAVAILABLE:
| ocr_seg_east_hwr | 1       | UNAVAILABLE:
| ocr_seg_east_tw  | 1       | UNAVAILABLE:
| ocr_word_hwr     | 1       | UNAVAILABLE:
| ocr_word_lp      | 1       | UNAVAILABLE:
```

