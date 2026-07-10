# iDRAC9 Documentation Index

This directory contains references to official Dell iDRAC9 documentation. Due to Dell's access restrictions, direct downloads require authentication through Dell's support portal.

## Available Documentation

### User Guides

#### iDRAC9 User's Guide
- **URL**: https://www.dell.com/support/product-details/en-us/product/idrac9-lifecycle-controller-v7.x-series/resources/manuals
- **Description**: Comprehensive information on iDRAC9 features, setup, and management
- **Updated**: March 16, 2026
- **File**: Requires manual download from Dell support portal
- **Storage Location**: `./idrac9-user-guide.pdf` (to be downloaded manually)

#### Integrated Dell Remote Access Controller 9 RACADM CLI Guide
- **Description**: RACADM subcommands, interfaces, and property database definitions
- **Updated**: December 16, 2025
- **File**: Requires manual download from Dell support portal

#### Lifecycle Controller User's Guide
- **Description**: iDRAC9 LC User guide
- **Updated**: March 12, 2024
- **File**: Requires manual download from Dell support portal

### Reference Guides

#### iDRAC9 Attribute Registry
- **Description**: Manageable attributes of iDRAC and components (BIOS, FC, NIC, Storage, etc.)
- **Updated**: March 16, 2026
- **File**: Requires manual download from Dell support portal

#### PowerEdge Servers Error and Event Messages Reference Guide
- **Description**: Error messages displayed on GUI, CLI, and stored in log files
- **Updated**: April 25, 2026
- **File**: Requires manual download from Dell support portal

#### iDRAC Error and Event Messages Reference Guide
- **Description**: iDRAC-specific error and event messages for 12G-17G PowerEdge servers
- **Updated**: January 23, 2026
- **File**: Requires manual download from Dell support portal

### Security Guides

#### iDRAC9 Security Configuration Guide
- **Description**: Security features configuration and recommended settings
- **Updated**: January 16, 2026
- **File**: Requires manual download from Dell support portal

### Telemetry Guides

#### Dell iDRAC Telemetry Reference Guide
- **Description**: Telemetry feature for collecting and streaming live system data
- **Updated**: September 23, 2025
- **File**: Requires manual download from Dell support portal

## iDRAC9 Version 7.x Release Notes

The following iDRAC9 Version 7.x release notes are available from Dell's support portal:

### Latest Releases
- **iDRAC9 Version 7.30.30.51 Release Notes** (Updated: June 15, 2026)
- **iDRAC9 Version 7.30.10.50 Release Notes** (Updated: March 16, 2026)

### Version 7.20.x Series
- **iDRAC9 Version 7.20.80.50 Release Notes** (Updated: December 16, 2025)
- **iDRAC9 Version 7.20.70.50 Release Notes** (Updated: November 03, 2025)
- **iDRAC9 Version 7.20.60.50 Release Notes** (Updated: September 01, 2025)
- **iDRAC9 Version 7.20.30.50 Release Notes** (Updated: June 23, 2025)
- **iDRAC9 Version 7.20.30.00 Release Notes** (Updated: April 25, 2025)
- **iDRAC9 Version 7.20.10.50 Release Notes** (Updated: March 24, 2025)
- **iDRAC9 Version 7.20.10.05 Release Notes** (Updated: March 21, 2025)
- **iDRAC9 Version 7.20.05.10 Release Notes** (Updated: April 08, 2025)
- **iDRAC9 Version 7.20.03.15 Release Notes** (Updated: May 06, 2025)
- **iDRAC9 Version 7.20.03.10 Release Notes** (Updated: April 16, 2025)

### Version 7.10.x Series
- **iDRAC9 Version 7.10.77.00 Release Notes** (Updated: April 15, 2025)

### Version 7.00.x Series
- **iDRAC9 Version 7.00.00.184 Release Notes** (Updated: April 11, 2026)
- **iDRAC9 Version 7.00.00.183 Release Notes** (Updated: October 17, 2025)
- **iDRAC9 Version 7.00.00.182 Release Notes** (Updated: August 21, 2025)
- **iDRAC9 Version 7.00.00.181 Release Notes** (Updated: March 21, 2025)

## Download Instructions

### Manual Download Process

1. **Access Dell Support Portal**
   - Navigate to: https://www.dell.com/support/product-details/en-us/product/idrac9-lifecycle-controller-v7.x-series/resources/manuals
   - Sign in with your Dell account (corporate account recommended for full access)

2. **Download Documentation**
   - Filter by language (English recommended)
   - Locate the desired document
   - Click on the document title to download

3. **Store in Appropriate Directory**
   - User Guides → `./idrac-architecture/guides/`
   - Release Notes → `./idrac-architecture/release-notes/`
   - Reference Guides → `./idrac-architecture/specs/`
   - Error Patterns → `./patterns/`

### Automated Download Setup

For automated downloads, consider setting up:
- Dell API access (if available for corporate accounts)
- Web scraping with authentication (respecting Dell's terms of service)
- Scheduled synchronization scripts

## Documentation Organization

### Directory Structure

```
idrac-architecture/
├── lld/                    # Low-Level Design documents
├── hld/                    # High-Level Design documents
├── guides/                 # User guides and manuals
│   ├── documentation-index.md
│   └── [downloaded guides]
├── specs/                  # Technical specifications and reference guides
└── release-notes/          # Version release notes
    └── [downloaded release notes]

patterns/                   # Error patterns and troubleshooting
└── [error pattern files]

known-issues/              # Known issues and workarounds
└── [known issue documentation]
```

## Maintenance

### Regular Updates

- **Quarterly**: Check for new documentation updates
- **Monthly**: Review new release notes
- **As Needed**: Update when new iDRAC versions are released

### Version Control

Consider storing documentation in a version control system to track changes and maintain history.

### Access Control

Ensure proper access controls are in place as some documentation may contain sensitive information.

## Contributing

When adding new documentation:
1. Update this index file
2. Place files in appropriate directories
3. Maintain consistent naming conventions
4. Include update dates and sources
5. Document any access requirements