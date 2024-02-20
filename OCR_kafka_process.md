## Overall OCR Process

### Initiation
- The OCR process begins when images or documents are uploaded or submitted to the OCR system.

### Noise Removal (noise_consumer.py)
- Another Kafka consumer (`noise_consumer.py`) listens to the 'queue_noise_remove' topic.
- For each message received:
  - The script retrieves information such as 'id', 'projectId', 'fileName', and 'noiseType' from the Kafka message.
  - It performs noise removal, including tasks such as skew correction, border noise removal, and background removal.
  - The processed image is sent to the 'queue_detect_logo' Kafka topic for further processing.

### Logo Detection (logo_consumer.py)
- A Kafka consumer (`logo_consumer.py`) is set up to listen to the 'queue_detect_logo' topic.
- For each message received:
  - The script loads a pre-trained YOLOv5 model for logo detection.
  - It retrieves information such as 'id', 'projectId', 'fileName', and 'documentType' from the Kafka message.
  - If the document type is not 'hw' or 'tw', the script performs logo detection and removal using the YOLOv5 model.
  - The processed image and regions without logos are sent to the 'queue_segment_word' Kafka topic.

### Segmentation (segmentation_consumer.py)
- A Kafka consumer (`segmentation_consumer.py`) listens to the 'queue_segment_word' topic.
- For each message received:
  - The script retrieves information such as 'id', 'projectId', 'fileName', and 'documentType' from the Kafka message.
  - If the document type is 'hw' or 'tw', the script uses an EAST detector to detect words.
  - If the document type is not 'hw' or 'tw', the script removes logos based on previously detected regions.
  - The segmented words or text regions are sent to the 'queue_recognition' Kafka topic.

### Recognition (recognition_consumer.py)
- Another Kafka consumer (`recognition_consumer.py`) listens to the 'queue_recognition' topic.
- For each message received:
  - The script retrieves information such as 'id', 'projectId', 'fileName', 'documentType', 'isNewspaper', 'ocrModelType', and 'keepEnglish'.
  - It reads the image from the file server and optionally removes English text.
  - Depending on the document type, the script uses different OCR models (handwritten, typewriter, letterpress, or computer-generated) for word recognition.
  - The recognized words or text regions, along with layout information, are sent to the 'queue_docx_text_reconstruct' Kafka topic.
  - The recognized text and layout information are also posted to the layout URL.

### Document Text Reconstruction (not shown in provided scripts)
- This step may involve further processing to reconstruct the document text, potentially converting it to a structured format such as DOCX.

## Additional Notes

### Status and State Updates
- Throughout the process, the status and state of each document are updated in a central database or service.
- These updates indicate the progress of each document through various stages of the OCR pipeline.

### Exception Handling
- The scripts include exception handling mechanisms to log errors and update the status in case of failures during processing.

### Logging and Timing
- Loguru logger is used to record important events and timings at different stages of the OCR process.

### Producing to Kafka Topics
- Processed data, along with relevant information, is sent to different Kafka topics for subsequent stages in the pipeline.

### Integration with External Services
- The scripts interact with external services, such as file servers, layout URLs, and OCR models, to retrieve images, perform processing, and update information.

### Parallel Processing
- Kafka consumers process messages independently and in parallel, allowing for efficient and scalable OCR processing.
