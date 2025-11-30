# Architecture Overview

This document provides a visual overview of the system architecture, illustrating how the core models, development platforms, and Google Cloud environment interact.

## System Components & Data Flow

```mermaid
graph TD
    %% A. Core Model and Development Platform
    subgraph A[Core Model and Development Platform]
        GEMINI("Gemini Models");
        AISTUDIO("Google AI Studio");
    end
    
    %% B. Google Cloud Environment (谷歌云环境)
    subgraph B[Google Cloud Platform - GCP]
        GCLOUD("gcloud CLI");
        VERTE_AI("Vertex AI Platform");
    end
    
    %% C. LLM Frameworks and Libraries
    subgraph C[Developer Integration]
        LANGCHAIN(LangChain / LangGraph);
        PYSDK("Google GenAI SDK");
    end
    
    %% Relationships
    
    %% 1. Model Consumers
    AISTUDIO -->|Consumes| GEMINI
    VERTE_AI -->|Deploys| GEMINI
    PYSDK -->|Calls API| GEMINI
    
    %% 2. Developer Integration Flow
    LANGCHAIN -->|Uses| PYSDK
    PYSDK -->|Prototyping| AISTUDIO
    
    %% 3. Management & Deployment
    GCLOUD -->|Manages| VERTE_AI
    VERTE_AI -->|Supports| LANGCHAIN
    
    %% 4. Core Feedback (Optional: Tuning or Feedback)
    GEMINI -.->|Tuning/Feedback| AISTUDIO
    
    %% Styling
    style GEMINI fill:#FFC107,stroke:#333,stroke-width:3px,color:#000
    style VERTE_AI fill:#4CAF50,stroke:#333,stroke-width:2px,color:#FFF
    style AISTUDIO fill:#2196F3,stroke:#333,stroke-width:2px,color:#FFF
    style GCLOUD fill:#9E9E9E,stroke:#333,stroke-width:2px,color:#FFF
    style LANGCHAIN fill:#9C27B0,stroke:#333,stroke-width:2px,color:#FFF

```
