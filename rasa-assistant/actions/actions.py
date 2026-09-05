from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionPlayMusic(Action):
    def name(self):
        return "action_play_music"

    def run(self, dispatcher, tracker, domain):
        song = tracker.get_slot("song")

        if song:
            message = f"Playing {song}."
        else:
            message = "Playing music."

        dispatcher.utter_message(text=message)
        return []


class ActionPauseMusic(Action):
    def name(self):
        return "action_pause_music"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Music paused.")
        return []


class ActionResumeMusic(Action):
    def name(self):
        return "action_resume_music"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Resuming music.")
        return []


class ActionStopMusic(Action):
    def name(self):
        return "action_stop_music"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Music stopped.")
        return []


class ActionNextSong(Action):
    def name(self):
        return "action_next_song"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Playing the next song.")
        return []


class ActionPreviousSong(Action):
    def name(self):
        return "action_previous_song"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Playing the previous song.")
        return []
