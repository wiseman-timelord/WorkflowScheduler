import gradio as gr
from scripts.utility_misc import validate_config, countdown_timer
import threading

def launch_interface(config, save_config, port=7860):
    """Launch the Gradio interface with configuration and save functionality."""
    interrupt_event = threading.Event()

    def configure_schedule(data):
        """Update the schedule and save it to file."""
        config = [{"event": label.strip(), "duration": int(duration.strip()) if duration.strip().isdigit() else 0}
                  for label, duration in zip(data["event"], data["duration"])]
        save_config(config)
        return "Schedule Saved!"

    def start_schedule(config):
        """Transition to the execution page with validated events."""
        events = validate_config(config)
        if not events:
            return "No valid events to execute!", gr.update(visible=True), gr.update(visible=False)
        return "Starting schedule...", gr.update(visible=False), gr.update(visible=True, value=events)

    def run_schedule(events):
        """Execute the schedule with timers and progress updates."""
        interrupt_event.clear()
        progress_updates = []
        for event in events:
            if interrupt_event.is_set():
                yield "Execution stopped!", 0
                return
            progress_updates.append(f"Starting: {event['event']}")
            yield "\n".join(progress_updates), len(progress_updates) / len(events) * 100
            countdown_timer(event["duration"] * 60, lambda r, d: None, interrupt_event)
        yield "All events completed!", 100

    def stop_execution():
        """Stop current execution and reset to configuration."""
        interrupt_event.set()
        return gr.update(visible=False), gr.update(visible=True)

    # Build Gradio UI
    with gr.Blocks() as app:
        with gr.Row(visible=True) as configure_page:
            event_labels = gr.Textbox(placeholder="Enter Event Labels (one per line)", lines=10, label="Events")
            event_durations = gr.Textbox(placeholder="Enter Durations in Minutes (one per line)", lines=10, label="Durations")
            save_btn = gr.Button("Save And Start")

        with gr.Row(visible=False) as execution_page:
            current_event = gr.Textbox(label="Current Event", interactive=False)
            progress_bar = gr.Slider(0, 100, step=1, label="Progress", interactive=False)
            stop_btn = gr.Button("Stop and Exit")
            back_btn = gr.Button("Back to Configure")

        save_btn.click(
            lambda labels, durations: configure_schedule({"event": labels.split("\n"), "duration": durations.split("\n")}),
            [event_labels, event_durations],
            [configure_page, execution_page]
        )

        stop_btn.click(stop_execution, None, [execution_page, configure_page])

        app.launch(server_name="0.0.0.0", server_port=port)  # Ensure accessibility on Linux
