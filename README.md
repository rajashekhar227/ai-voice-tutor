# AI Voice Tutor – IVR Learning Platform

An AI-powered voice learning platform that enables students to access educational content through keypad/feature phones using an IVR (Interactive Voice Response) system.

The system combines Retrieval-Augmented Generation (RAG), multilingual Text-to-Speech, FastAPI, and Exotel IVR to deliver structured educational lessons through phone calls without requiring a smartphone or internet-enabled device.

## Features

- Keypad Phone Support – Students can access lessons using a regular phone and keypad inputs.
- Multilingual Learning – Supports English, Hindi, and Telugu.
- Educational Content Processing – Extracts and processes educational content from textbook PDF files.
- RAG-based Content Retrieval – Uses embeddings and FAISS to retrieve relevant educational content.
- Text-to-Speech – Converts lesson content into speech using Piper TTS.
- Multilingual Voice Models – Uses language-specific ONNX voice models for English, Hindi, and Telugu.
- Custom Audio Playback – Generated lessons are stored as WAV files and played during phone calls.
- IVR Navigation – Students can select language, subject, and topic using keypad numbers.
- FastAPI Backend – Provides REST APIs for IVR interaction and audio delivery.
- Exotel Integration – Handles phone calls and IVR-based lesson delivery.

## System Architecture

```text
Educational PDFs
      |
      v
   PyMuPDF
      |
      v
Text Cleaning
      |
      v
Text Chunking
      |
      v
Sentence Transformers
   Embeddings
      |
      v
    FAISS
      |
      v
     RAG
      |
      v
Lesson Generation
      |
      v
   Piper TTS
    + ONNX
      |
      v
   WAV Audio
      |
      v
    Exotel
      |
      v
  Student Phone
```

## IVR Flow

```text
Call AI Voice Tutor
        |
        v
 Select Language
    /    |    \
   1     2     3
   |     |     |
English Hindi Telugu
   |     |     |
   +-----+-----+
         |
         v
  Select Subject
         |
         v
       Science
         |
         v
    Select Topic
         |
         v
    Kharif Crops
         |
         v
  Play Lesson Audio
         |
         v
       Hang Up
```

## How It Works

### 1. Educational Content Processing

Educational textbook PDFs are processed using PyMuPDF. Text is extracted from the documents, cleaned, and divided into smaller chunks for efficient retrieval.

### 2. Embedding Generation

The processed text chunks are converted into numerical vector representations using Sentence Transformers.

### 3. Vector Search with FAISS

The generated embeddings are stored in FAISS, enabling similarity-based retrieval of relevant educational content.

### 4. Retrieval-Augmented Generation

The RAG pipeline retrieves relevant information from the indexed educational content and uses it as context for generating structured lesson content.

### 5. Text-to-Speech

The generated lesson text is converted into speech using Piper TTS with ONNX-based voice models.

```text
English → English Voice Model
Hindi   → Hindi Voice Model
Telugu  → Telugu Voice Model
```

### 6. Audio Generation

The generated speech is saved as WAV audio files. These audio files are uploaded to the Exotel Audio Library for playback during IVR calls.

### 7. IVR Delivery

Exotel handles the incoming phone call and keypad-based navigation.

```text
Language → Subject → Topic → Lesson Audio
```

After the topic is selected, the corresponding lesson audio is played over the phone.

## Exotel Setup

Exotel is used as the telephony and IVR layer of the project.

The IVR flow is configured using Exotel's Custom App / App Builder.

### Step 1: Create an Exotel Account

Create an Exotel account and obtain a trial phone number/exophone for testing.

### Step 2: Create a Custom IVR App

Create a Custom App using Exotel's App Builder.

Basic flow:

```text
Call Start → Greeting → IVR Menu
```

### Step 3: Configure the Welcome Menu

Configure the first IVR menu for language selection.

Example prompt:

```text
Welcome to AI Voice Tutor.
Press 1 for English.
Press 2 for Hindi.
Press 3 for Telugu.
```

Keypad mapping:

```text
1 → English
2 → Hindi
3 → Telugu
```

### Step 4: Configure Language Selection

After selecting a language, use another IVR Menu.

Example:

```text
You selected English.
Press 1 for Science.
```

Configure equivalent menus for Hindi and Telugu.

### Step 5: Configure Subject Selection

After selecting Science:

```text
You selected Science.
Press 1 for Kharif Crops.
```

### Step 6: Configure Topic Selection

Configure the topic menu:

```text
Press 1 for Kharif Crops.
```

When the student presses `1`, the call proceeds to the lesson audio.

### Step 7: Upload Lesson Audio

Upload the generated WAV files to the Exotel Audio Library.

Example:

```text
hesc1dd_kharif_crops_english.wav
hesc1dd_kharif_crops_hindi.wav
hesc1dd_kharif_crops_telugu.wav
```

### Step 8: Configure Audio Playback

Place a Greeting applet after the topic selection and select the appropriate WAV file.

```text
Topic Selection
      |
      v
Greeting Applet
      |
      v
Lesson WAV Audio
      |
      v
Student hears lesson
```

### Step 9: Add Hangup

Connect a Hangup applet after the lesson audio.

```text
Lesson Audio → Hangup
```

### Step 10: Save and Test

1. Save the Custom App.
2. Call the Exotel number.
3. Select a language using the keypad.
4. Select the subject.
5. Select the topic.
6. Verify that the correct language-specific audio is played.
7. Verify that the call terminates after the lesson.

## Audio Requirements

For Exotel compatibility, the generated audio can be converted to telephony-compatible WAV format.

```text
Channels:      Mono
Sample Rate:   8000 Hz
Sample Width:  16-bit
Format:        WAV
```

Audio generated at a higher sample rate can be resampled to 8000 Hz before uploading to Exotel.

## API Endpoints

### Health Check

```http
GET /
```

Returns the current status of the AI Voice Tutor backend.

### Get Languages

```http
GET /ivr
```

Returns the available language options.

### Select Language

```http
POST /ivr/language
```

Example request:

```json
{
    "digit": "1"
}
```

### Select Subject

```http
POST /ivr/subject
```

Example request:

```json
{
    "language": "english",
    "digit": "1"
}
```

### Select Topic

```http
POST /ivr/topic
```

Example request:

```json
{
    "language": "english",
    "subject": "science",
    "digit": "1"
}
```

### Audio Delivery

```http
GET /audio/{filename}
```

Serves the generated WAV lesson audio files.

## Technology Stack

### Programming Language
- Python

### Backend
- FastAPI
- REST APIs

### AI / Machine Learning
- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- FAISS
- Sentence Transformers

### Document Processing
- PyMuPDF

### Text-to-Speech
- Piper TTS
- ONNX Voice Models

### Telephony
- Exotel
- IVR

### Development Tools
- Git
- GitHub
- VS Code
- Jupyter Notebook

## Project Structure

```text
ai-voice-tutor/
│
├── app/
│   ├── api/
│   ├── audio/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── prompts/
│   ├── rag/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── data/
│   └── audio/
│
├── scripts/
│
├── tests/
│
├── vector_store/
│   ├── chunks.json
│   ├── metadata.json
│   └── subject.index
│
├── requirements.txt
├── .env
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/rajashekhar227/ai-voice-tutor.git
```

Navigate to the project directory:

```bash
cd ai-voice-tutor
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

FastAPI interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Text-to-Speech Models

The project uses Piper TTS with ONNX voice models.

```text
en_US-lessac-medium.onnx
hi_IN-priyamvada-medium.onnx
te_IN-venkatesh-medium.onnx
```

These models are used to generate speech for English, Hindi, and Telugu.

## Audio Pipeline

```text
Lesson Text
     |
     v
Piper TTS
     |
     v
ONNX Voice Model
     |
     v
WAV Audio
     |
     v
Audio Conversion
     |
     v
Exotel Audio Library
     |
     v
IVR Call
     |
     v
Student
```

## Supported Languages

| Language | Support |
|----------|---------|
| English  | Yes |
| Hindi    | Yes |
| Telugu   | Yes |

## Example Interaction

```text
Student calls the AI Voice Tutor number.

AI:
Welcome to AI Voice Tutor.
Press 1 for English.
Press 2 for Hindi.
Press 3 for Telugu.

Student:
1

AI:
You selected English.
Press 1 for Science.

Student:
1

AI:
You selected Science.
Press 1 for Kharif Crops.

Student:
1

AI:
[Plays Kharif Crops lesson audio]

Call ends.
```

## Use Case

The project is designed to improve access to digital education for students who may not have access to smartphones, computers, or reliable internet connectivity.

Instead of requiring a smartphone or educational application, students can call the provided number and use their phone keypad to navigate through educational lessons.

The system combines AI-based educational content processing with traditional telephony to provide learning through a familiar medium: a regular phone call.

## Future Enhancements

- Add more subjects and educational topics.
- Support additional regional languages.
- Add interactive quizzes using keypad inputs.
- Track student learning progress.
- Add personalized learning paths.
- Expand the educational knowledge base.
- Generate lessons automatically for newly added topics.
- Add question-answer based voice interactions.
- Improve lesson personalization based on student performance.
- Add more IVR-based educational activities.

## Project Goals

The main goal of the project is to make technology-assisted education accessible to students using basic mobile phones.

By combining RAG-based educational content processing, multilingual Text-to-Speech, and Exotel IVR, the platform allows students to access structured educational lessons through a simple phone call.

## License

This project is developed for educational and academic purposes.
