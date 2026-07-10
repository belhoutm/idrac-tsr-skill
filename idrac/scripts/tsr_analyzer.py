#!/usr/bin/env python3
"""
TSR Analyzer - Analyze Dell Technical Support Reports for system health and diagnostics
"""

import zipfile
import xml.etree.ElementTree as ET
import tempfile
import os
from datetime import datetime
from collections import defaultdict


class TSRAnalyzer:
    """Analyze Dell Technical Support Reports"""
    
    def __init__(self, tsr_file):
        """
        Initialize TSR Analyzer
        
        Args:
            tsr_file: Path to TSR ZIP file
        """
        self.tsr_file = tsr_file
        self.temp_dir = tempfile.mkdtemp()
        self.extracted = False
        self.extract_tsr()
    
    def extract_tsr(self):
        """Extract TSR ZIP file to temporary directory"""
        try:
            with zipfile.ZipFile(self.tsr_file, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
            self.extracted = True
        except Exception as e:
            raise Exception(f"Failed to extract TSR file: {str(e)}")
    
    def cleanup(self):
        """Clean up temporary files"""
        if os.path.exists(self.temp_dir):
            for file in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        os.rmdir(file_path)
                except Exception as e:
                    print(f"Error cleaning up {file_path}: {str(e)}")
            os.rmdir(self.temp_dir)
    
    def get_system_info(self):
        """
        Extract basic system information from support.xml
        
        Returns:
            Dictionary with system information
        """
        support_xml = os.path.join(self.temp_dir, 'support.xml')
        
        if not os.path.exists(support_xml):
            return {}
        
        try:
            tree = ET.parse(support_xml)
            root = tree.getroot()
            
            sys_info = {}
            
            # Try to extract common fields
            for field in ['ServiceTag', 'Model', 'SerialNumber', 'AssetTag', 
                         'BIOSVersion', 'iDRACVersion']:
                element = root.find(f'.//{field}')
                if element is not None:
                    sys_info[field.lower()] = element.text
            
            # Get generation information
            gen_info = root.find('.//GenerationInformation')
            if gen_info is not None:
                gen_date = gen_info.find('GenerationDate')
                if gen_date is not None:
                    sys_info['generation_date'] = gen_date.text
            
            return sys_info
            
        except Exception as e:
            print(f"Error parsing system info: {str(e)}")
            return {}
    
    def get_hardware_inventory(self):
        """
        Extract hardware inventory from system.xml
        
        Returns:
            Dictionary with hardware inventory
        """
        system_xml = os.path.join(self.temp_dir, 'system.xml')
        
        if not os.path.exists(system_xml):
            return {}
        
        try:
            tree = ET.parse(system_xml)
            root = tree.getroot()
            
            inventory = {
                'processors': [],
                'memory': [],
                'storage': [],
                'network': []
            }
            
            # Extract processors
            for proc in root.findall('.//Processor'):
                proc_info = {
                    'id': self._get_element_text(proc, 'ID'),
                    'manufacturer': self._get_element_text(proc, 'Manufacturer'),
                    'model': self._get_element_text(proc, 'Model'),
                    'cores': self._get_element_text(proc, 'Cores'),
                    'threads': self._get_element_text(proc, 'Threads'),
                    'speed': self._get_element_text(proc, 'Speed'),
                    'status': self._get_element_text(proc, 'Status'),
                    'health': self._get_element_text(proc, 'Health')
                }
                inventory['processors'].append(proc_info)
            
            # Extract memory
            for dimm in root.findall('.//DIMM'):
                dimm_info = {
                    'id': self._get_element_text(dimm, 'ID'),
                    'manufacturer': self._get_element_text(dimm, 'Manufacturer'),
                    'capacity': self._get_element_text(dimm, 'Capacity'),
                    'type': self._get_element_text(dimm, 'Type'),
                    'speed': self._get_element_text(dimm, 'Speed'),
                    'status': self._get_element_text(dimm, 'Status'),
                    'health': self._get_element_text(dimm, 'Health')
                }
                inventory['memory'].append(dimm_info)
            
            return inventory
            
        except Exception as e:
            print(f"Error parsing hardware inventory: {str(e)}")
            return {}
    
    def get_system_logs(self):
        """
        Extract system event logs from sel.xml
        
        Returns:
            List of log entries
        """
        sel_xml = os.path.join(self.temp_dir, 'sel.xml')
        
        if not os.path.exists(sel_xml):
            return []
        
        try:
            tree = ET.parse(sel_xml)
            root = tree.getroot()
            
            logs = []
            for entry in root.findall('.//Entry'):
                log_entry = {
                    'id': self._get_element_text(entry, 'ID'),
                    'timestamp': self._get_element_text(entry, 'Timestamp'),
                    'severity': self._get_element_text(entry, 'Severity'),
                    'category': self._get_element_text(entry, 'Category'),
                    'message': self._get_element_text(entry, 'Message'),
                    'component': self._get_element_text(entry, 'Component')
                }
                logs.append(log_entry)
            
            return logs
            
        except Exception as e:
            print(f"Error parsing system logs: {str(e)}")
            return []
    
    def get_firmware_versions(self):
        """
        Extract firmware versions from firmware.xml
        
        Returns:
            List of firmware components
        """
        firmware_xml = os.path.join(self.temp_dir, 'firmware.xml')
        
        if not os.path.exists(firmware_xml):
            return []
        
        try:
            tree = ET.parse(firmware_xml)
            root = tree.getroot()
            
            firmware = []
            for component in root.findall('.//Component'):
                fw_info = {
                    'name': self._get_element_text(component, 'Name'),
                    'version': self._get_element_text(component, 'Version'),
                    'release_date': self._get_element_text(component, 'ReleaseDate'),
                    'status': self._get_element_text(component, 'Status')
                }
                firmware.append(fw_info)
            
            return firmware
            
        except Exception as e:
            print(f"Error parsing firmware versions: {str(e)}")
            return []
    
    def analyze_errors(self):
        """
        Analyze system logs for errors and warnings
        
        Returns:
            Dictionary with categorized errors
        """
        logs = self.get_system_logs()
        
        errors = {
            'critical': [],
            'warning': [],
            'info': []
        }
        
        for log in logs:
            severity = log.get('severity', 'Info')
            if severity == 'Critical':
                errors['critical'].append(log)
            elif severity == 'Warning':
                errors['warning'].append(log)
            else:
                errors['info'].append(log)
        
        return errors
    
    def assess_health(self):
        """
        Comprehensive health assessment
        
        Returns:
            Dictionary with health assessment
        """
        inventory = self.get_hardware_inventory()
        errors = self.analyze_errors()
        
        health_assessment = {
            'overall_health': 'OK',
            'health_score': 100,
            'component_health': {},
            'issues': [],
            'recommendations': []
        }
        
        # Check processor health
        failed_processors = [p for p in inventory.get('processors', []) 
                           if p.get('health') != 'OK']
        health_assessment['component_health']['processors'] = {
            'status': 'OK' if not failed_processors else 'Critical',
            'failed_count': len(failed_processors)
        }
        
        if failed_processors:
            health_assessment['health_score'] -= 20
            health_assessment['issues'].append(
                f"{len(failed_processors)} processor(s) failed health check"
            )
        
        # Check memory health
        failed_memory = [m for m in inventory.get('memory', []) 
                       if m.get('health') != 'OK']
        health_assessment['component_health']['memory'] = {
            'status': 'OK' if not failed_memory else 'Warning',
            'failed_count': len(failed_memory)
        }
        
        if failed_memory:
            health_assessment['health_score'] -= 10
            health_assessment['issues'].append(
                f"{len(failed_memory)} memory module(s) failed health check"
            )
        
        # Check for critical errors
        if errors['critical']:
            health_assessment['health_score'] -= 30
            health_assessment['issues'].append(
                f"{len(errors['critical'])} critical error(s) detected"
            )
        
        # Check for warnings
        if errors['warning']:
            health_assessment['health_score'] -= 5
        
        # Determine overall health
        if health_assessment['health_score'] >= 90:
            health_assessment['overall_health'] = 'OK'
        elif health_assessment['health_score'] >= 70:
            health_assessment['overall_health'] = 'Warning'
        else:
            health_assessment['overall_health'] = 'Critical'
        
        # Generate recommendations
        if health_assessment['overall_health'] != 'OK':
            health_assessment['recommendations'].append(
                f"System health is {health_assessment['overall_health']}. "
                "Immediate attention recommended."
            )
        
        if errors['critical']:
            health_assessment['recommendations'].append(
                f"Review {len(errors['critical'])} critical error(s) in system logs"
            )
        
        return health_assessment
    
    def generate_report(self):
        """
        Generate comprehensive analysis report
        
        Returns:
            Dictionary with complete analysis report
        """
        report = {
            'system_info': self.get_system_info(),
            'hardware_inventory': self.get_hardware_inventory(),
            'system_logs': self.get_system_logs(),
            'firmware_versions': self.get_firmware_versions(),
            'error_analysis': self.analyze_errors(),
            'health_assessment': self.assess_health(),
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def _get_element_text(self, parent, tag):
        """Helper to safely get element text"""
        element = parent.find(tag)
        return element.text if element is not None else 'Unknown'
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.cleanup()


def main():
    """Example usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python tsr_analyzer.py <tsr_file.zip>")
        sys.exit(1)
    
    tsr_file = sys.argv[1]
    
    try:
        print(f"Analyzing TSR file: {tsr_file}")
        analyzer = TSRAnalyzer(tsr_file)
        
        # Generate report
        report = analyzer.generate_report()
        
        # Print summary
        print("\n=== System Information ===")
        sys_info = report['system_info']
        print(f"Service Tag: {sys_info.get('service_tag', 'Unknown')}")
        print(f"Model: {sys_info.get('model', 'Unknown')}")
        print(f"Serial Number: {sys_info.get('serial_number', 'Unknown')}")
        print(f"BIOS Version: {sys_info.get('biosversion', 'Unknown')}")
        print(f"iDRAC Version: {sys_info.get('idracversion', 'Unknown')}")
        
        print("\n=== Health Assessment ===")
        health = report['health_assessment']
        print(f"Overall Health: {health['overall_health']}")
        print(f"Health Score: {health['health_score']}")
        
        print("\n=== Component Health ===")
        for component, data in health['component_health'].items():
            print(f"{component}: {data['status']}")
        
        print("\n=== Error Analysis ===")
        errors = report['error_analysis']
        print(f"Critical Errors: {len(errors['critical'])}")
        print(f"Warnings: {len(errors['warning'])}")
        
        print("\n=== Recommendations ===")
        for rec in health['recommendations']:
            print(f"- {rec}")
        
        # Save full report to JSON
        import json
        output_file = tsr_file.replace('.zip', '_report.json')
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nFull report saved to: {output_file}")
        
    except Exception as e:
        print(f"Error analyzing TSR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()