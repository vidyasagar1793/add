#  AI Content Aggregator --- Agent Instructions

## Project Vision

Build an AI-powered web application that collects blog articles from
multiple sources based on user-selected topics, intelligently processes
them, personalizes recommendations, and sends mobile notifications to
users.

------------------------------------------------------------------------

# Core AI Agent Roles

## 1. Content Discovery Agent

**Purpose:** Discover relevant articles automatically.

### Responsibilities

-   Monitor RSS feeds, websites, APIs
-   Topic-based crawling
-   Detect trending articles
-   Deduplicate content

------------------------------------------------------------------------

## 2. Content Intelligence Agent

**Purpose:** Improve content usability.

### Responsibilities

-   Topic classification
-   AI summarization
-   Keyword extraction
-   Sentiment analysis
-   Relevance scoring

### Outputs

-   Article summaries
-   Topic tags
-   Relevance score
-   Notification priority

------------------------------------------------------------------------

## 3. Personalization Agent

**Purpose:** Match articles to user interests.

### Responsibilities

-   Maintain interest profiles
-   Learn from behavior:
    -   Clicks
    -   Reading time
    -   Ignored notifications
-   Rank recommendations

------------------------------------------------------------------------

## 4. Notification Agent

**Purpose:** Deliver timely updates.

### Responsibilities

-   Push notifications
-   Digest batching
-   Timing optimization
-   Notification fatigue control

------------------------------------------------------------------------

## 5. Moderation Agent

**Purpose:** Maintain content quality.

### Responsibilities

-   Spam filtering
-   Source validation
-   Misinformation detection

------------------------------------------------------------------------

# Full Technical Architecture Diagram

    External Sources
    (RSS / APIs / Blogs)
            |
            v
    Content Discovery Service
    (Scrapers + Scheduler)
            |
            v
    AI Processing Pipeline
    (Classification, Summaries,
    Embeddings, Scoring)
            |
            +-------------------+
            |                   |
            v                   v
    Primary Database        Vector Database
    (Users, Articles,       (Embeddings,
    Topics, Logs)           Similarity)
            |
            v
    Personalization Engine
    (Relevance Ranking)
            |
            +-------------------+
            |                   |
            v                   v
    Notification Service   Web Backend API
            |                   |
            v                   v
    Mobile Push Layer      Frontend Web App
    (PWA / Mobile Push)    (Dashboard)

------------------------------------------------------------------------

# System Components

## Frontend

-   Web dashboard
-   Topic management
-   Personalized feed
-   Notification settings

## Backend Services

-   Content ingestion pipeline
-   AI processing services
-   User profile service
-   Notification service

------------------------------------------------------------------------

# Databases

## Structured Database

Suggested: - PostgreSQL or MySQL

Stores: - Users - Topics - Article metadata - Notification history

## Vector Database

Suggested: - pgvector, Weaviate, Pinecone

Stores: - Article embeddings - User preference embeddings

------------------------------------------------------------------------

# Notification Strategy

## Channels

-   Progressive Web App push
-   Mobile push notifications
-   Email fallback

## Notification Types

-   Breaking topic alerts
-   Daily digest
-   Weekly digest

------------------------------------------------------------------------

# Development Phases

## Phase 1 --- MVP Foundation

-   Project setup
-   Basic scraping
-   RSS integration
-   User signup/login
-   Topic selection UI

## Phase 2 --- AI Integration

-   Article summarization
-   Topic classification
-   Embedding generation
-   Recommendation engine

## Phase 3 --- Notification System

-   Push notifications
-   Timing optimization
-   Frequency controls

## Phase 4 --- Optimization

-   Better recommendations
-   Performance scaling
-   Moderation filters

------------------------------------------------------------------------

# Recommended Tech Stack

## Backend

-   FastAPI or Node.js
-   Background jobs: Celery / BullMQ

## AI Layer

-   LLM APIs
-   Embedding models

## Frontend

-   React + Tailwind
-   Service worker push notifications

## Infrastructure

-   Cloud VPS or serverless
-   CDN frontend hosting

------------------------------------------------------------------------

# Success Metrics

-   Daily active users
-   Notification engagement rate
-   Article completion rate
-   Recommendation accuracy

------------------------------------------------------------------------

# Scalability Considerations

## Performance

-   Queue-based scraping
-   Batch AI processing
-   CDN caching

## Reliability

-   Retry pipelines
-   Monitoring
-   Source validation

## Security

-   OAuth authentication
-   Data encryption
-   Rate limiting

------------------------------------------------------------------------

# Agent Mission Summary

Build an automated AI-driven system that:

1.  Discovers relevant blog content
2.  Processes it using AI
3.  Personalizes recommendations
4.  Delivers notifications effectively
5.  Maintains high-quality content standards
