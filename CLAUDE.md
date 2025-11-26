# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ClaudeCode_Secretary is a personal AI assistant system designed for 张俊 (Zhang Jun). The system consists of three specialized AI agents that act as personal life assistants:

1. **新闻张 (News Zhang)**: Morning news aggregator that searches AI, finance, and stock market news, creates daily news briefs in markdown format organized by date, and can send notifications via Feishu (飞书/Lark).

2. **教练张 (Coach Zhang)**: Daily health and fitness coach that tracks weight, provides exercise recommendations and meal delivery suggestions based on goals in "about me" profile, generates health tracking documents, and updates profile information.

3. **反思张 (Reflection Zhang)**: End-of-day reflection facilitator that conducts guided conversations about daily work and insights, performs deep exploration through multiple dialogue rounds, and generates reflective markdown documents to help understand work patterns, mental state, and personal growth.

## Project Architecture

This is a multi-agent system where each agent:
- Responds to specific trigger phrases ("早上好", "自律", "今工作结束了")
- Maintains context from an "about me" profile
- Generates dated markdown documents for record-keeping
- Has distinct conversational patterns and objectives

### Key Design Considerations

- **Trigger-based Activation**: Each agent activates based on specific user greetings or phrases
- **Document Generation**: All agents create timestamped markdown files organized by date
- **Profile Integration**: Agents read from and update a central "about me" profile with user goals and current metrics
- **External Integration**: System needs to integrate with Feishu/Lark API for notifications
- **Conversational Flow**: 反思张 requires multi-turn dialogue capabilities with deep questioning patterns

### Data Structure

Expected file organization:
- `about me/` - User profile with goals, current weight, preferences
- `YYYY-MM-DD/` - Date-based folders containing daily documents
  - `今日新闻.md` - Daily news briefs
  - `健康.md` - Health and fitness recommendations
  - `反思.md` - Daily reflection documents

## Implementation Notes

When implementing agents, ensure:
- Chinese language support throughout the system
- Natural conversation flow with appropriate personality for each agent role
- Robust date/time handling for file organization
- API integration patterns for web scraping (news) and Feishu notifications
- State management for multi-turn conversations (especially 反思张)
- Profile update mechanisms that preserve existing data while adding new metrics
