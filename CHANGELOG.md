# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.6] - 2025-01-26

### Added/Changed/Removed
- Add "menu" itens with icons

## [0.0.5] - 2025-01-22

### Added/Changed/Removed
- Change "myapp" folder to "directory"
- Add navbar image in template base.html
- Create additional views for:
    - User Management:
        - List all users with status indicators
        - Create new users
        - Edit user details
        - Reset passwords
        - Delete users
    - Group Management:
        - List all groups with member counts
        - Create new groups
        - Edit group details
        - Manage group membership
        - Delete groups
    - Computer Management:
        - List all computers with status and OS information
        - View computer details
    - Additional Features:
        - Confirmation modals for delete operations
        - Responsive tables
        - Clean Bootstrap-based UI
        - Form validation
        - Success/error messages
        - Audit logging of operations

## [0.0.4] - 2025-01-07

### Added/Changed/Removed
- Enable DEBUG in .env
- Change trace in two test files

## [0.0.3] - 2025-01-07

### Added/Changed/Removed
- Add template menu.html
- Change templates layout.html, home.html, about.html
- Add locale settings config (settings.py, views.py, urls.py )

## [0.0.2] - 2025-01-05

### Added/Changed/Removed
- Change the name of project from gnu_admw to core
- Change Settings of core project
- Add application myapp
- Add urls.py to myapp
- Add favicon.ico
- Add active-directory.png logo
- Change template base.html to layout.html
- Change template index.html to home.html
- Removed template menu.html

## [0.0.1] - 2025-01-03

### Added/Changed/Removed
- Project start.
- Add Directories created.
- Add Two scripts that assist in testing the configuration and connection to Active Directory provided.
