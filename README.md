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
                    +-----------+
                    |  PyMuPDF  |
                    |   PDF     |
                    | Extraction|
                    +-----+-----+
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
                    +-----------+
                    |   FAISS   |
                    |   Vector  |
                    |   Search  |
                    +-----+-----+
                          |
                          v
                         RAG
                          |
                          v
                  Lesson Generation
                          |
                          v
                    +-----------+
                    | Piper TTS |
                    |   ONNX    |
                    +-----+-----+
                          |
                          v
                     WAV Audio
                          |
                          v
                    +-----------+
                    |  Exotel   |
                    |    IVR    |
                    +-----+-----+
                          |
                          v
                    Student Phone