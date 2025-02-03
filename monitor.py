from playwright.sync_api import sync_playwright
import time
import random
import json
from ai_model import PredictionEngine

class WebsiteObserver:
    def __init__(self):
        self.config = json.load(open("config.json"))
        self.engine = PredictionEngine()
        self.last_outcome = None
        
    def get_website_data(self):
        """Stealthy data extraction with randomized behavior"""
        with sync_playwright() as p:
            # Configure stealth browser
            browser = p.chromium.launch(
                headless=True,
                proxy={"server": "per-context"} if self.config["stealth_mode"] else None
            )
            
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
                viewport={"width": 1920, "height": 1080}
            )
            
            page = context.new_page()
            page.goto(self.config["website_url"])
            
            # Randomize interaction patterns
            if self.config["stealth_mode"]:
                page.mouse.move(
                    random.randint(0, 1000), 
                    random.randint(0, 1000)
                )
                time.sleep(random.uniform(0.5, 2.0))
                
            # Extract game outcome
            outcome = page.query_selector(".game-result").inner_text()
            
            # Cleanup
            context.close()
            browser.close()
            
            return outcome.strip()

    def start_monitoring(self):
        """Main observation loop"""
        while True:
            try:
                current_outcome = self.get_website_data()
                if current_outcome != self.last_outcome:
                    analysis = self.engine.analyze_patterns(current_outcome)
                    self.display_prediction(analysis)
                    self.last_outcome = current_outcome
                
                # Randomized delay
                delay = self.config["check_interval"] + random.uniform(-2, 2)
                time.sleep(max(delay, 3))  # Minimum 3 seconds
                
            except Exception as e:
                print(f"Monitoring error: {str(e)}")
                time.sleep(10)

    def display_prediction(self, analysis):
        """Console display with formatting"""
        print(f"\n{' NEW PREDICTION '.center(40, '=')}")
        print(f"Current Outcome: {self.last_outcome}")
        print(f"Next Prediction: {analysis['prediction']}")
        print(f"Confidence: {analysis['confidence']*100:.1f}%")
        print(f"History: {len(self.engine.history)} analyzed outcomes")
        print("="*40)

if __name__ == "__main__":
    observer = WebsiteObserver()
    observer.start_monitoring()