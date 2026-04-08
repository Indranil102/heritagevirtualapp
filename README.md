# AI-Powered Heritage Site Virtual Guide

## Overview

The **AI-Powered Heritage Site Virtual Guide** is an intelligent computer vision and LLM-based application that identifies heritage landmarks from uploaded images and generates contextual historical descriptions. The system combines image classification techniques with large language model (LLM) response generation to provide users with meaningful cultural and informational insights about recognized locations.

This project demonstrates an end-to-end AI pipeline integrating computer vision, backend APIs, and language models for real-world interactive use.

---

## Key Features

* Upload an image of a heritage site for automatic recognition
* Computer vision-based landmark identification
* LLM-powered contextual description generation
* FastAPI backend for scalable inference
* MongoDB database for structured data storage
* REST API support for easy integration with frontend applications

---

## System Architecture

The workflow of the application follows these steps:

1. User uploads an image through the interface
2. Image preprocessing standardizes resolution and format
3. Computer vision model extracts features and predicts the heritage site
4. Prediction result is passed to an LLM pipeline
5. LLM generates contextual historical and cultural information
6. Response is returned via FastAPI endpoint
7. Metadata is optionally stored in MongoDB for reuse and analytics

---

## Tech Stack

**Languages**

* Python

**Frameworks & Tools**

* FastAPI
* OpenCV
* NumPy
* MongoDB

**AI Components**

* Computer Vision Model for landmark classification
* LLM integration for contextual description generation

---

## Project Structure

```
heritagevirtualapp/
│
├── app/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   └── models/
│
├── database/
├── utils/
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the Repository

```
git clone https://github.com/Indranil102/heritagevirtualapp.git
cd heritagevirtualapp
```

### 2. Create Virtual Environment

```
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Start the Server

```
uvicorn app.main:app --reload
```

Server will run at:

```
http://127.0.0.1:8000
```

---

## API Workflow Example

**Input:** Upload image of a heritage landmark

**Processing:**

* Image preprocessing
* Feature extraction
* Landmark prediction
* LLM-based description generation

**Output:**

```
{
  "site": "Taj Mahal",
  "description": "The Taj Mahal is a UNESCO World Heritage Site located in Agra, India..."
}
```

---

## Model Pipeline

The AI pipeline integrates:

* Image preprocessing for normalization and consistency
* Feature extraction using computer vision techniques
* Landmark classification model
* LLM-based contextual explanation generation

This hybrid pipeline improves recognition consistency and produces informative outputs beyond simple classification.

---

## Future Improvements

* Expand dataset coverage for more heritage sites
* Add multilingual response generation
* Integrate vector database for retrieval-augmented responses
* Deploy cloud-based inference pipeline
* Add frontend visualization dashboard

---

## Author

**Indranil Samanta**

* GitHub: [https://github.com/Indranil102](https://github.com/Indranil102)
* LinkedIn: [https://linkedin.com/in/indranil]([https://linkedin.com/in/indranil](https://www.linkedin.com/in/indranil-samanta-26558a253/))

---

## License

This project is developed for academic and research purposes. Extendable for production deployment with additional optimization and dataset scali
