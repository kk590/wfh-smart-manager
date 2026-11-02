# System Architecture

See the README for the high-level overview of the multi-agent pipeline, dynamic schema extension, and security model.

This document expands on the internal components.

## Agents

- Intent Parser
- Permission Checker
- Code Generator
- Sandbox Validator
- Executor

## Data Model

Base tables: User, Team

Extension tables created on demand for custom attributes.
