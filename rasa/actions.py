
import requests
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionCoronaTracker(Action):
    def name(self) -> Text:
        return "action_corona_tracker"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response=requests.get("https://api.covid19india.org/data.json").json()
        entities=tracker.latest_message['entities']
        print('Last Message Now',entities)
        state= None
        for e in entities:
            if (e['entity']=='state'):
                state=e['value']
        message='Please enter correct state name'
        if(state=='india'):
            state='Total'
        for data in response['statewise']:
            if(data['state']==state.title()):
                print(data)
                message="Active: "+data["active"] +" Confirmed: " + data["confirmed"] +" Recovered: " + data["recovered"] +" Deaths:" + data["deaths"] +" Updated On "+data["lastupdatedtime"]
                print(message)
         
        dispatcher.utter_message(message)
        return []
