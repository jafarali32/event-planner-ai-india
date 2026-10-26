# Changelog

All notable changes to CelebrateAI will be documented in this file.

## [1.1.0] - 2026-10-26
### Added
- GZip compression middleware for optimized asset delivery.
- Comprehensive security headers (`nosniff`, `SAMEORIGIN`, `X-XSS-Protection`).
- WCAG 2.1 AA/AAA accessibility compliance across all UI components.
- In-memory LRU caching for static blueprint samples.
- Expanded automated test suite with boundary and security validation.

### Changed
- Replaced stdout logging with structured Python `logging` module.
- Enforced strict Pydantic v2 input sanitization and field constraints.
