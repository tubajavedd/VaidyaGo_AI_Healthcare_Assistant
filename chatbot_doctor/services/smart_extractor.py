import re

class SmartExtractor:
    @staticmethod
    def extract_slot_generation_details(message):
        """
        Attempts to extract dates and durations for slot generation.
        Example: "Generate 30 min slots for tomorrow"
        """
        data = {}
        
        # Extract duration
        duration_match = re.search(r'(\d+)\s*(min|minute)', message.lower())
        if duration_match:
            data['slot_duration'] = int(duration_match.group(1))
        
        # Simple date logic
        if 'tomorrow' in message.lower():
            from datetime import datetime, timedelta
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            data['start_date'] = tomorrow
            data['end_date'] = tomorrow
            
        return data

    @staticmethod
    def extract_date(message):
        # Basic regex for YYYY-MM-DD
        date_match = re.search(r'\d{4}-\d{2}-\d{2}', message)
        return date_match.group(0) if date_match else None
