# Process to calculate Intersection Over Union of Deep Learning Based Document Layout Analysis model's Inference:

## Inference
- [Document Image Transformer] (https://huggingface.co/spaces/nielsr/dit-document-layout-analysis)
- [Layout LM] (https://huggingface.co/spaces/nihalbaig/layoutlmv3_official_document)
- Custom Trained YoloV8 was inferred on local system

## Resize
To normalize the pixel values of images, inferred images were resized using [resize.ipynb](https://github.com/marufahmed/dla_paper_resources/blob/master/resize.ipynb)

## Annotation
To create the annotations for inferred predictions, [labelme](https://github.com/labelmeai/labelme) was used. The classes that were labeled are as follows:
- Paragraph
- Image
- Table

After annotating the inferred images, corresponding json files were created.

## IOU comparison
Individual & collective IOU comparison was measured using [iou_comparison.ipynb](https://github.com/marufahmed/dla_paper_resources/blob/master/iou_comparison.ipynb)

## Collected Data

|                    |    | bengali 1 |  | bengali 2 |  | marathi |  | gujrati |  |
|---------------------------|-----------|----------|---------|----------|---------|---------|----------|---------|----------|
| Model                     | Class     | Overlapping Areas | Average IoU | Overlapping Areas | Average IoU | Overlapping Areas | Average IoU | Overlapping Areas | Average IoU |
| Ground Truth              | Paragraph | 14       | 1       | 6        | 1       | 10      | 1        | 17      | 1        |
| Ground Truth              | Table     | 1        | 1       | 0        | 0       | 1       | 1        | 0       | 0        |
| Ground Truth              | Image     | 0        | 0       | 1        | 1       | 0       | 0        | 2       | 1        |
| Yolo V8 custom trained   | Paragraph | 14       | 0.812   | 5        | 0.808   | 10      | 0.904    | 16      | 0.865    |
| Yolo V8 custom trained   | Table     | 1        | 0.788   | 0        | 0       | 1       | 0.906    | 0       | 0        |
| Yolo V8 custom trained   | Image     | 0        | 0       | 1        | 0.938   | 0       | 0        | 2       | 0.777    |
| Document Image Transformer | Paragraph | 12       | 0.655   | 5        | 0.732   | 10      | 0.883    | 16      | 0.851    |
| Document Image Transformer | Table     | 1        | 0.746   | 0        | 0       | 1       | 0.531    | 0       | 0        |
| Document Image Transformer | Image     | 0        | 0       | 1        | 0.918   | 0       | 0        | 0       | 0        |
| Layout LM                 | Paragraph | 11       | 0.723   | 6        | 0.783   | 8       | 0.699    | 16      | 0.843    |
| Layout LM                 | Table     | 0        | 0       | 0        | 0       | 0       | 0        | 0       | 0.798    |
| Layout LM                 | Image     | 0        | 0       | 1        | 0.898   | 0       | 0        | 2       |          |
| Yolo V8 Pretrained        | Paragraph | 12       | 0.659   | 6        | 0.788   |         |          |         |          |
| Yolo V8 Pretrained        | Table     | 0        | 0.749   | 0        | 0       |         |          |         |          |
| Yolo V8 Pretrained        | Image     | 0        | 0       | 1        | 0.904   |         |          |         |          |
