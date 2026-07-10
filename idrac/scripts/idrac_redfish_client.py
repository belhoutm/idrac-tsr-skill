#!/usr/bin/env python3
"""
iDRAC Redfish Client - Basic client for Dell iDRAC Redfish API operations
"""

import requests
import json
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning
import urllib3

# Suppress SSL warnings for testing (remove in production)
urllib3.disable_warnings(InsecureRequestWarning)


class IDRACRedfishClient:
    """Client for interacting with Dell iDRAC via Redfish API"""
    
    def __init__(self, host, username, password, verify_ssl=False):
        """
        Initialize iDRAC Redfish client
        
        Args:
            host: iDRAC IP address or hostname
            username: iDRAC username
            password: iDRAC password
            verify_ssl: Whether to verify SSL certificates (default: False)
        """
        self.host = host
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self.base_url = f"https://{host}/redfish/v1"
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, password)
    
    def get(self, endpoint):
        """
        Perform GET request to Redfish endpoint
        
        Args:
            endpoint: Redfish endpoint path (e.g., '/Systems/System.Embedded.1')
        
        Returns:
            JSON response data
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, verify=self.verify_ssl)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"GET request failed: {response.status_code} - {response.text}")
    
    def post(self, endpoint, data):
        """
        Perform POST request to Redfish endpoint
        
        Args:
            endpoint: Redfish endpoint path
            data: Dictionary of data to send
        
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        response = self.session.post(url, json=data, headers=headers, verify=self.verify_ssl)
        
        if response.status_code in [200, 202]:
            return response
        else:
            raise Exception(f"POST request failed: {response.status_code} - {response.text}")
    
    def patch(self, endpoint, data):
        """
        Perform PATCH request to Redfish endpoint
        
        Args:
            endpoint: Redfish endpoint path
            data: Dictionary of data to update
        
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        response = self.session.patch(url, json=data, headers=headers, verify=self.verify_ssl)
        
        if response.status_code == 200:
            return response
        else:
            raise Exception(f"PATCH request failed: {response.status_code} - {response.text}")
    
    def get_system_info(self):
        """Get system information"""
        return self.get('/Systems/System.Embedded.1')
    
    def get_power_state(self):
        """Get current power state"""
        system = self.get_system_info()
        return system.get('PowerState', 'Unknown')
    
    def power_on(self):
        """Power on the server"""
        return self.post('/Systems/System.Embedded.1/Actions/ComputerSystem.Reset',
                        {'ResetType': 'On'})
    
    def power_off(self, force=False):
        """
        Power off the server
        
        Args:
            force: Force power off (default: False, attempts graceful shutdown)
        """
        reset_type = 'ForceOff' if force else 'GracefulShutdown'
        return self.post('/Systems/System.Embedded.1/Actions/ComputerSystem.Reset',
                        {'ResetType': reset_type})
    
    def restart_server(self, force=False):
        """
        Restart the server
        
        Args:
            force: Force restart (default: False, attempts graceful restart)
        """
        reset_type = 'ForceRestart' if force else 'GracefulRestart'
        return self.post('/Systems/System.Embedded.1/Actions/ComputerSystem.Reset',
                        {'ResetType': reset_type})
    
    def get_processors(self):
        """Get processor information"""
        return self.get('/Systems/System.Embedded.1/Processors')
    
    def get_memory(self):
        """Get memory information"""
        return self.get('/Systems/System.Embedded.1/Memory')
    
    def get_storage(self):
        """Get storage information"""
        return self.get('/Systems/System.Embedded.1/Storage')
    
    def get_network_interfaces(self):
        """Get network interface information"""
        return self.get('/Systems/System.Embedded.1/EthernetInterfaces')
    
    def get_system_health(self):
        """Get system health status"""
        system = self.get_system_info()
        return system.get('Status', {})
    
    def get_temperature(self):
        """Get temperature readings"""
        return self.get('/Systems/System.Embedded.1/Thermal')
    
    def get_power_consumption(self):
        """Get power consumption data"""
        return self.get('/Systems/System.Embedded.1/Power')
    
    def get_system_logs(self, log_type='SEL'):
        """
        Get system logs
        
        Args:
            log_type: Type of log ('SEL' for System Event Log, 'LifecycleLog' for Lifecycle Log)
        """
        endpoint = f'/Systems/System.Embedded.1/LogServices/{log_type}/Entries'
        return self.get(endpoint)
    
    def set_boot_override(self, boot_target, mode='UEFI'):
        """
        Set boot override for next boot
        
        Args:
            boot_target: Boot target (Pxe, Cd, Usb, Hdd, BiosSetup, UefiTarget)
            mode: Boot mode (UEFI, Legacy)
        """
        return self.patch('/Systems/System.Embedded.1',
                         {'Boot': {
                             'BootSourceOverrideEnabled': 'Once',
                             'BootSourceOverrideTarget': boot_target,
                             'BootSourceOverrideMode': mode
                         }})
    
    def mount_virtual_media(self, media_id, image_url):
        """
        Mount virtual media
        
        Args:
            media_id: Media slot ID (e.g., 'CD', 'USB')
            image_url: URL to the ISO image
        """
        endpoint = f'/Managers/iDRAC.Embedded.1/VirtualMedia/{media_id}/Actions/VirtualMedia.InsertMedia'
        return self.post(endpoint, {
            'Image': image_url,
            'Inserted': True,
            'WriteProtected': True
        })
    
    def eject_virtual_media(self, media_id):
        """
        Eject virtual media
        
        Args:
            media_id: Media slot ID (e.g., 'CD', 'USB')
        """
        endpoint = f'/Managers/iDRAC.Embedded.1/VirtualMedia/{media_id}/Actions/VirtualMedia.EjectMedia'
        return self.post(endpoint, {})
    
    def get_firmware_inventory(self):
        """Get firmware inventory"""
        return self.get('/UpdateService/FirmwareInventory')
    
    def update_firmware(self, firmware_url, component_target):
        """
        Update firmware
        
        Args:
            firmware_url: URL to firmware file
            component_target: Target component (e.g., '/redfish/v1/Systems/System.Embedded.1')
        """
        response = self.post('/UpdateService/Actions/UpdateService.SimpleUpdate',
                            {'ImageURI': firmware_url, 'Targets': [component_target]})
        
        if response.status == 202:
            job_id = response.headers.get('Location')
            return job_id
        return None
    
    def monitor_job(self, job_id):
        """
        Monitor job progress
        
        Args:
            job_id: Job ID to monitor
        """
        while True:
            try:
                job = self.get(job_id)
                state = job.get('JobState', 'Unknown')
                
                if state == 'Completed':
                    return True, job
                elif state in ['Failed', 'Exception']:
                    return False, job
                
                percent_complete = job.get('PercentComplete', 0)
                print(f"Job progress: {percent_complete}%")
                
            except Exception as e:
                return False, {'error': str(e)}
            
            time.sleep(10)


def main():
    """Example usage"""
    # Initialize client
    # SECURITY: Replace with your actual credentials
    # Never commit real credentials to Git
    client = IDRACRedfishClient(
        host='192.168.1.100',
        username='<YOUR_USERNAME>',
        password='<YOUR_PASSWORD>',
        verify_ssl=False
    )
    
    try:
        # Get system information
        print("Getting system information...")
        system_info = client.get_system_info()
        print(f"Model: {system_info.get('Model')}")
        print(f"Serial Number: {system_info.get('SerialNumber')}")
        print(f"Power State: {system_info.get('PowerState')}")
        
        # Get system health
        print("\nGetting system health...")
        health = client.get_system_health()
        print(f"Health Status: {health.get('Health', 'Unknown')}")
        
        # Get temperature
        print("\nGetting temperature readings...")
        temp = client.get_temperature()
        for reading in temp.get('Temperatures', []):
            print(f"{reading.get('Name')}: {reading.get('ReadingCelsius')}°C")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()