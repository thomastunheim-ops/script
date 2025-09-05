#!/usr/bin/env python3
"""
IP Reputation Checker
Checks IP addresses using IPQualityScore
"""

import requests
import json
import sys
import argparse
import ipaddress

class IPReputationChecker:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()

    def check_ipqualityscore(self, ip: str):
        """Check IP reputation using IPQualityScore"""
        url = f"https://ipqualityscore.com/api/json/ip/{self.api_key}/{ip}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': f'IPQualityScore API error: {str(e)}'}

    def analyze_ipqualityscore_result(self, result: dict) -> dict:
        """Analyze IPQualityScore results"""
        if 'error' in result:
            return {'status': 'error', 'message': result['error']}

        fraud_score = result.get('fraud_score', 0)

        if fraud_score >= 85:
            threat_level = 'high'
        elif fraud_score >= 50:
            threat_level = 'medium'
        elif fraud_score >= 25:
            threat_level = 'low'
        else:
            threat_level = 'clean'

        return {
            'status': 'success',
            'threat_level': threat_level,
            'fraud_score': fraud_score,
            'proxy': result.get('proxy', False),
            'vpn': result.get('vpn', False),
            'tor': result.get('tor', False),
            'country': result.get('country_code', 'Unknown'),
            'isp': result.get('ISP', 'Unknown')
        }

    def check_ip_reputation(self, ip: str):
        """Check IP reputation (IPQualityScore only)"""
        print(f"Checking reputation for IP: {ip}")
        print("-" * 50)

        ipqs_result = self.check_ipqualityscore(ip)
        return self.analyze_ipqualityscore_result(ipqs_result)

    def print_results(self, ip: str, result: dict):
        """Print formatted results"""
        print(f"\n{'='*60}")
        print(f"IP REPUTATION REPORT FOR: {ip}")
        print(f"{'='*60}")

        if result['status'] == 'error':
            print(f"❌ Error: {result['message']}")
        else:
            emoji = {
                'clean': '✅',
                'low': '⚠️',
                'medium': '🔶',
                'high': '🚨'
            }.get(result['threat_level'], '❓')

            print(f"{emoji} Threat Level: {result['threat_level'].upper()}")
            print(f"   Fraud Score: {result['fraud_score']}")
            print(f"   Proxy: {'Yes' if result['proxy'] else 'No'}")
            print(f"   VPN: {'Yes' if result['vpn'] else 'No'}")
            print(f"   Tor: {'Yes' if result['tor'] else 'No'}")
            print(f"   Country: {result['country']}")
            print(f"   ISP: {result['isp']}")

        print(f"\n{'='*60}")


def main():
    parser = argparse.ArgumentParser(description='Check IP reputation with IPQualityScore')
    parser.add_argument('ip', nargs='?', help='IP address to check')
    parser.add_argument('--api-key', default="AIzaSyDBmZ_1gcUZRpAL29aGxdf2uUGAGS3sZ7Q",
                        help='API key for IPQualityScore')
    parser.add_argument('--json', action='store_true', help='Output results in JSON format')

    args = parser.parse_args()

    if not args.ip:
        args.ip = input("Enter IP address to check: ")

    try:
        ipaddress.ip_address(args.ip)
    except ValueError:
        print(f"Error: '{args.ip}' is not a valid IP address")
        sys.exit(1)

    checker = IPReputationChecker(args.api_key)
    result = checker.check_ip_reputation(args.ip)

    if args.json:
        print(json.dumps({args.ip: result}, indent=2))
    else:
        checker.print_results(args.ip, result)


if __name__ == "__main__":
    main()
